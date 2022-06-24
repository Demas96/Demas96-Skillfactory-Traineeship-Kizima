from django.contrib.auth.models import User
from django.db import models
from django.db.models import fields


class CaseInsensitiveTextField(fields.TextField):
    def db_type(self, connection):
        return "citext"


class Coords(models.Model):
    latitude = models.FloatField(max_length=255)
    longitude = models.FloatField(max_length=255)
    height = models.IntegerField()



class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = CaseInsensitiveTextField(unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255)


class PerevalAdd(models.Model):
    NEW = 'N'
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'
    STATUS_CHOICES = [
        (NEW, 'new'),
        (PENDING, 'pending',),
        (ACCEPTED, 'accepted',),
        (REJECTED, 'rejected')
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=NEW)
    coords = models.OneToOneField(Coords, on_delete=models.CASCADE)
    beautyTitle = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    other_titles = models.CharField(max_length=255)
    connect = models.TextField(blank=True)
    add_time = models.DateTimeField()
    level_winter = models.CharField(max_length=255, blank=True)
    level_summer = models.CharField(max_length=255, blank=True)
    level_autumn = models.CharField(max_length=255, blank=True)
    level_spring = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)


class Images(models.Model):
    pereval = models.ForeignKey(PerevalAdd, on_delete=models.CASCADE)
    img = models.TextField()
    title = models.CharField(max_length=255)
    date_added = models.DateField(auto_now_add=True)







