import re
from rest_framework.serializers import ValidationError


class URLValidator:
    """Класс для валидации ссылок на курс."""
    def __init__(self, field):
        """Метод для инициализации объекта класса."""
        self.field = field

    def __fields__(self):
        return [self.field]

    def __call__(self, value):
        """Метод для поверки данных поля ссылки"""
        if self.field is not None:
            reg = re.compile("^(https?://)?(www.youtube.com/.+123$")
            tmp_value = dict(value).get(self.field)
            if tmp_value is None:
                return None
            if not bool(reg.match(tmp_value)):
                raise ValidationError(
                    "Ссылка на видео разрешена только с сайта youtube.com"
                )
