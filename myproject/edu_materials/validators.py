from urllib.parse import urlparse
from rest_framework.serializers import ValidationError

class URLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        url = attrs.get(self.field)
        if not url:
            return
        try:
            p = urlparse(url)
        except Exception:
            raise ValidationError("Ссылка не корректна. Не корректный формат ссылки.")
        if p.scheme not in ("http", "https") or not p.netloc:
            raise ValidationError("Ссылка не корректна. Не корректный формат ссылки.")
        host = (p.hostname or "").lower()
        if not (host == "youtube.com" or host.endswith(".youtube.com")):
            raise ValidationError("Ссылка на видео разрешена только с сайта youtube.com.")
