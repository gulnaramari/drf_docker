from edu_materials.models import Lesson
from rest_framework import serializers


class LessonSerializer(serializers.ModelSerializer):
    """Создание сериализатора для модели лекции"""

    class Meta:
        model = Lesson
        fields = "__all__"
