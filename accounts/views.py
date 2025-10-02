# accounts/views.py
from datetime import timedelta
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from accounts.permissions import IsAdminUserRole

from .serializers import (
    StaffSerializer,
    StaffCreateSerializer,
    CustomTokenObtainPairSerializer,
)
from .models import StaffUser


# JWT Login that sets refresh token as HttpOnly cookie and returns access in body
class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    # Optionally exempt CSRF for token endpoint (see notes below)
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # Let the parent handle validation and token creation
        response = super().post(request, *args, **kwargs)

        # On success, parent sets response.data with access and refresh
        if response.status_code == 200:
            refresh = response.data.get("refresh")
            # remove refresh from response body so JS can't read it
            response.data.pop("refresh", None)

            # derive cookie lifetime from settings.SIMPLE_JWT or default 7 days
            lifetime = getattr(settings, "SIMPLE_JWT", {}).get("REFRESH_TOKEN_LIFETIME")
            if lifetime is None:
                lifetime = timedelta(days=7)
            max_age = int(lifetime.total_seconds())

            secure_flag = not getattr(settings, "DEBUG", True)

            # set the refresh token cookie (HttpOnly)
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=secure_flag,
                samesite="Lax",
                max_age=max_age,
                path="/api/auth/",
            )

        return response


# Refresh endpoint that reads refresh token from HttpOnly cookie
class CookieTokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    # If you implement CSRF protection, remove csrf_exempt and handle accordingly
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh_token")
        if not refresh:
            return Response({"detail": "No refresh token cookie"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TokenRefreshSerializer(data={"refresh": refresh})
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

        access = serializer.validated_data.get("access")
        return Response({"access": access}, status=status.HTTP_200_OK)


# Logout endpoint deletes the refresh cookie (and can blacklist if you enable blacklisting)
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Optionally blacklist request.auth here if using token_blacklist
        response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token", path="/api/auth/")
        return response


# Only ADMINS can create staffs
class StaffCreateView(generics.CreateAPIView):
    queryset = StaffUser.objects.all()
    serializer_class = StaffCreateSerializer
    permission_classes = [IsAdminUserRole]  # only ADMINs can create staff

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            staff = serializer.save()
            return Response(
                {
                    "message": "Staff account created successfully",
                    "staff": StaffSerializer(staff).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
