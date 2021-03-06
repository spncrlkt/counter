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
from counter.models import Event, EventLog, EventPermission

def index(request):
    current_user = request.user

    own_events = Event.objects.filter(owner_id=current_user.id).order_by('-last_updated_time')
    others_events = Event.objects.filter(eventpermission__grantee_id=current_user.id).filter(eventpermission__status='a').order_by('-last_updated_time')
    event_list = own_events | others_events

    unaccepted_invites = EventPermission.objects.select_related().filter(grantee_id=current_user.id).filter(status='s')

    context = {
        'event_list': event_list,
        'unaccepted_invites': unaccepted_invites,
    }
    return render(request, 'counter/index.html', context)

@login_required
def detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event_log = EventLog.objects.filter(event_id=event.id).order_by('-updated_time')[:5]
    return render(request, 'counter/detail.html', {'event': event, 'event_log': event_log})

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

        log = EventLog(event=e, updated_time=timezone.now, updated_by=u)
        log.save()
    except Exception as ex:
        # return error
        return HttpResponse(json.dumps({
            'event_id': e.id,
            'error_message': ex,
        }))

    return HttpResponse(json.dumps({'event_id':e.id}))

@login_required
def add_permission(request, event_id):
    # Get objects from request
    u = request.user
    grantee_email = request.POST['grantee_email']
    e = Event.objects.select_related().get(id=event_id)

    try:
        grantee_u = User.objects.get(email=grantee_email)
    except User.DoesNotExist: 
        # Instead need to send join up email to unsigned up user
        return HttpResponse(json.dumps({'status':'sent'}))
        
    if e and grantee_u and e.owner.id == u.id:
        try:
            ep = EventPermission(granter=u, grantee=grantee_u, event=e, status='s')
            ep.save()
        except Exception as ex:
            # return error
            return HttpResponse(json.dumps({
                'error_message': ex.message,
            }))
        
    return HttpResponse(json.dumps({'status':'sent'}))

@login_required
def accept_invite(request):
    ## Get authed user
    u = request.user

    invite_id = request.POST['invite_id']

    try:
        ep = EventPermission.objects.get(pk=invite_id)
        ep.status = 'a';
        ep.save()
    except Exception as ex:
        # return error
        return HttpResponse(json.dumps({
            'error_message': ex,
        }))

    return HttpResponse(json.dumps({'status':'accepted'}))

######################
# Bullshitty auth code
######################

def register(request):
    context = RequestContext(request)

    registered = False

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        user = User(email=email, username=username)

        try:
            user.set_password(password)
            user.save()
            registered = True
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect('/counter/')

        except Exception as ex:
            # return error
            return HttpResponse(json.dumps({
                'error_message': ex.message,
            }))

    return render_to_response(
        'counter/register.html',
        {'registered': registered},
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

