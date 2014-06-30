from django.conf.urls import patterns, url

from counter import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<event_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<event_id>\d+)/reset/$', views.reset, name='reset'),
    url(r'^add/$', views.add, name='add'),
)
