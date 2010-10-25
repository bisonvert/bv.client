#django imports
from django.conf.urls.defaults import *

#bvclient imports
from bv.client.trips.forms import TRIP_OFFER, TRIP_DEMAND

urlpatterns = patterns('bv.client.trips.views',
    (r'^$', 'home', {}, 'home'),
    
    (r'^mine/(?P<page>\d+)/$', 'list_mine', {}, 'list_mine'),
    (r'^mine/$', 'list_mine', {}, 'list_mine'),    
    
    (r'^show/(?P<trip_id>\d+)/$', 'show_trip', {}, 'show'),
    (r'^list/$', 'list_trips', {}, 'list'),    
    (r'^list/(?P<page>\d+)/$', 'list_trips', {}, 'list'),
    (r'^edit/(?P<trip_id>\d+)/$', 'edit_trip', {}, 'edit'),
    (r'^create/$', 'create_trip', {}, 'create'),
    (r'^create_return_trip/$', 'create_return_trip', {}, 'create_return_trip'),
    (r'^delete/(?P<trip_id>\d+)/$', 'delete_trip', {}, 'delete'),
    
    (r'^search/(?P<trip_type>\d)$', 'search_trip', {}, 'search'),
    (r'^search_offer/$', 'search_trip', {'trip_type': TRIP_OFFER}, 'search_offer'),
    (r'^search_demand/$', 'search_trip', {'trip_type': TRIP_DEMAND}, 'search_demand'),
    (r'^show_results/(?P<trip_id>\d+)/$', 'show_trip_results', {}, 'show_results'),
    (r'^save_search/$', 'save_search', {}, 'save_search'),
    
    #ajax calls
    (r'^get_city/$', 'get_city', {}, 'get_city'),
    (r'^get_matching_trips/$', 'display_matching_trips', {}, 'display_maching_trips'),
    (r'^get_matching_trips/(?P<trip_id>\d+)/$', 'display_matching_trips', {}, 'display_maching_trips'),
    (r'^switch_alert/(?P<trip_id>\d+)/$', 'switch_trip_alert', {}, 'switch_trip_alert'),
    (r'^calculate_buffer/', 'calculate_buffer', {}, 'calculate_buffer'),
    (r'^ogcserver/', 'ogcserver', {}, 'ogcserver'),
)
