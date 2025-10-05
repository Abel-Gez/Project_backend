from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer
from accounts.permissions import RolePermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-publishDate')
    serializer_class = PostSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Anyone (public) can view posts
            return [permissions.AllowAny()]
        # Only MARKETING role can create/update/delete
        return [RolePermission(required_roles=["MARKETING"])]
