from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

"""
elasticsearch is in another container
"""
connections.create_connection(hosts=['elasticsearch:9200'], timeout=20)

"""
Model description for elasticsearch index
"""
class EventPostIndex(DocType):
    title = Text()
    event_date = Date()
    location = Text()

    class Meta:
        index = 'event-index'

"""
This function indexes all existing Events. Call it from a django shell session
manually
"""
def bulk_indexing():
    EventPostIndex.init()
    es = Elasticsearch('elasticsearch:9200')
    bulk(client=es, actions=(b.indexing() for b in models.Event.objects.all().iterator()))
