from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Provider)
admin.site.register(Parent)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(TagEventAssociation)
