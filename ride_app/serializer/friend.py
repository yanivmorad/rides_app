from django.contrib.auth.models import User
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
        from_user = self.context['request'].user
        to_user = validated_data['to_user']

        # Check if there is an existing friend request in the opposite direction
        try:
            reverse_friend_request = FriendRequest.objects.get(from_user=to_user, to_user=from_user)
            if reverse_friend_request.status == 'pending':
                # Approve the reverse friend request
                reverse_friend_request.status = 'approved'
                reverse_friend_request.save()

                # Create new Friends object
                Friends.objects.create(user1=from_user, user2=to_user)

                # Return the updated friend request
                return reverse_friend_request
            else:
                # A friend request already exists in the opposite direction and it's not pending.
                # Return an error response indicating that the request cannot be processed.
                raise serializers.ValidationError("Friend request already exists.")

        except FriendRequest.DoesNotExist:
            pass

        # Check if the users are already friends
        if Friends.objects.filter(user1=from_user, user2=to_user).exists() or Friends.objects.filter(user1=to_user,
                                                                                                     user2=from_user).exists():
            raise serializers.ValidationError("You are already friends.")

        # Check if the from_user and to_user are the same
        if from_user == to_user:
            raise serializers.ValidationError("You are the same person.")

        # Create a new friend request
        validated_data['from_user'] = from_user
        friend_request = FriendRequest.objects.create(**validated_data)
        return friend_request
