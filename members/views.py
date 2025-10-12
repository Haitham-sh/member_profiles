from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EventMember
from events.models import Event
from users.models import User
from .serializers import EventMemberSerializer, JoinEventSerializer, ChangeRoleSerializer

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'POST':
        serializer = JoinEventSerializer(data=request.data)
        if serializer.is_valid():
            if event.event_password != serializer.validated_data['event_password']:
                return Response(
                    {'error': 'Invalid event password'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            if EventMember.objects.filter(user=request.user, event=event).exists():
                return Response(
                    {'error': 'You have already joined this event'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            event_member = EventMember.objects.create(
                user=request.user,
                event=event,
                bio=serializer.validated_data.get('bio', ''),
                specialization=serializer.validated_data.get('specialization', ''),
                role='participant'
            )
            return Response(
                EventMemberSerializer(event_member).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_members(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    is_member = EventMember.objects.filter(user=request.user, event=event).exists()
    is_organizer = event.creator == request.user
    if not (is_member or is_organizer):
        return Response(
            {'error': 'You are not a member of this event'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    members = EventMember.objects.filter(event=event)
    serializer = EventMemberSerializer(members, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def change_member_role(request, event_id, member_id):
    try:
        event = Event.objects.get(id=event_id)
        user = User.objects.get(id=member_id)
        event_member = EventMember.objects.get(user=user, event=event)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except EventMember.DoesNotExist:
        return Response(
            {'error': 'Member not found in this event'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    if event.creator != request.user:
        return Response(
            {'error': 'Only event organizer can change roles'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    serializer = ChangeRoleSerializer(data=request.data)
    if serializer.is_valid():
        new_role = serializer.validated_data['new_role']
        event_member.role = new_role
        event_member.save()
        return Response({
            'message': f'Role changed to {new_role} successfully',
            'member': {
                'id': event_member.id,
                'user_name': user.username,
                'event_title': event.title,
                'new_role': event_member.role
            }
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
