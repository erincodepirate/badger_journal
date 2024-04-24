from rest_framework import serializers
from .models import Entry
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class EntrySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Entry 
        fields = ('id', 'title', 'text', 'date', 'user')