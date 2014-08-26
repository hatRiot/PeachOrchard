from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'server.views.home', name='home'),
    url(r'^node/([0-9]{0,5})/$', 'server.views.node', name='node'),  # supports up to 10000 nodes
    url(r'^register/$', 'server.views.register', name='register'),
    url(r'^status/$', 'server.views.status', name='status'),
    url(r'^crash/$', 'server.views.crash', name='crash'),
    url(r'^admin/', include(admin.site.urls), name='admin'),
)