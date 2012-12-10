from django.conf.urls import patterns, include, url


urlpatterns = patterns('spurapp.views',
    url(r'^ipn$', 'ipn'),
    url(r'^$', 'index'),
    url(r'^charity/(?P<charity_id>\d+)/$', 'charity_detail'),
    url(r'^charity/(?P<charity_id>\d+)/campaign/$', 'campaign'),
)
