from rest_framework import serializers
from .models import Event, User

class EventUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
        
class EventSerializer(serializers.ModelSerializer):
    organizer_username = serializers.CharField(source='organizer.username', read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'organizer_username', 'name', 'description', 'date', 'venue', 'price', 'created_at', 'updated_at', 'status')

class EventDetailSerializer(serializers.ModelSerializer):
  organizer = EventUserSerializer(read_only=True)

  class Meta:
    model = Event
    fields = ('id', 'organizer', 'name', 'description', 'date', 'venue', 'price', 'created_at', 'updated_at', 'status')

class EventStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('status',)
