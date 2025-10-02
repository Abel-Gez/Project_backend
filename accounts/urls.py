from django.urls import path
from .views import  CustomTokenObtainPairView, StaffCreateView

urlpatterns = [
    # Existing non-JWT login (optional)
    # path('login/', LoginView.as_view(), name='staff-login'),

    # JWT login endpoint
    path('jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt-login'),

     #Staff creation endpoint
    path('staff/create/', StaffCreateView.as_view(), name='staff-create'),
]
