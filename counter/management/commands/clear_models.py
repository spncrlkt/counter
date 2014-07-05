from django.core.management.base import BaseCommand
from counter.models import Event, EventLog, EventPermission 

class Command(BaseCommand):
    def handle(self, *args, **options):
        EventPermission.objects.all().delete()
        EventLog.objects.all().delete()
        Event.objects.all().delete()
