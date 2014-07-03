from django.contrib import admin
from counter.models import Event, EventPermission


class EventAdmin(admin.ModelAdmin):
    fields = ['name', 'archived', 'owner']

class EventPermissionAdmin(admin.ModelAdmin):
    fields = ['event', 'grantee', 'granter','status']

admin.site.register(Event, EventAdmin)
admin.site.register(EventPermission, EventPermissionAdmin)

# Register your models here.
