from tickets.models import Event
import django_filters
from elasticsearch_dsl import DocType, Text, Date, Search

class EventFilter(django_filters.FilterSet):
    event_type = django_filters.ChoiceFilter(choices=Event.TYPES)
    class Meta:
        model = Event
        fields = ['event_type', 'age_range', 'title', ]
    def elastic_filter(self, queryset, name, value):
        s = Search().filter('match', title=value)
        response = s.execute(ignore_cache=True)
        results = set()
        response = response.to_dict()
        for r in response['hits']['hits']:
            results.add(Event.objects.get(pk=r['_id']))
        return results


