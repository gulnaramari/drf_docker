from django.db import models

from django.conf import settings


class Course(models.Model):
    """Создание модели курса с соответствующими полями"""

    name = models.CharField(
        max_length=100,
        verbose_name="название курса",
        help_text="укажите название курса",
    )
    preview = models.ImageField(
        upload_to="edu_materials/previews",
        verbose_name="превью",
        blank=True,
        null=True,
        help_text="Загрузите превью",
    )
    description = models.TextField(
        max_length=250,
        verbose_name="описание курса",
        help_text="опишите курс",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="owner",
        help_text="Укажите владельца курса",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="Дата изменения"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """Создание модели лекции с соответствующими полями"""

    name = models.CharField(
        max_length=100,
        verbose_name="название урока",
        help_text="укажите название урока",
    )
    description = models.TextField(
        max_length=250,
        verbose_name="описание урока",
        help_text="опишите урок",
        blank=True,
        null=True,
    )
    preview = models.ImageField(
        upload_to="edu_materials/pictures",
        verbose_name="картинка",
        blank=True,
        null=True,
        help_text="Загрузите изображение",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        related_name="lessons",
        verbose_name="course",
        help_text="Select the course",
        null=True,
        blank=True,
    )
    video_url = models.URLField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="ссылка на видео",
        help_text="загрузите видео",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="lessons",
        verbose_name="owner",
        help_text="Укажите владельца лекции",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="Дата изменения"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
