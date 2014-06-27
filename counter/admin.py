from django.contrib import admin
from counter.models import Event


class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'archived', 'owner']

admin.site.register(Event, EventAdmin)

# Register your models here.
