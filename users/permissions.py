from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Проверка, является ли пользователь владельцем
        """
        return obj.owner == request.user


class IsCurrentUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Проверка, является ли текущий пользователь владельцем учетной записи
        """
        return obj == request.user
