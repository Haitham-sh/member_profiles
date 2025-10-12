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
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type', 
            'event_password', 'creator', 'creator_name',
            'event_date', 'created_at', 'member_count'
        ]
        extra_kwargs = {
            'creator': {'read_only': True},
            'event_password': {'write_only': True}
        }
    
    def get_member_count(self, obj):
        return obj.eventmember_set.count()