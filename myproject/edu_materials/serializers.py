from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from .models import Course, Lesson
from .validators import URLValidator


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
    lesson = LessonSerializer(read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    count_subscriptions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id", "amount_of_lessons", "lesson",
            "is_subscribed", "count_subscriptions",
            "name", "preview", "description", "owner",
            "created_at", "updated_at",
        ]

    def get_amount_of_lessons(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        return False

    def get_count_subscriptions(self, obj):
        return "Подписок - 0."


class DocNoPermissionSerializer(serializers.Serializer):
    detail = serializers.CharField(default="У вас нет права на это действие")
