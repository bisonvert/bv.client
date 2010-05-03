#django imports
from django.conf.urls.defaults import *

urlpatterns = patterns('talks.views',
    url(r'^$', 'list_talks', {}, 'list'),
    url(r'^(?P<page>\d+)/$', 'list_talks', {}, 'list'),
    url(r'^with/user/(?P<trip_id>\d+)/$', 'contact_user', {}, 'contact_user'),
    url(r'^(?P<talk_id>\d+)/cancel/$', 'cancel_talk', {}, 'cancel'),
    url(r'^(?P<talk_id>\d+)/messages/$', 'list_messages', {}, 'list_messages'),
    url(r'^(?P<talk_id>\d+)/add_message/$', 'list_messages', {}, 'add_message'),
    url(r'^(?P<talk_id>\d+)/validate/$', 'validate_talk', {}, 'validate'),
)

urlpatterns += patterns('django.views.generic.simple',
    url(r'(?P<talk_id>\d+)/confirm_validate/$', 'direct_to_template', {
        'template': 'talks/confirm_validation.html',}, 'confirm_validate'),
)

