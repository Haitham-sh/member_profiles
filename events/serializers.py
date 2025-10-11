from rest_framework import serializers
from .models import Event

class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 
            'event_password', 'event_date'
        ]

class EventSerializer(serializers.ModelSerializer):
    creator_name = serializers.CharField(source='creator.username', read_only=True)
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type', 
            'creator', 'creator_name', 'event_date', 'created_at'
        ]
        read_only_fields = ['creator']