from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from spurapp.models import *


urlpatterns = patterns('spurapp.views',
    url(r'^ipn$', 'ipn'),
    url(r'^$', 'index'),
    url(r'^charity/(?P<charity_id>\d+)/$', 'charity_detail'),
    url(r'^charity/(?P<charity_id>\d+)/campaign/$', 'campaign'),
    url(r'^redirect/(?P<donation_id>\d+)', 'redirect'),
	#url(r'^campaign/donate', 'donate'),
	# url(r'^$',
		# ListView.as_view(
			# queryset=Charity.objects,
			# context_object_name='charity_list',
			# template_name='charities/index.html')),
	# url(r'^(?P<pk>\d+)/$',
		# ListView.as_view(
			# queryset=Campaign.objects,
			# template_name='campaign/index.html')),
	# url(r'^(?P<pk>\d+)/$',
		# DetailView.as_view(
			# model=Charity,
			# template_name='charities/detail.html')),
	# url(r'^(?P<pk>\d+)/$',
		# DetailView.as_view(
			# model=Campaign,
			# template_name='campaign/detail.html')),
)
