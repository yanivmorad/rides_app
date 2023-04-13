from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator

from ride_app.models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver


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

        if profile_data:
            profile = UserProfile.objects.create(
                user=user,
                picture_url=profile_data.get('picture_url', ''),
                address=profile_data.get('address', ''),
                gender=profile_data.get('gender', ''),
            )
            profile.save()
            user.profile = profile
            user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'profile')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        UserProfile.objects.create(user=instance)
