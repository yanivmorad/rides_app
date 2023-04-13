from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ride_app.models import Member, Group, UserProfile


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'


class CreateGroupSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Group
        fields = ('name', 'description', 'owner')

    def create(self, validated_data):
        group = Group.objects.create(**validated_data)
        Member.objects.create(user=self.context['request'].user, group=group)
        return group
from rest_framework import serializers
from ride_app.models import Member, Group

class AddToGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ('user', 'group')

    def validate(self, data):
        group = data['group']
        user = data['user']

        # check if user is already a member of the group
        if Member.objects.filter(user=user, group=group).exists():
            raise serializers.ValidationError('User is already a member of this group.')

        # check if user is the owner of the group
        if group.owner == user:
            raise serializers.ValidationError('Owner is already a member of this group.')
        return data

    def create(self, validated_data):
        member = Member.objects.create(**validated_data)
        return member


