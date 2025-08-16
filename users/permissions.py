from rest_framework import permissions

from users.models import User


class IsAdminOrAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User):
            return request.user.is_staff or obj == request.user
        return request.user.is_staff or obj.author == request.user
