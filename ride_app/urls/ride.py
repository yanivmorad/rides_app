

from django.urls import path
from rest_framework.routers import DefaultRouter

from ride_app.views.ride import RidesViewSet

router = DefaultRouter()
router.register('', RidesViewSet)

urlpatterns = []

urlpatterns.extend(router.urls)
