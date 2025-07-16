from django.shortcuts import render
from rest_framework import generics

from edu_materials.models import Lesson
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator, IsOwner
from .models import Course, Lesson
from .serializers import LessonSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание контроллера для создания лекции немодератором."""

    serializer_class = LessonSerializer
    permission_classes = (~IsModerator,)
    queryset = Lesson.objects.all().order_by("id")

    def perform_create(self, serializer):
        """Метод для присваивания лекции владельцу."""
        lesson = serializer.save(owner=self.request.user)
        lesson.save()
