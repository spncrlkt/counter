import json

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader

from counter.models import Event
from django.contrib.auth.models import User
from django.utils import timezone

def index(request):
    event_list = Event.objects.order_by('-last_updated_time')[:5]
    context = {'event_list': event_list}
    return render(request, 'counter/index.html', context)

def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'counter/detail.html', {'event': event})

def add(request):
    ## Get authed user
    u = get_object_or_404(User, username='sliechty')
    
    name = request.POST['event_name']
    e = Event(owner=u, name=name)
    try:
        e.save()
    except Exception as ex:
        # return error
        return HttpResponse(json.dumps({
            'error_message': ex,
        }))
        
    return HttpResponse(json.dumps({'event_id':e.id}))

def reset(request, event_id):
    e = get_object_or_404(Event, pk=event_id)
    ## Get authed user
    u = get_object_or_404(User, username='sliechty')

    try:
        ## Update last_updated info
        e.last_updated_by = u
        e.last_udated_time = timezone.now
        e.save()
    except Exception as ex:
        # return error
        return HttpResponse(json.dumps({
            'event_id': e.id,
            'error_message': ex,
        }))

    return HttpResponse(json.dumps({'event_id':e.id}))
