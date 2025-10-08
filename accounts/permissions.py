# accounts/permissions.py
from rest_framework.permissions import BasePermission
from accounts.models import StaffUser

class RolePermission(BasePermission):
    """
    Allow access only if request.user.role is in required_roles.
    """

    required_roles = []

    def has_permission(self, request, view):
        # Check authentication first
        if not request.user or not request.user.is_authenticated:
            return False

        # Get roles from view if available
        roles = getattr(view, "required_roles", self.required_roles)
        user_role = getattr(request.user, "role", "").strip().upper()
        return user_role in [r.upper() for r in roles]


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