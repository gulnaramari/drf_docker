from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import EduMaterialsConfig
from .views import (
    CourseViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    )

app_name = EduMaterialsConfig.name

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("lessons/new", LessonCreateAPIView.as_view(), name="create_lesson"),
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path(
        "lessons/<int:pk>/update", LessonUpdateAPIView.as_view(), name="update_lesson"
    ),
    path(
        "lessons/<int:pk>/delete", LessonDestroyAPIView.as_view(), name="delete_lesson"
    ),
]

urlpatterns += router.urls
