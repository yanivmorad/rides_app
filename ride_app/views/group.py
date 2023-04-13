from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Group
from ..serializer.group import CreateGroupSerializer, GroupSerializer, AddToGroupSerializer, RemoveFromGroupSerializer, \
    MemberSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    serializer = CreateGroupSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        group = serializer.save()
        group_serializer = GroupSerializer(group)
        return Response(group_serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def add_to_group(request):
    serializer = AddToGroupSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        member = serializer.save()
        member_serializer = MemberSerializer(member)
        return Response(member_serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])

def remove_from_group(request, group_id, user_id):
    serializer = RemoveFromGroupSerializer(data={'group_id': group_id, 'user_id': user_id}, context={'request': request})
    if serializer.is_valid():
        serializer.delete()
        return Response(status=204)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
@login_required
def list_groups(request):
    groups = Group.objects.filter(member__user=request.user)
    serializer = GroupSerializer(groups, many=True)
    return Response(serializer.data, status=200)
