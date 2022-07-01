from drf_yasg.utils import swagger_serializer_method

from .models import *
from rest_framework import serializers


class CoordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coords
        exclude = ('id',)


class LevelSerialize(serializers.Serializer):
    winter = serializers.CharField(allow_blank=True)
    summer = serializers.CharField(allow_blank=True)
    autumn = serializers.CharField(allow_blank=True)
    spring = serializers.CharField(allow_blank=True)


class UsersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='firstname')
    fam = serializers.CharField(source='lastname')
    otc = serializers.CharField(source='patronymic')
    email = serializers.CharField()

    class Meta:
        model = Users
        fields = ('email', 'fam', 'name', 'otc', 'phone',)
        # exclude = ('id', 'user')


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        exclude = ('id', 'pereval')


class PerevalDetailSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer()
    user = UsersSerializer()
    images = ImagesSerializer(many=True)

    class Meta:
        model = PerevalAdd
        fields = '__all__'


class PerevalSerializer(serializers.ModelSerializer):
    coords = CoordsSerializer()
    user = UsersSerializer()
    images = ImagesSerializer(many=True)
    level = LevelSerialize()

    class Meta:
        model = PerevalAdd
        exclude = ('id', 'status')

    def create(self, validated_data):
        user = validated_data['user']
        coords = validated_data['coords']
        level = validated_data['level']
        images = validated_data['images']
        if Users.objects.filter(email=user['email']).exists():
            Users.objects.filter(email=user['email']).update(firstname=user['firstname'],
                                                             lastname=user['lastname'], patronymic=user['patronymic'],
                                                             phone=user['phone'])
            uss = Users.objects.get(email=user['email'])
        else:
            us = User.objects.create(username=user['email'])
            uss = Users.objects.create(user=us, email=user['email'], firstname=user['firstname'],
                                       lastname=user['lastname'], patronymic=user['patronymic'],
                                       phone=user['phone'])

        co = Coords.objects.create(latitude=coords['latitude'], longitude=coords['longitude'],
                                   height=coords['height'])

        pe = PerevalAdd.objects.create(coords=co, beauty_title=validated_data['beauty_title'],
                                       title=validated_data['title'], other_titles=validated_data['other_titles'],
                                       connect=validated_data['connect'], add_time=validated_data['add_time'],
                                       level_winter=level['winter'], level_summer=level['summer'],
                                       level_autumn=level['autumn'], level_spring=level['spring'],
                                       user=uss)

        for obj in images:
            Images.objects.create(pereval=pe, data=obj['data'], title=obj['title'])
        data = {
            'status': '200',
            'message': 'null',
            'id': f"{pe.id}"
        }
        return data

    def update(self, instance, validated_data):
        instance.beauty_title = validated_data.get('beauty_title', instance.beauty_title)
        instance.title = validated_data.get('title', instance.title)
        instance.other_titles = validated_data.get('other_titles', instance.other_titles)
        instance.connect = validated_data.get('connect', instance.connect)
        instance.add_time = validated_data.get('add_time', instance.add_time)
        instance.level_winter = validated_data['level'].get('winter', instance.level_winter)
        instance.level_summer = validated_data['level'].get('summer', instance.level_summer)
        instance.level_autumn = validated_data['level'].get('autumn', instance.level_autumn)
        instance.level_spring = validated_data['level'].get('spring', instance.level_spring)
        instance.save()
        instance.coords.latitude = validated_data['coords'].get('latitude', instance.coords.latitude)
        instance.coords.longitude = validated_data['coords'].get('longitude', instance.coords.longitude)
        instance.coords.height = validated_data['coords'].get('height', instance.coords.height)
        instance.coords.save()
        for obj in instance.images.all():
            obj.delete()
        for obj in validated_data['images']:
            Images.objects.create(pereval=instance, data=obj['data'], title=obj['title'])
        return instance
