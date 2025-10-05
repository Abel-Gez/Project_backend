# accounts/views.py
from datetime import timedelta
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdminUserRole
from .serializers import StaffSerializer, StaffCreateSerializer, CustomTokenObtainPairSerializer
from .models import StaffUser


# --- JWT Login: sets refresh token as HttpOnly cookie, returns access token in body
class CookieTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh = response.data.get("refresh")
            response.data.pop("refresh", None)  # remove from body

            lifetime = getattr(settings, "SIMPLE_JWT", {}).get("REFRESH_TOKEN_LIFETIME", timedelta(days=7))
            max_age = int(lifetime.total_seconds())
            secure_flag = not getattr(settings, "DEBUG", False) # Secure in production

            # Set HttpOnly refresh cookie
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=secure_flag,
                # samesite="Lax",
                samesite=None,
                max_age=max_age,
                path="/api/auth/",
            )

        return response


# --- Refresh endpoint reads HttpOnly cookie, rotates if configured
class CookieTokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

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
        new_refresh = serializer.validated_data.get("refresh")  # only if ROTATE_REFRESH_TOKENS=True

        response = Response({"access": access}, status=status.HTTP_200_OK)

        # If rotation is enabled, update HttpOnly refresh cookie
        if new_refresh:
            lifetime = getattr(settings, "SIMPLE_JWT", {}).get("REFRESH_TOKEN_LIFETIME", timedelta(days=7))
            max_age = int(lifetime.total_seconds())
            secure_flag = not getattr(settings, "DEBUG", False) # Secure in production

            response.set_cookie(
                key="refresh_token",
                value=new_refresh,
                httponly=True,
                secure=secure_flag,
                # samesite="Lax",
                samesite=None,
                max_age=max_age,
                path="/api/auth/",
            )

        return response


# --- Logout endpoint: deletes refresh cookie and optionally blacklists
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token", path="/api/auth/")
        return response


# --- ADMIN only: create staff accounts
class StaffCreateView(generics.CreateAPIView):
    queryset = StaffUser.objects.all()
    serializer_class = StaffCreateSerializer
    permission_classes = [IsAdminUserRole]

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


# --- Current user profile: used by frontend ProtectedRoute
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = StaffSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
