from rest_framework import serializers
# from .models import RegisteredUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .models import Event, EventDate, Enrollment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','first_name', 'last_name', 'email')


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['first_name'] + validated_data['last_name'],  # Assuming email is used as username
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True,write_only=True)



# Serializer for Event
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'venue')


# Serializer for EventDate
class EventDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDate
        fields = ('id', 'event', 'date', 'time')

class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Enrollment
        fields = ('user', 'event', 'enrolled_on')

    def create(self, validated_data):
        user = validated_data['user']
        event = validated_data['event']

        # Prevent duplicate enrollments
        if Enrollment.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("User is already enrolled in this event.")
        
        return super().create(validated_data)

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

