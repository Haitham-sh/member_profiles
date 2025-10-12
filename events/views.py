from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer, EventCreateSerializer
from django.db.models import Q

# Create your views here.
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def event_list_create(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = EventCreateSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save(creator=request.user)
            response_serializer = EventSerializer(event)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_detail(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Event not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_search(request):
    events = Event.objects.all()
    
    search_query = request.GET.get('q', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    event_type = request.GET.get('event_type', '')
    if event_type:
        events = events.filter(event_type=event_type)
    
    serializer = EventSerializer(events, many=True)
    
    return Response({
        'count': events.count(),
        'filters': {
            'search_query': search_query,
            'event_type': event_type,
        },
        'events': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_types(request):
    event_types = [choice[0] for choice in Event.EVENT_TYPES]
    return Response({
        'event_types': event_types
    })