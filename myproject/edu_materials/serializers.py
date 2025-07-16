from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers

from .models import Course, Lesson
from .validators import URLValidator
from users.models import Subscription


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Example 1",
            value={
                "video_url": "http://youtube.com/your-lesson",
                "name": "string",
                "description": "string",
                "preview": "string",
                "course": 0,
            },
            request_only=True,
        ),
    ]
)
class LessonSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели лекции"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [URLValidator(field="video_url")]


class CourseSerializer(serializers.ModelSerializer):
    """Создание кастомного сериализатора для модели курса
    с дополнительными полями и вложенным сериализатором по лекции"""

    amount_of_lessons = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    count_subscriptions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """Класс для изменения поведения полей сериализатора модели "Курс"."""

        model = Course
        fields = "__all__"

    def get_amount_of_lessons(self, course):
        """Метод для вывода информации о количестве уроков в курсе."""
        return Lesson.objects.filter(course=course).count()

    def get_count_subscriptions(self, instance):
        """Метод для вывода информации о количестве подписок на курс."""
        return f"Подписок - {Subscription.objects.filter(course=instance).count()}."

    def get_is_subscribed(self, course):
        """Метод для вывода информации о подписке текущего пользователя на курс."""
        user = self.context["request"].user
        subscription = Subscription.objects.all().filter(user=user, course=course).exists()
        if subscription:
            return "У Вас есть подписка на данный курс."
        return False



class DocNoPermissionSerializer(serializers.Serializer):
    detail = serializers.CharField(default="У вас нет права на это действие")
