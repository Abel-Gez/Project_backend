from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.permissions import IsAdminUserRole

from .serializers import (
    LoginSerializer,
    StaffSerializer,
    StaffCreateSerializer,
    CustomTokenObtainPairSerializer,
)
from .models import StaffUser


# # Optional: existing login view (non-JWT)
# class LoginView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.validated_data['user']
#             login(request, user)
#             return Response({
#                 "message": "Login successful",
#                 "user": StaffSerializer(user).data
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# JWT Login view using custom serializer
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer


# Only ADNINS can create staffs
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

