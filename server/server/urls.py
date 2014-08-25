from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'server.views.home'),
    # supports up to 10000 nodes
    url(r'^node/([0-9]{0,5})/$', 'server.views.node'),
    url(r'^register/$', 'server.views.register'),
    url(r'^status/$', 'server.views.status'),
    url(r'^crash/$', 'server.views.crash'),
    url(r'^admin/', include(admin.site.urls)),
)