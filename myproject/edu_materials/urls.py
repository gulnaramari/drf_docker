from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListAPIView, LessonRetrieveAPIView,
    LessonCreateAPIView, LessonUpdateAPIView, LessonDestroyAPIView,
)

app_name = "edu_materials"

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="courses")

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonListAPIView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_detail"),
    path("lessons/create/", LessonCreateAPIView.as_view(), name="create_lesson"),
    path("lessons/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="update_lesson"),
    path("lessons/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="delete_lesson"),
]
