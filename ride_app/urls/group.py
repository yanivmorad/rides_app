from django.urls import path
from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from ride_app.views.group import create_group, add_to_group, leave_or_remove_from_group
=======
from ride_app.views.group import create_group, add_to_group
>>>>>>> origin/main

router = DefaultRouter()
urlpatterns = [
    path('create/', create_group),
    path('add/', add_to_group),
<<<<<<< HEAD
    path('remove_member/', leave_or_remove_from_group),

]
=======

]
>>>>>>> origin/main
