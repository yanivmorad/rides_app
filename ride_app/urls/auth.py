

from django.urls import path
from rest_framework.routers import DefaultRouter


from ride_app.views.auth import Get_user, signup, me

router = DefaultRouter()

router.register('users', Get_user)
urlpatterns = [
    path('signup/', signup),
    path('me/', me),

]

