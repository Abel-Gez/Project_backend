# vacancy/urls.py (MODIFIED)

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacancyApplicationViewSet

router = DefaultRouter()
# The router creates paths like 'applications/' and 'applications/{pk}/'
router.register(r'applications', VacancyApplicationViewSet, basename='vacancyapplication')

urlpatterns = [
    # CHANGE: Remove the redundant path('api/', include(router.urls))
    path('', include(router.urls)), 
]