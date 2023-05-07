from rest_framework import serializers

from ride_app.models import FriendRequest, Friends


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = "__all__"

    def validate_to_user(self, data):
        to_user = data
        from_user = self.context['request'].user
        if Friends.objects.filter(user1=from_user, user2=to_user).exists() or Friends.objects.filter(user1=to_user,
                                                                                                     user2=from_user).exists():
            raise serializers.ValidationError("You are already friends.")

        return data

    def create(self, validated_data):
        validated_data['from_user'] = self.context['request'].user
        friend_request = FriendRequest.objects.create(**validated_data)
        return friend_request