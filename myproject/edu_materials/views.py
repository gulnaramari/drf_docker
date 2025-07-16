from datetime import timedelta
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets, status
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsModerator, IsOwner
from .paginators import LMSPagination
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, DocNoPermissionSerializer



@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="description from swagger_auto_schema via method_decorator"
))
class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер-вьюсет для CRUD
    с правами для работы модераторов, немодераторов или владельцев курсов, лекций"""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LMSPagination

    def get_permissions(self):
        """Метод разграничения разрешений на доступ к эндпоитам в соответствии с запросом."""
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated & ~IsModerator]
        elif self.action in ['list', 'change', 'retrieve']:
            self.permission_classes = [IsAuthenticated & IsOwner | IsAuthenticated & IsModerator]
        elif self.action in ['destroy']:
            self.permission_classes = [IsAuthenticated & IsOwner]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Метод для присваивания курса владельцу"""
        new_course = serializer.save(owner=self.request.user)
        new_course.save()


    def get_queryset(self):
        """Метод для изменения запроса к базе данных по объектам модели "Курса"."""
        if self.request.user.groups.filter(name="Модератор").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


@extend_schema(
    responses={
        status.HTTP_201_CREATED: LessonSerializer,
        status.HTTP_403_FORBIDDEN: DocNoPermissionSerializer,
    },
)
class LessonCreateAPIView(generics.CreateAPIView):
    """Создание контроллера для создания лекции немодератором."""

    serializer_class = LessonSerializer
    permission_classes = (~IsModerator,)
    queryset = Lesson.objects.all().order_by("id")

    def perform_create(self, serializer):
        """Метод для присваивания лекции владельцу."""
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Создание контроллера для вывода списка лекций,
    которые могут просматривать владельцы или модераторы"""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]
    pagination_class = LMSPagination

    def get_queryset(self):
        """Метод, позволяет получить список лекции владельца или модератора"""
        if not IsModerator().has_permission(self.request, self):
            return Lesson.objects.filter(owner=self.request.user)
        return Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Класс, позволяет модератору или владельцу получить детали лекции"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Класс, позволяет модератору или владельцу редактировать лекцию"""

    queryset = Lesson.objects.all().order_by("id")
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]





class LessonDestroyAPIView(generics.DestroyAPIView):
    """Класс, позволяет немодератору или владельцу удалить лекцию"""

    queryset = Lesson.objects.all().order_by("id")
    permission_classes = [IsAuthenticated & IsModerator | IsAuthenticated & IsOwner]
