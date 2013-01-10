from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from spurapp.models import *


urlpatterns = patterns('spurapp.views',
    url(r'^ipn$', 'ipn'),
    url(r'^$', 'index'),
    url(r'^charity/(?P<charity_id>\d+)/$', 'charity_detail'),
    url(r'^charity/(?P<charity_id>\d+)/campaign/$', 'campaign'),
    url(r'^redirect/(?P<donation_id>\d+)', 'redirect'),
    url(r'^share/(?P<campaign_id>\d+)', 'share'),
    url(r'^complete_donation$', 'complete_donation'),
)
