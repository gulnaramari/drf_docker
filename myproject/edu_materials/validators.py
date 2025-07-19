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
        """Метод для получения и проверки указанных данных поля ссылки на видео у объекта модели "Урок"."""

        reg = re.compile('^(https?:\/\/)?([\w-]{1,32}\.[\w-]{1,32})[^\s@]*$')
        tmp_val = dict(value).get(self.field)
        if not value or value is None or not bool(reg.match(tmp_val)):
            raise ValidationError('Ссылка не корректна. Не корректный формат ссылки.')
        elif "youtube.com" not in tmp_val:
            raise ValidationError(f'Ссылка на видео разрешена только с сайта youtube.com.')
