from django.conf.urls.defaults import *
from django.core.urlresolvers import resolve, reverse
from django.conf import settings

urlpatterns = patterns('',
    (r'^$', 'trips.views.home', {}, 'home'),
    (r'^trips/', include('trips.urls', namespace='trips')),
    (r'^oauth/', include('oauthclient.urls', namespace='oauth'),
            {'identifier': getattr(settings, 'BVCLIENT_OAUTH_APPID', 'bisonvert')}),
)

# To serve static files. Do not use in production.
if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_DOC_ROOT}),
    )

