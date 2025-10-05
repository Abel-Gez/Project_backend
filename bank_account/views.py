from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import AccountApplication, Branch, BranchManagerProfile
from .serializers import AccountApplicationSerializer, BranchSerializer

class IsBranchManager(permissions.BasePermission):
    """
    Allow access only if user is authenticated and has a branch_profile with is_branch_manager True.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        profile = getattr(user, 'branch_profile', None)
        return bool(profile and profile.is_branch_manager and profile.branch is not None)

class AccountApplicationViewSet(viewsets.ModelViewSet):
    """
    - create (POST): public (AllowAny) — frontend submits application
    - list (GET): authenticated branch managers see only their branch submissions;
                staff/superuser see all.
    - retrieve/update/destroy: restricted (IsAuthenticated for retrieve; further permission required for modifications)
    """
    queryset = AccountApplication.objects.all().select_related('branch')
    serializer_class = AccountApplicationSerializer

    def get_permissions(self):
        # create is public; all other actions require authentication
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        # if anonymous or creating, don't filter (create uses POST with AllowAny)
        if not user or not user.is_authenticated:
            return AccountApplication.objects.none()  # no list access for anonymous
        # superusers and staff can see all
        if user.is_superuser or user.is_staff:
            return super().get_queryset()
        # branch managers — only accounts for their branch
        profile = getattr(user, 'branch_profile', None)
        if profile and profile.is_branch_manager and profile.branch:
            return super().get_queryset().filter(branch=profile.branch)
        # other authenticated users: return none
        return AccountApplication.objects.none()

class BranchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Branch.objects.all().order_by('name')
    serializer_class = BranchSerializer
    permission_classes = [AllowAny]  # branch list is safe to be public for dropdowns
