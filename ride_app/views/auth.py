import os
import uuid
import boto3
from django.contrib.auth.models import User
from django.db.models import Q, F, Value
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework import mixins, status
from django.http import JsonResponse
from django.db import transaction
from django.db.models.functions import  Concat

from ride_app.serializer.auth import SignupSerializer, UserSerializer, UserProfileSerializer, UpdateUserSerializer


@api_view(['POST'])
def signup(request):
    signup_serializer = SignupSerializer(data=request.data)
    if signup_serializer.is_valid():
        user = signup_serializer.save()
        user_serializer = UserSerializer(user)

        if 'file' in request.data:
            random_uuid = uuid.uuid1()
            file, ext = os.path.splitext(request.data['file'].name)
            bucket_name = 'ride-app'
            obj_key = f"profile_imgs/{random_uuid}{ext}"

            s3 = boto3.client('s3')
            s3.upload_fileobj(request.data['file'].file, bucket_name, obj_key)

            print(f'Successfully uploaded!')

            url = f"https://{bucket_name}.s3.amazonaws.com/{obj_key}"

            # Update user profile with the URL
            profile = user.profile
            profile.picture_url = url
            profile.save()

            # Retrieve updated user profile data
            profile_serializer = UserProfileSerializer(profile)
            profile_data = profile_serializer.data

            # Merge user and profile data
            data = user_serializer.data
            data.update(profile_data)
        else:
            # No file provided, return only user data
            data = user_serializer.data

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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    user_serializer = UpdateUserSerializer(instance=request.user, data=request.data)
    if user_serializer.is_valid():
        with transaction.atomic():
            user = user_serializer.save()
            user_serializer = UserSerializer(user)

            profile = user.profile

            file = request.data.get('file')
            if file:
                random_uuid = uuid.uuid1()
                _, ext = os.path.splitext(file.name)
                bucket_name = 'ride-app'
                obj_key = f"profile_imgs/{random_uuid}{ext}"

                s3 = boto3.client('s3')
                s3.upload_fileobj(file.file, bucket_name, obj_key)

                url = f"https://{bucket_name}.s3.amazonaws.com/{obj_key}"
                profile.picture_url = url

            profile.address = request.data.get('address', profile.address)
            profile.gender = request.data.get('gender', profile.gender)
            profile.phone_number = request.data.get('phone_number', profile.phone_number)
            profile.save()

            profile_serializer = UserProfileSerializer(profile)
            profile_data = profile_serializer.data

            data = user_serializer.data
            data.update(profile_data)
            print('Data:', data)  # Add debug output statement

            return Response(data=data, status=status.HTTP_200_OK)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def check_email_unique(request):
    email = request.GET.get('email', None)

    # Perform the email uniqueness check in your database
    is_unique = not User.objects.filter(email=email).exists()

    return JsonResponse({'isUnique': is_unique})

@api_view(['GET'])
def search_users(request):
    name = request.GET.get('name', '')
    parts = name.split(' ')
    first_name = parts[0]
    last_name = parts[1] if len(parts) > 1 else ''

    users = User.objects.annotate(
        full_name=Concat('first_name', Value(' '), 'last_name')
    ).filter(
        Q(first_name__istartswith=first_name) |
        Q(last_name__istartswith=first_name) |
        Q(full_name__istartswith=first_name)
    ).order_by(
        F('first_name').desc(nulls_last=True), 'last_name'
    )

    serializer = UserSerializer(users, many=True)
    serialized_data = serializer.data
    return Response(serialized_data)
class UserDetail(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
