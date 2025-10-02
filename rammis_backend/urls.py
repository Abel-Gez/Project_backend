from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # All authentication/account related endpoints
    path('api/auth/', include('accounts.urls')),
]
