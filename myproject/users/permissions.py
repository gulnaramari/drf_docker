from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    """Модель для получения прав группы модераторов."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    """Модель для получения прав у владельцев курса или лекции."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUser(BasePermission):
    """Модель для получения прав у пользователей"""

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsUserOwner(BasePermission):
    """Класс ограничений по доступу для владельцев профилей пользователя."""

    def has_object_permission(self, request, view, obj):
        """Метод для проверки прав доступа у пользователя на объект."""

        if request.user == obj:
            return True
        return False
