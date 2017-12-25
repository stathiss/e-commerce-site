from django.db import models
from django import forms
from django.contrib.auth.base_user import AbstractBaseUser

class Event(models.Model):
    title = models.TextField(max_length=256)
    event_date = models.DateTimeField('event date')
    date_added = models.DateTimeField('Date added')
    capacity = models.IntegerField()
    availability = models.IntegerField()
    location = models.TextField(max_length=256)
    latitude = models.DecimalField(decimal_places=5, max_digits=7)
    longitude = models.DecimalField(decimal_places=5, max_digits=7)
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE)


class Provider(AbstractBaseUser):
    full_name = models.TextField()
    email = models.EmailField()
    address = models.TextField()
    afm = models.TextField()
    doy = models.TextField()
    legal_representative = models.TextField()
    adt = models.TextField()
    site = models.URLField()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELD = ['full_name', 'email', 'address', 'site']

class Parent(AbstractBaseUser):
    email = models.EmailField()
    full_name = models.TextField()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELD = ['full_name', 'email']

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
