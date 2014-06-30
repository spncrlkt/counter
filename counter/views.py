import json

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone

from counter.forms import UserForm
from counter.models import Event

def index(request):
    current_user = request.user
    event_list = Event.objects.filter(owner_id=current_user.id).order_by('-last_updated_time')[:5]
    context = {'event_list': event_list}
    return render(request, 'counter/index.html', context)

@login_required
def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'counter/detail.html', {'event': event})

@login_required
def add(request):
    u = request.user
    
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

@login_required
def reset(request, event_id):
    e = get_object_or_404(Event, pk=event_id)
    ## Get authed user
    u = request.user

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


def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            registered = True

    else:
        user_form = UserForm()

    return render_to_response(
        'counter/register.html',
        {'user_form': user_form, 'registered': registered},
        context)

def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect('/counter/')

        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        return render_to_response('counter/login.html', {}, context)




@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/counter/')
