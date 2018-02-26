from django.db import models
from django import forms
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe
from .search import EventPostIndex

class User(AbstractUser):
    is_parent = models.BooleanField('parent status', default = False)
    is_provider = models.BooleanField('provider status', default = False)

class Event(models.Model):
    AGE_RANGES = (
            ( "0005", "0-5"),
            ( "0609", "6-9"),
            ( "1012", "10-12"),
            ( "1314", "13-14"),
            )
    TYPES = (
            ( "1", "Παιδικά θέατρα"),
            ( "2", "Συναυλίες"),
            ( "3", "Παιδότοποι"),
            ( "4", "Πάρτυ"),
            ( "5", "Εκπαιδευτικές εκδρομές/εκδηλώσεις"),
            ( "6", "Αθλητικές δραστηριότητες"),
            ( "7", "Πάρκα αναψυχής"),
            ( "8", "Παιδικές κατασκηνώσεις"),
            )
    title = models.TextField(max_length=256)
    event_date = models.DateTimeField('event date')
    date_added = models.DateTimeField('Date added')
    capacity = models.IntegerField()
    availability = models.IntegerField()
    location = models.TextField(max_length=256)
    latitude = models.DecimalField(decimal_places=5, max_digits=7)
    longitude = models.DecimalField(decimal_places=5, max_digits=7)
    age_range = models.CharField(max_length=4, choices = AGE_RANGES, default="0005")
    event_type = models.CharField(max_length=1, choices = TYPES, default="1")
    cost = models.IntegerField()
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE)
    hits = models.IntegerField()

    def get_absolute_url(self):
        return "/event/%i" % self.id
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
            sort_keys=True)
    def __str__(self):
        return "%s (%s)" % (self.title, self.event_date)
    def indexing(self):
        obj = EventPostIndex(
                meta = { 'id': self.id },
                title = self.title,
                date = self.event_date,
                location = self.location,
                )
        obj.save()
        return obj.to_dict(include_meta=True)

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
    logo = models.ImageField(upload_to='media/')
    def get_absolute_url(self):
        return "/provider/%i" % self.user.id
    def __str__(self):
        return "%s" % self.full_name

class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,default='')
    email = models.EmailField(default='')
    full_name = models.TextField()
    address = models.TextField(default='')
    coins = models.IntegerField(default = 0)
    latitude = models.DecimalField(decimal_places=5, max_digits=7)
    longitude = models.DecimalField(decimal_places=5, max_digits=7)

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

class Transaction(models.Model):
    event = models.ForeignKey('Event', on_delete = models.CASCADE)
    parent = models.ForeignKey(Parent, on_delete = models.CASCADE)
    date = models.DateTimeField("Purchase date")
    amount = models.IntegerField()
    total_cost = models.IntegerField()
