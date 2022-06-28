from .models import *
from rest_framework import serializers


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        exclude = ('id',)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        exclude = ('id', 'user')

class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        exclude = ('id', 'pereval')

class PerevalSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer()
    user = UsersSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = PerevalAdd
        exclude = ('id',)




