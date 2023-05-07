
from django.urls import path
from rest_framework.routers import DefaultRouter

from ride_app.views.friend import friend_request, confirm_friend_request

router = DefaultRouter()
urlpatterns = [
    path('request/', friend_request)
  ,
    path('confirm/<int:friend_request_id>/', confirm_friend_request)
    ,


]