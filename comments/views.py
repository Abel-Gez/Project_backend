from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from accounts.permissions import RolePermission

class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    - create (POST): anyone can submit a message/comment
    - list/retrieve/update/delete: only staff with MARKETING role can access
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def get_permissions(self):
        # POST is public
        if self.action == 'create':
            return [permissions.AllowAny()]
        # Other actions: only MARKETING role
        return [RolePermission(required_roles=["MARKETING"])]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == "MARKETING":
            return super().get_queryset()
        return super().get_queryset().none()
