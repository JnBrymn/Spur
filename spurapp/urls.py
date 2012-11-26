from django.conf.urls import patterns, include, url


urlpatterns = patterns('spurapp.views',
    url(r'^ipn$', 'ipn'),
    # Examples:
    # url(r'^$', 'spurproject.views.home', name='home'),
    # url(r'^spurproject/', include('spurproject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
