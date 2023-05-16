from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ride_app.models import FriendRequest, Friends
from ride_app.serializer.auth import UserSerializer
from ride_app.serializer.friend import FriendRequestSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def friend_request(request):
    data = request.data.copy()
    data['from_user'] = request.user.id
    serializer = FriendRequestSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        serializer.save(from_user=request.user)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_friend_request(request, friend_request_id):
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request does not exist'}, status=404)
    if friend_request.status != 'pending':
        return Response({'error': 'Friend request has already been confirmed or denied'}, status=400)
    friend_request.status = 'approved'
    friend_request.save()
    Friends.objects.create(user1=friend_request.from_user, user2=friend_request.to_user)
    return Response({'success': 'Friend request confirmed'}, status=200)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_friend_request(request, friend_request_id):
    try:
        friend_request = FriendRequest.objects.get(id=friend_request_id, to_user=request.user)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Friend request does not exist'}, status=404)
    if friend_request.status != 'pending':
        return Response({'error': 'Friend request has already been confirmed or denied'}, status=400)
    friend_request.status = 'cancelled'
    friend_request.save()
    return Response({'success': 'Friend request cancelled'}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests_received(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    serializer = FriendRequestSerializer(friend_requests, many=True)
    return Response(serializer.data, status=200)


from django.db.models import Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mutual_friends(request):
    user1_id = request.user.id
    user2_id = request.query_params.get('user2')

    user1 = get_object_or_404(User, id=user1_id)
    user2 = get_object_or_404(User, id=user2_id)

    friends1 = Friends.objects.filter(Q(user1=user1) | Q(user2=user1))
    friends2 = Friends.objects.filter(Q(user1=user2) | Q(user2=user2))

    friends1_user_ids = set(friends1.values_list('user1_id', flat=True)) | set(friends1.values_list('user2_id', flat=True))
    friends2_user_ids = set(friends2.values_list('user1_id', flat=True)) | set(friends2.values_list('user2_id', flat=True))

    mutual_friends = friends1_user_ids.intersection(friends2_user_ids)

    # Exclude user1 and user2 from mutual friends
    mutual_friends.discard(user1.id)
    mutual_friends.discard(user2.id)

    mutual_friends = User.objects.filter(id__in=mutual_friends)

    serializer = UserSerializer(mutual_friends, many=True)
    return Response(serializer.data)
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friends(request):
    user_id = request.user.id
    user = get_object_or_404(User, id=user_id)

    friends1 = Friends.objects.filter(user1=user)
    friends2 = Friends.objects.filter(user2=user)

    friend_user_ids = set(friends1.values_list('user2_id', flat=True)) | set(friends2.values_list('user1_id', flat=True))

    friends = User.objects.filter(id__in=friend_user_ids)

    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)
