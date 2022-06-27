from .models import *
from rest_framework import serializers

class PerevalSerializer(serializers.Serializer):
    status = serializers.CharField(max_length=10)
    coords = serializers.CharField()
    beautyTitle = serializers.CharField(max_length=255)
    title = serializers.CharField(max_length=255)
    other_titles = serializers.CharField(max_length=255)
    connect = serializers.CharField()
    add_time = serializers.DateTimeField()
    level_winter = serializers.CharField(max_length=255)
    level_summer = serializers.CharField(max_length=255)
    level_autumn = serializers.CharField(max_length=255)
    level_spring = serializers.CharField(max_length=255)
    user = serializers.CharField()

def encode():
    m