
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework import mixins, status

from ride_app.serializer.auth import SignupSerializer, UserSerializer, UserProfileSerializer, UpdateUserSerializer


@api_view(['POST'])
def signup(request):
    signup_serializer = SignupSerializer(data=request.data)
    if signup_serializer.is_valid():
        user = signup_serializer.save()
        user_serializer = UserSerializer(user)

        # Retrieve user profile data
        profile_serializer = UserProfileSerializer(user.profile)
        profile_data = profile_serializer.data

        # Merge user and profile data
        data = user_serializer.data
        data.update(profile_data)

        return Response(data=data, status=status.HTTP_201_CREATED)
    else:
        return Response(signup_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Get_user(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    # you will get here only if the user is already authenticated!
    user_serializer = UserSerializer(instance=request.user, many=False)
    return Response(data=user_serializer.data)
@api_view(['PUT','PATCH' ])
@permission_classes([IsAuthenticated])
def update_user(request):
    user_serializer = UpdateUserSerializer(instance=request.user, data=request.data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        user_serializer = UserSerializer(user)

        # Retrieve user profile data
        profile_serializer = UserProfileSerializer(user.profile)
        profile_data = profile_serializer.data

        # Merge user and profile data
        data = user_serializer.data
        data.update(profile_data)

        return Response(data=data, status=status.HTTP_201_CREATED)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
