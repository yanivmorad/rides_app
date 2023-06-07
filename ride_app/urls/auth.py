

from django.urls import path
from rest_framework.routers import DefaultRouter


from ride_app.views.auth import Get_user, signup, me, update_user, UserDetail, check_email_unique, search_users

router = DefaultRouter()

router.register('users', Get_user)
urlpatterns = [
    path('signup/', signup),
    path('me/', me),
    path('update_user/', update_user),
path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('search_users/',search_users),
    path('check-email-unique/', check_email_unique, name='check_email_unique'),

]

