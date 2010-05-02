from django.conf.urls.defaults import *
from django.core.urlresolvers import resolve, reverse
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'trips.views.home', {}, 'home'),
    (r'^trips/', include('trips.urls', namespace='trips')),
    (r'^talks/', include('talks.urls', namespace='talks')),
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

