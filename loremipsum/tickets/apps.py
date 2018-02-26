from django.apps import AppConfig

class TicketsConfig(AppConfig):
    name = 'tickets'
    def ready(self):
        import tickets.signals # signals for post-save indexing in elasticsearch
