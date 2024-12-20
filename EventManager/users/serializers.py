from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'role')  
        extra_kwargs = {
            'password': {'write_only': True}, 
        }

    def create(self, validated_data):

        role = validated_data.pop('role', 'participant')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.role = role
        user.save()
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 
