from rest_framework import serializers
from .models import EventMember
from users.serializers import UserProfileSerializer
from events.serializers import EventSerializer

class EventMemberSerializer(serializers.ModelSerializer):
    user_info = UserProfileSerializer(source='user', read_only=True)
    event_info = EventSerializer(source='event', read_only=True)
    
    class Meta:
        model = EventMember
        fields = [
            'id', 'user', 'user_info', 'event', 'event_info',
            'role', 'bio', 'specialization', 'join_date'
        ]
        read_only_fields = ['id', 'user', 'event', 'join_date']

class JoinEventSerializer(serializers.Serializer):
    event_password = serializers.CharField(write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    specialization = serializers.CharField(required=False, allow_blank=True)