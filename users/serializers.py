from rest_framework import serializers
from .models import User
from rest_framework.parsers import MultiPartParser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'profile_picture', 'bio']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = User.objects.filter(email=email).first()
            if user:
                if user.email == email and user.check_password(password):
                    data['user'] = user
                    return data
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Invalid email or password.')
        else:
            raise serializers.ValidationError('Must include email and password.')
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    created_events_count = serializers.SerializerMethodField()
    joined_events_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'profile_picture', 'bio', 
            'date_joined', 'created_events_count', 'joined_events_count'
        ]
        read_only_fields = ['id', 'date_joined']

    def get_created_events_count(self, obj):
        return obj.event_set.count()

    def get_joined_events_count(self, obj):
        return obj.eventmember_set.count()
    

class ProfilePictureSerializer(serializers.Serializer):
    profile_picture = serializers.ImageField()
    parser_classes = [MultiPartParser]
