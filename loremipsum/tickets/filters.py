from tickets.models import Event
import django_filters

class EventFilter(django_filters.FilterSet):
    event_type = django_filters.ChoiceFilter(choices=Event.TYPES)
    class Meta:
        model = Event
        fields = ['event_type', 'age_range', 'title', ]
