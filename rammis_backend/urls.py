from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),  # auth API
    path("api/v1/", include("comments.urls")),  # <--- contact form API
     path("api/v1/", include("blog.urls")),   # -> /api/v1/posts/
     path("api/v1/", include("blog.urls")),      # blog API
     path("api/v1/", include("currency.urls")),
     path("api/v1/", include("bank_account.urls")),
     path('api/vacancy/', include('vacancy.urls')),     # HR vacancy app



]

