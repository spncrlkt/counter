from django.db import models
from django.contrib.auth.models import User

"""
@------------
Event -
owner_id
name
last_updated_time
last_updated_by
archived
@------------

User -
email
password
username

Permission -
owner_id
grantee_id
event_id

ShareRequest -
granter_id
grantee_email
grantee_id
status - pending,sent,accepted


EXAMPLE:
class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


        def __unicode__(self):  # Python 3: def __str__(self):
                return self.question
"""


class Event(models.Model):
    owner = models.ForeignKey(User, related_name='event_owners')
    name = models.CharField(max_length=200)
    last_updated_time = models.DateTimeField(auto_now=True, null=True)
    last_updated_by = models.ForeignKey(User, related_name='event_updatedby',null=True)
    archived = models.BooleanField(default=False)

    def __unicode__(self): 
        return self.owner.username + ": " + self.name

class EventLog(models.Model):
    event = models.ForeignKey(Event)
    updated_time = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User)

    def __unicode__(self): 
        return self.updated_by.username + ": " + self.updated_time

class EventPermission(models.Model):
    event = models.ForeignKey(Event)
    granter = models.ForeignKey(User, related_name='event_permission_granter')
    grantee = models.ForeignKey(User, related_name='event_permission_grantee')
    STATUSES = (
        ('s','sent'),
        ('a','accepted'),
    )
    status = models.CharField(max_length=1, choices=STATUSES)

    class Meta:
        unique_together = ("event", "granter", "grantee")
