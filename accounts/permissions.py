# accounts/permissions.py
from rest_framework.permissions import BasePermission

from accounts.models import StaffUser

class RolePermission(BasePermission):
    """
    Flexible permission class for role-based access.
    Usage in views: permission_classes = [RolePermission(required_roles=["HR"])]
    """
    message = "You do not have permission to perform this action."

    def __init__(self, required_roles=None):
        self.required_roles = required_roles or []

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in self.required_roles
        )

class IsAdminUserRole(BasePermission):
    """
    Allows access only to users with role=ADMIN.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == StaffUser.Role.ADMIN
        )