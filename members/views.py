from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import EventMember
from events.models import Event
from .serializers import EventMemberSerializer, JoinEventSerializer

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
        members = EventMember.objects.filter(event=event)
        serializer = EventMemberSerializer(members, many=True)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
