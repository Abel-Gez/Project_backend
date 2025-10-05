from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountApplicationViewSet, BranchViewSet

router = DefaultRouter()
router.register(r'accounts', AccountApplicationViewSet, basename='account')
router.register(r'branches', BranchViewSet, basename='branch')

urlpatterns = [
    path('', include(router.urls)),
]
