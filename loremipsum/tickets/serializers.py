from rest_framework import serializers
from tickets.models import Event


"""
from tickets.serializers import EventSerializer
s = EventSerializer()
print(repr(s))
"""
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id',
                'event_date',
                'date_added',
                'capacity',
                'availability',
                'location',
                'latitude',
                'longitude',
                'provider',
                )
