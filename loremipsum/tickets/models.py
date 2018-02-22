from django.db import models
from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe

class User(AbstractUser):
    is_parent = models.BooleanField('parent status', default = False)
    is_provider = models.BooleanField('provider status', default = False)

class Event(models.Model):
    title = models.TextField(max_length=256)
    event_date = models.DateTimeField('event date')
    date_added = models.DateTimeField('Date added')
    capacity = models.IntegerField()
    availability = models.IntegerField()
    location = models.TextField(max_length=256)
    latitude = models.DecimalField(decimal_places=5, max_digits=7)
    longitude = models.DecimalField(decimal_places=5, max_digits=7)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    cost = models.IntegerField()
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE)

    def get_absolute_url(self):
        return "/event/%i" % self.id

class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default='')
    full_name = models.TextField()
    email = models.EmailField()
    address = models.TextField(default='')
    afm = models.TextField()
    doy = models.TextField()
    legal_representative = models.TextField()
    adt = models.TextField()
    site = models.URLField()
    def get_absolute_url(self):
        return "/provider/%i" % self.user.id

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default='')
    email = models.EmailField(default='')
    full_name = models.TextField()
    address = models.TextField(default='')

class Review(models.Model):
    date = models.DateTimeField('review date')
    user = models.ForeignKey('Parent', on_delete =models.CASCADE)
    event = models.ForeignKey('Event', on_delete= models.CASCADE)
    content = models.TextField()
    rating = models.IntegerField()

class Tag(models.Model):
    name = models.TextField()

class TagEventAssociation(models.Model):
    event = models.ForeignKey('Event', on_delete = models.CASCADE)
    tag = models.ForeignKey('Tag', on_delete = models.CASCADE)
