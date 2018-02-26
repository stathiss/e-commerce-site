from .models import Event
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Event)
def index_post(sender, instance, **kwargs):
    instance.indexing() # signals for post-save indexing in elasticsearch
