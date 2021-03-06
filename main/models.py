from django.contrib.auth.models import User, AbstractUser
from django.db import models

from django.core import serializers


class Coords(models.Model):
    latitude = models.FloatField(max_length=255, verbose_name='Широта')
    longitude = models.FloatField(max_length=255, verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    def __str__(self):
        return f'{self.latitude} {self.longitude} {self.height}'

    def extra_address(self):
        return serializers.serialize('python', self.pereval.all())

    class Meta:
        verbose_name_plural = ("Координаты")


class Users(AbstractUser):
    email = models.EmailField(unique=True)
    patronymic = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.email}: {self.last_name} {self.first_name} {self.patronymic}'


class PerevalAdd(models.Model):
    NEW = 'NEW'
    PENDING = 'PENDING'
    ACCEPTED = 'ACCEPTED'
    REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (NEW, 'new'),
        (PENDING, 'pending',),
        (ACCEPTED, 'accepted',),
        (REJECTED, 'rejected')
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=NEW)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    beauty_title = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField()
    level_winter = models.CharField(max_length=255, blank=True)
    level_summer = models.CharField(max_length=255, blank=True)
    level_autumn = models.CharField(max_length=255, blank=True)
    level_spring = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='pereval')

    def __str__(self):
        return f'{self.beauty_title} {self.title} {self.other_titles}'

    class Meta:
        verbose_name_plural = ("Перевалы")


class Images(models.Model):
    pereval = models.ForeignKey(PerevalAdd, on_delete=models.CASCADE, related_name='images')
    data = models.TextField()
    title = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.pereval}: {self.title}'

    class Meta:
        verbose_name_plural = ("Изображения")


class PerevalAreas(models.Model):
    id_parent = models.IntegerField()
    title = models.TextField()

    def __str__(self):
        return f'{self.title}'


class ActivitiesTypes(models.Model):
    title = models.TextField()

    def __str__(self):
        return f'{self.title}'
