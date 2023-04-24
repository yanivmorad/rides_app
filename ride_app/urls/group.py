from django.urls import path
from rest_framework.routers import DefaultRouter

from ride_app.views.group import  leave_or_remove_from_group

from ride_app.views.group import create_group, add_to_group


router = DefaultRouter()
urlpatterns = [
    path('create/', create_group),
    path('add/', add_to_group),
    path('remove_member/', leave_or_remove_from_group),

]



