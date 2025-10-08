from requests import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from .models import Vacancy, VacancyApplication
from .serializers import VacancySerializer, VacancyApplicationSerializer
from accounts.permissions import RolePermission


class VacancyViewSet(viewsets.ModelViewSet):
    queryset = Vacancy.objects.all().order_by('-posted_at')
    serializer_class = VacancySerializer
    permission_classes = [RolePermission]
    required_roles = ["HR", "SUPERADMIN"]

    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """
        Return all applications for a specific vacancy.
        URL: /vacancies/<id>/applications/
        """
        vacancy = self.get_object()
        applications = VacancyApplication.objects.filter(position_applied=vacancy.title)
        serializer = VacancyApplicationSerializer(applications, many=True)
        return Response(serializer.data)

# class VacancyApplicationViewSet(viewsets.ModelViewSet):
#     """
#     Public can create applications.
#     HR can view/delete applications.
#     """
#     queryset = VacancyApplication.objects.all().order_by('-created_at')
#     serializer_class = VacancyApplicationSerializer

#     def get_permissions(self):
#         if self.action == 'create':
#             return [permissions.AllowAny()]  # public submission
#         # For all other actions, use RolePermission
#         return [RolePermission()]
    
#     # ✅ add required_roles as class attribute
#     required_roles = ["HR"]

class VacancyApplicationViewSet(viewsets.ModelViewSet):
    """
    Public can create applications.
    HR can view/delete applications.
    """
    queryset = VacancyApplication.objects.all().order_by('-created_at')
    serializer_class = VacancyApplicationSerializer
    required_roles = ["HR"]

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]  # public submission
        return [RolePermission()]

    def get_queryset(self):
        vacancy_id = self.kwargs.get('vacancy_pk') or self.request.query_params.get('vacancy')
        if vacancy_id:
            return VacancyApplication.objects.filter(vacancy_id=vacancy_id).order_by('-created_at')
        return VacancyApplication.objects.all().order_by('-created_at')
