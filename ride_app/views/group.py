from django.contrib.auth.decorators import login_required
<<<<<<< HEAD
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import permissions, status

from ..models import Group, Member
from ..serializer.group import CreateGroupSerializer, GroupSerializer, AddToGroupSerializer
=======
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Group
from ..serializer.group import CreateGroupSerializer, GroupSerializer, AddToGroupSerializer, RemoveFromGroupSerializer, \
    MemberSerializer
>>>>>>> origin/main


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_group(request):
    serializer = CreateGroupSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        group = serializer.save()
        group_serializer = GroupSerializer(group)
        return Response(group_serializer.data, status=201)
    return Response(serializer.errors, status=400)

<<<<<<< HEAD

class IsGroupAdminOrOwner(permissions.BasePermission):
    message = 'You must be the group owner or an admin to add members to the group.'

    def has_permission(self, request, view):
        group_id = request.data.get('group')
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response({'detail': f'The group with ID {group_id} does not exist.'}, status=404)

        # Check if the user who sent the request is the same user who manages the group
        if not request.user == group.owner:
            return False

        return True


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsGroupAdminOrOwner])
def add_to_group(request):
    serializer = AddToGroupSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_or_remove_from_group(request):
    '''There is a problem!! When a manager leaves the group, there is no change of manager for the group'''
    group_id = request.data.get('group_id')
    if request.data.get('user_id'):
         user = request.data.get('user_id')
    else:
        user = request.user

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'detail': f'The group with ID {group_id} does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        member = Member.objects.get(user=user, group=group)
    except Member.DoesNotExist:
        return Response({'detail': f'The user is not a member of the group.'}, status=status.HTTP_400_BAD_REQUEST)

    if user == group.owner:
        # Check if there are other members in the group
        other_members = Member.objects.filter(group=group).exclude(user=user)
        if other_members.exists():
            # Choose a new owner from the other members
            new_owner = other_members.first().user
            group.owner = new_owner
            group.save()
        else:
            # If there are no other members, delete the groupv
            group.delete()
            return Response({'detail': f'The owner left the group, so the group was deleted.'},
                            status=status.HTTP_204_NO_CONTENT)

    # Remove the member from the group
    member.delete()

    return Response({'detail': f'The user has left the group.'}, status=status.HTTP_204_NO_CONTENT)
=======
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
>>>>>>> origin/main
