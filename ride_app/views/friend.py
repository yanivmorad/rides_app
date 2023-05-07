

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ride_app.models import FriendRequest, Friends
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

