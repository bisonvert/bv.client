#django imports
from django.conf.urls.defaults import *

urlpatterns = patterns('talks.views',
    url(r'contact_user/(?P<trip_id>\d+)', 'contact_user', {}, 'contact_user'),
    url(r'list/', 'list_talks', {}, 'list'),
    url(r'list/(?P<page>\d+)', 'list_talks', {}, 'list'),
    url(r'(?P<talk_id>\d+)/cancel/', 'cancel_talk', {}, 'cancel'),
    url(r'(?P<talk_id>\d+)/messages/', 'list_messages', {}, 'list_messages'),
    url(r'(?P<talk_id>\d+)/add_message/', 'list_messages', {}, 'add_message'),
    url(r'(?P<talk_id>\d+)/validate/', 'validate_talk', {}, 'validate'),
)

