from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator

from ride_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('picture_url', 'address', 'gender')


class SignupSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'profile')

    email = serializers.EmailField(
        write_only=True,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, allow_null=False, allow_blank=False)
    first_name = serializers.CharField(write_only=True, required=True, allow_blank=False, allow_null=False)
    last_name = serializers.CharField(write_only=True, required=True, allow_blank=False, allow_null=False)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)

        user = User.objects.create(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])
        user.save()
        print(profile_data)
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'picture_url': profile_data.get('picture_url', ''),
                    'address': profile_data.get('address', ''),
                    'gender': profile_data.get('gender', ''),
                }
            )
            if not created:
                profile.picture_url = profile_data.get('picture_url', '')
                profile.address = profile_data.get('address', '')
                profile.gender = profile_data.get('gender', '')
                profile.save()
            user.profile = profile
            user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    picture_url = serializers.CharField(source='profile.picture_url')
    address = serializers.CharField(source='profile.address')
    gender = serializers.CharField(source='profile.gender')
    phone_number = serializers.CharField(source='profile.phone_number')

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'picture_url', 'address', 'gender','phone_number')



class UpdateUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ( 'email', 'first_name', 'last_name', 'profile')


    email = serializers.EmailField(
        write_only=True,
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        if profile_data:
            profile, created = UserProfile.objects.get_or_create(
                user=instance,
                defaults={
                    'picture_url': profile_data.get('picture_url', instance.profile.picture_url),
                    'address': profile_data.get('address', instance.profile.address),
                    'gender': profile_data.get('gender', instance.profile.gender),
                }
            )
            if not created:
                profile.picture_url = profile_data.get('picture_url', instance.profile.picture_url)
                profile.address = profile_data.get('address', instance.profile.address)
                profile.gender = profile_data.get('gender', instance.profile.gender)
                profile.save()
            instance.profile = profile

        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
