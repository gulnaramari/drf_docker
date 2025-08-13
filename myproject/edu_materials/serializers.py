from urllib.parse import urlparse
from django.conf import settings
from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from .models import Course, Lesson


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
    class Meta:
        model = Lesson
        fields = [
            "id", "name", "description", "preview", "video_url",
            "course", "owner", "created_at", "updated_at",
        ]

    def validate_video_url(self, value):
        # допускаем пустое значение
        if not value:
            return value
        host = (urlparse(value).hostname or "").lower()
        allowed = getattr(settings, "ALLOWED_LESSON_DOMAINS", ("youtube.com",))
        # разрешаем поддомены, например www.youtube.com
        if not any(host == d or host.endswith("." + d) for d in allowed):
            raise serializers.ValidationError("Допустимы ссылки только на youtube.com")
        return value


class CourseSerializer(serializers.ModelSerializer):
    """Создание кастомного сериализатора для модели курса
    с дополнительными полями и вложенным сериализатором по лекции"""

    amount_of_lessons = serializers.SerializerMethodField(read_only=True)
    lesson = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    count_subscriptions = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "amount_of_lessons",
            "lesson",
            "is_subscribed",
            "count_subscriptions",
            "name", "preview", "description", "owner",
            "created_at", "updated_at",
        ]

    def get_amount_of_lessons(self, obj):
        # Берём менеджер обратной связи независимо от related_name
        manager = getattr(obj, "lessons", None) or getattr(obj, "lesson", None) or obj.lesson_set
        return manager.count()

    def get_lesson(self, obj):
        manager = getattr(obj, "lessons", None) or getattr(obj, "lesson", None) or obj.lesson_set
        qs = manager.all().order_by("id")
        return LessonSerializer(qs, many=True).data

    def get_is_subscribed(self, obj):
        return False

    def get_count_subscriptions(self, obj):
        return "Подписок - 0."


class DocNoPermissionSerializer(serializers.Serializer):
    detail = serializers.CharField(default="У вас нет права на это действие")
