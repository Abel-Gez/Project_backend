# vacancy/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VacancyViewSet, VacancyApplicationViewSet
from rest_framework_nested import routers


router = DefaultRouter()
router.register(r'vacancies', VacancyViewSet, basename='vacancy')
vacancy_router = routers.NestedDefaultRouter(router, r'vacancies', lookup='vacancy')
# Nested router for applications under a vacancy
router.register(r'applications', VacancyApplicationViewSet, basename='vacancyapplication')

urlpatterns = [
    path('', include(router.urls)),
     path('', include(vacancy_router.urls)),
]
