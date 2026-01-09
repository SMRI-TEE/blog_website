
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        # Admin can do anything
        if request.user and request.user.is_staff:
            return True

        # Read-only permissions
        if request.method in permissions.SAFE_METHODS:
            return True

        # Blog owner
        if hasattr(obj, 'author'):
            return obj.author == request.user

        # Comment owner
        if hasattr(obj, 'user'):
            return obj.user == request.user

        return False

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Only superuser/admin can create/update/delete.
    Others can only read.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser
    