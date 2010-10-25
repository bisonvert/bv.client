from django.conf.urls.defaults import *
from django.core.urlresolvers import resolve, reverse
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('bv.client',
    (r'^$', 'trips.views.home', {}, 'home'),
    (r'^trips/', include('bv.client.trips.urls', namespace='trips')),
    (r'^talks/', include('bv.client.talks.urls', namespace='talks')),
    (r'^ratings/', include('bv.client.ratings.urls', namespace='ratings')),
    (r'^oauth/', include('oauthclient.urls', namespace='oauth', app_name='bvoauth'),
            {'identifier': getattr(settings, 'BVCLIENT_OAUTH_APPID', 'bisonvert')}),

    (r'^admin/(.*)', admin.site.root),
)

# To serve static files. Do not use in production.
if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT}),
    )

