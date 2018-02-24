from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

connections.create_connection(hosts=['elasticsearch:9200'], timeout=20)

class EventPostIndex(DocType):
    title = Text()
    event_date = Date()
    location = Text()

    class Meta:
        index = 'event-index'

def bulk_indexing():
    EventPostIndex.init()
    es = Elasticsearch('elasticsearch:9200')
    bulk(client=es, actions=(b.indexing() for b in models.Event.objects.all().iterator()))
