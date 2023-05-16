
from django.urls import path
from rest_framework.routers import DefaultRouter

from ride_app.views.friend import friend_request, confirm_friend_request, friend_requests_received, \
    cancel_friend_request, mutual_friends, get_friends

router = DefaultRouter()
urlpatterns = [
    path('request/', friend_request)
  ,
    path('confirm/<int:friend_request_id>/', confirm_friend_request),
path('cancel/<int:friend_request_id>/',cancel_friend_request),
    path('request_list/',friend_requests_received),
    path('mutual_friends/',mutual_friends),
    path('my_friends/',get_friends)


]