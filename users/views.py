from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated
from events.models import Event
from members.models import EventMember
from rest_framework.parsers import MultiPartParser, FormParser
from users.serializers import UserProfileSerializer, ProfilePictureSerializer
from rest_framework.views import APIView

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_events_overview(request):
    user = request.user
    created_events = Event.objects.filter(creator=user)
    joined_events = EventMember.objects.filter(member=user)
    created_events_count = created_events.count()
    joined_events_count = joined_events.count()
    return Response({
    
})

# Create your views here.
@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User created successfully'}, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Profile updated successfully',
                'user': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_auth(request):
    return Response({
        'message': 'User is authenticated',
        'user': {
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email
        }
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_events_overview(request):
    user = request.user
    created_events = Event.objects.filter(creator=user).order_by('-created_at')[:5]
    joined_events_memberships = EventMember.objects.filter(
        user=user
    ).select_related('event').order_by('-join_date')[:5]

    created_events_data = []
    for event in created_events:
        created_events_data.append({
            'id': event.id,
            'title': event.title,
            'event_type': event.event_type,
            'event_date': event.event_date,
            'member_count': event.eventmember_set.count(),
            'role': 'organizer'
        })
    
    joined_events_data = []
    for membership in joined_events_memberships:
        joined_events_data.append({
            'id': membership.event.id,
            'title': membership.event.title,
            'event_type': membership.event.event_type,
            'event_date': membership.event.event_date,
            'member_count': membership.event.eventmember_set.count(),
            'role': membership.role,
            'join_date': membership.join_date
        })
    
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'created_events_count': user.event_set.count(),
            'joined_events_count': user.eventmember_set.count()
        },
        'recent_created_events': created_events_data,
        'recent_joined_events': joined_events_data
    })

class UploadProfilePictureView(APIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ProfilePictureSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.profile_picture = serializer.validated_data['profile_picture']
            user.save()
            return Response({
                'message': 'Profile picture uploaded successfully'
})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_picture(request):
    if request.method == 'DELETE':
        user = request.user
        if user.profile_picture:
            user.profile_picture.delete(save=False)
            user.profile_picture = None
            user.save()
            
            return Response({
                'message': 'Profile picture deleted successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': 'No profile picture to delete'
            }, status=status.HTTP_400_BAD_REQUEST)
