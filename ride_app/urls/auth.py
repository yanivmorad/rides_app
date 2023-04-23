

from django.urls import path
from rest_framework.routers import DefaultRouter


from ride_app.views.auth import Get_user, signup, me, update_user, UserDetail

router = DefaultRouter()

router.register('users', Get_user)
urlpatterns = [
    path('signup/', signup),
    path('me/', me),
    path('update_user/', update_user),
path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),

]

