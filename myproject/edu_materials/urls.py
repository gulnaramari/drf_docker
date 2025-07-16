from django.urls import path
from rest_framework.routers import DefaultRouter

from .apps import EduMaterialsConfig
from .views import LessonCreateAPIView

app_name = EduMaterialsConfig.name



urlpatterns = [
    path("lessons/new", LessonCreateAPIView.as_view(), name="create_lesson"),
   ]


