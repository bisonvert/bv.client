#django imports
from django.conf.urls.defaults import *

pending_params = {'method': 'get_pending_ratings', 'template': 'ratings/pending.html'}
received_params = {'method': 'get_received_ratings', 'template': 'ratings/received.html'}
given_params = {'method': 'get_given_ratings', 'template': 'ratings/given.html'}

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
