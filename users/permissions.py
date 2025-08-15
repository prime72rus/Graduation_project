from rest_framework import permissions


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.author is None:
            return False
        return obj.author == request.user
