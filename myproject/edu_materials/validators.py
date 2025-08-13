from rest_framework import serializers
from urllib.parse import urlparse
from django.conf import settings
from myproject.edu_materials import serializers


class URLValidator:
    """Класс для валидации ссылок на курс."""

    def __init__(self, field):
        """Метод для инициализации объекта класса."""
        self.field = field

    def __fields__(self):
        return [self.field]

    def validate_video_url(self, value):
        if not value:
            return value
        host = (urlparse(value).hostname or "").lower()
        allowed = getattr(settings, "ALLOWED_LESSON_DOMAINS", ("youtube.com",))
        if not any(host == d or host.endswith("." + d) for d in allowed):
            raise serializers.ValidationError("Допустимы ссылки только на youtube.com")
        return value
