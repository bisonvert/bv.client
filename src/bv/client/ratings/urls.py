#django imports
from django.conf.urls.defaults import *

pending_params = {
    'method': 'get_pending_ratings', 
    'template': 'ratings/pending.html',
    'extra_context': {'is_pending': True}
}
received_params = {
    'method': 'get_received_ratings', 
    'template': 'ratings/received.html',
    'extra_context': {'is_received': True}
}
given_params = {
    'method': 'get_given_ratings', 
    'template': 'ratings/given.html',
    'extra_context': {'is_given': True}
}

urlpatterns = patterns('ratings.views',
    url(r'^$', 'list_ratings', pending_params, 'list'),
    url(r'^pending/$', 'list_ratings', pending_params, 'pending'),
    url(r'^pending/(?P<page>\d+)/$', 'list_ratings', pending_params, 'pending'),
    url(r'^received/$', 'list_ratings', received_params, 'received'),
    url(r'^received/(?P<page>\d+)/$', 'list_ratings', received_params, 'received'),
    url(r'^given/$', 'list_ratings', given_params, 'given'),
    url(r'^given/(?P<page>\d+)/$', 'list_ratings', given_params, 'given'),
    
    url(r'^rate/(?P<temprating_id>\d+)/', 'rate_user', {}, 'rate_user'),
)
