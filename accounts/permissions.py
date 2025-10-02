from rest_framework.permissions import BasePermission

from accounts.models import StaffUser

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
