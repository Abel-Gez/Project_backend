from rest_framework import viewsets, permissions
from .models import VacancyApplication
from .serializers import VacancyApplicationSerializer
from accounts.permissions import RolePermission

class IsHRStaff(permissions.BasePermission):
    """
    Only HR staff (specific user) can view submissions.
    """
    def has_permission(self, request, view):
        # replace 'hr_user' with your HR staff username
        return request.user.is_authenticated and request.user.username == 'hr_user'

class VacancyApplicationViewSet(viewsets.ModelViewSet):
    queryset = VacancyApplication.objects.all().order_by('-created_at')
    serializer_class = VacancyApplicationSerializer
    permission_classes = [RolePermission(required_roles=["HR"])]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]  # public submission
        return [IsHRStaff()]  # only HR staff can list/retrieve
