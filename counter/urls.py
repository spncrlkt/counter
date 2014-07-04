from django.conf.urls import patterns, url

from counter import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<event_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<event_id>\d+)/reset/$', views.reset, name='reset'),
    url(r'^(?P<event_id>\d+)/add_permission/$', views.add_permission, name='add_permission'),
    url(r'^add/$', views.add, name='add'),
    url(r'^accept_invite/$', views.accept_invite, name='accept_invite'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='user_login'),
    url(r'^logout/$', views.user_logout, name='user_logout'),
)
