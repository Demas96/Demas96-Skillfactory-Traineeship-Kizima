from .models import *
from rest_framework import serializers

class PerevalSerializer(serializers.Serializer):
    class Meta:
        model = PerevalAdd
        fields = (
            'status',
            'coords',
            'beautyTitle',
            'title',
            'other_titles',
            'connect',
            'add_time',
            'level_winter',
            'level_summer',
            'level_autumn',
            'level_spring',
        )