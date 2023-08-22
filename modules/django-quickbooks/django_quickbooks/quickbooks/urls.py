from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .viewsets import QuickbookViewSet

router = DefaultRouter()
router.register("", QuickbookViewSet, basename="quickbook_service")

urlpatterns = [
    path("", include(router.urls)),
]
