from django.contrib.auth.models import User
from rest_framework import serializers

from ride_app.models import Member, Group


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


class AddToGroupSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

    def create(self, validated_data):
        user = self.context['request'].user
        group = Group.objects.get(id=validated_data['group_id'], member__user=user,)
        member = Member.objects.create(user_id=validated_data['user_id'], group=group)
        return member

    def test_func(self):
        user = self.request.user
        group_id = self.validated_data.get('group_id')
        group = Group.objects.get(id=group_id)
        return group.owner == user

class RemoveFromGroupSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    group_id = serializers.IntegerField()

    def delete(self):
        user = self.context['request'].user
        group = Group.objects.get(id=self.validated_data['group_id'], member__user=user, member__is_owner=True)
        member = Member.objects.filter(user_id=self.validated_data['user_id'], group=group)
        member.delete()

    def test_func(self):
        user = self.request.user
        group_id = self.validated_data.get('group_id')
        group = Group.objects.get(id=group_id)
        return group.owner == user