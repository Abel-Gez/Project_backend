from django.urls import path
from .views import (
    CookieTokenObtainPairView,  
    CookieTokenRefreshView,
    LogoutView,
    StaffCreateView,
)

urlpatterns = [
    # JWT login (sets HttpOnly refresh cookie + returns access)
    path('jwt/login/', CookieTokenObtainPairView.as_view(), name='jwt-login'),

    # Refresh access token using HttpOnly cookie
    path('jwt/refresh/', CookieTokenRefreshView.as_view(), name='jwt-refresh'),

    # Logout (clears refresh cookie)
    path('logout/', LogoutView.as_view(), name='logout'),

    # Staff creation endpoint
    path('staff/create/', StaffCreateView.as_view(), name='staff-create'),
]
