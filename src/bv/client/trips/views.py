# python imports
import time
import datetime

# django imports
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError, HttpResponse, Http404
from django.template import RequestContext
from django.conf import settings

# bvclient imports
from bv.libclient.libtrips import LibTrips
from bv.libclient.libusers import LibUsers
from bv.libclient.utils import unicode_to_dict
from bv.libclient.ext.dj import inject_lib, need_bvoauth_authentication, \
        is_bvoauth_authenticated
from bv.libclient.exceptions import ResourceAccessForbidden, ResourceDoesNotExist
from bv.client.trips.misc import get_trip_dict
from bv.client.utils.paginator import compute_nb_pages

# forms
from forms import EditTripForm, SearchTripForm, TRIP_OFFER, TRIP_DEMAND, \
    TRIP_BOTH, EditTripOfferOptionsForm, EditTripDemandOptionsForm

# utils
import simplejson

# gis imports
from django.contrib.gis.geos import MultiPoint, GEOSGeometry

DEFAULT_ITEMS_PER_PAGE = settings.DEFAULT_ITEMS_PER_PAGE

"""This file contains all necessary material to interact with trips: search, 
creation, list, edition.

"""

@inject_lib(LibTrips)
def home(request, lib):
    """Display a simple search form, redirecting to the trip search result view.
    
    """
    if request.POST:
        form = SearchTripForm(request.POST)
        if form.is_valid():
            return search_trip(request, int(request.POST['type']))
    else:
        form = SearchTripForm()
        
    return render_to_response('home.html', {
        'form': form,
        'is_home': True,
    }, context_instance=RequestContext(request))


def search_trip(request, trip_type):
    """Action used to find information about existing trips.
    
    Display a map, with the actual trip, and a way to make some requests to 
    adjust all this.
    
    """
    try:
        mpoints = MultiPoint([
            GEOSGeometry(request.POST['departure_point']), 
            GEOSGeometry(request.POST['arrival_point']),
        ])
    except:
        return redirect(reverse('trips:home'))

    return render_to_response('search_trip.html', {
        'gmapkey': settings.GOOGLE_MAPS_API_KEY,
        'geometry': mpoints.envelope.wkt,
        'trip_details': {
            'departure': {
                'name': request.POST['departure'],
                'point': request.POST['departure_point'],
            },
            'arrival': {
                'name': request.POST['arrival'],
                'point': request.POST['arrival_point'],
            },
            'date': request.POST['date'],
        },
        'trip_type': trip_type,
        'OFFER': TRIP_OFFER,
        'is_trip': True,
    }, context_instance=RequestContext(request))

@need_bvoauth_authentication()
@inject_lib(LibTrips)
def show_trip_results(request, trip_id=None, lib=None):
    """Display information about the given trip and provides way to query the API
    to have information about matching trips.

    """
    userLib = LibUsers(**lib.get_params())
    user = userLib.get_active_user()
    trip = lib.get_trip(trip_id)

    if user.id != trip.user.id:
        raise Http404()

    if request.POST:
        dict = {}
        trip_details = simplejson.loads(request.POST['trip_details'])
        trip = lib.edit_trip(trip_id, **trip_details)

    return render_to_response('show_trip_results.html', {
        'trip': trip,
        'default_zoom': settings.DEFAULT_MAP_CENTER_ZOOM, 
        'default_center': settings.DEFAULT_MAP_CENTER_POINT,
        'is_trip': True,
        'page_url': request.build_absolute_uri(),
    }, context_instance=RequestContext(request))

@inject_lib(LibTrips)
def display_matching_trips(request, trip_id=None, lib=None):
    """Make a request to the BV server to find matching trips. Format the 
    output to be read by javascript clientside code.
    
    """
    def to_json(trip):
        return [get_trip_dict(t) for t in trips]

    trip_search_type = int(request.POST['trip_type'])
    results = lib.search_trip(trip_id=trip_id, **unicode_to_dict(request.POST))
    trip_demands = results['trip_demands']
    trip_offers = results['trip_offers']
    trip = results['trip']
    
    if trip_search_type == TRIP_OFFER:
        trips = trip_demands
    else:
        trips = trip_offers
    
    response_dict = {
        'authenticated': is_bvoauth_authenticated(request),
    }
    if not trip_id:
        response_dict['trips'] = to_json(trips)
    else:
        response_dict['trip_demands'] = to_json(trip_demands)
        response_dict['trip_offers'] = to_json(trip_offers)
    resp = HttpResponse()
    simplejson.dump(response_dict , resp, ensure_ascii=False, separators=(',',':'))
    return resp
    
@inject_lib(LibTrips)
def list_trips(request, page=1, lib=None):
    """List all trips
    
    """
    count = lib.count_trips()
    items_per_page = getattr(settings, 'TRIPS_PER_PAGE', DEFAULT_ITEMS_PER_PAGE)
    return render_to_response('list_trips.html', {
        'trips': lib.list_trips(page, items_per_page), 
        'count': count, 
        'page': int(page),
        'listpages': range(1, count // items_per_page +2),
        'is_trip': True,
    }, context_instance=RequestContext(request))

@need_bvoauth_authentication()
@inject_lib(LibTrips)
def list_mine(request, page=1, lib=None):
    """List all trips for the current user.
    
    """
    userlib = LibUsers(**lib.get_params())
    count = lib.count_user_trips()
    items_per_page = getattr(settings, 'TRIPS_PER_PAGE', DEFAULT_ITEMS_PER_PAGE)
    return render_to_response('my_trips.html', {
        'user': userlib.get_active_user(),
        'trips': lib.list_user_trips(page, items_per_page), 
        'count': count,
        'page': int(page),
        'listpages': compute_nb_pages(count, items_per_page),
        'is_trip': True,
    }, context_instance=RequestContext(request))

@inject_lib(LibTrips)
def show_trip(request, trip_id=None, lib=None):
    """display informations about a trip

    """
    return render_to_response('show_trip.html', {
        'trip': lib.get_trip(trip_id),
        'default_zoom': settings.DEFAULT_MAP_CENTER_ZOOM, 
        'default_center': settings.DEFAULT_MAP_CENTER_POINT,
        'authenticated': is_bvoauth_authenticated(request),
        'is_trip': True,
    }, context_instance=RequestContext(request))


@need_bvoauth_authentication()
@inject_lib(LibTrips)
def create_trip(request, trip_id=None, trip_from_search=False, lib=None):
    """Creates/Edit a trip.
    
    If informations provided in request.POST, try to send them throught the API, 
    and display eventual errors or redirect to the search view.
    
    If no informations provided in request.POST, just display the create trip
    form.
    
    """
    userlib = LibUsers(**lib.get_params())
    userprofiledata = userlib.get_active_user().to_dict()
    cartypes = [(c.id, c.name) for c in lib.get_cartypes()]
    
    if request.method == 'POST':
        if trip_id:
            #edition of an existing trip.
            trip = lib.get_trip(trip_id)
            form = EditTripForm(data=request.POST)
            form_offer = EditTripOfferOptionsForm(data=request.POST, 
                prefix="offer", cartype_choices=cartypes)
            form_demand = EditTripDemandOptionsForm(data=request.POST, 
                prefix="demand", cartype_choices=cartypes)
        else:
            # creation of a new trip.
            form = EditTripForm(data=request.POST)
            form_offer = EditTripOfferOptionsForm(prefix="offer",
                cartype_choices=cartypes,
                initial=userprofiledata, 
            )

            form_demand = EditTripDemandOptionsForm(prefix="demand", 
                cartype_choices =cartypes,
                initial=userprofiledata,
            )

            trip_type = int(request.POST['trip_type']) 
            if trip_type == TRIP_OFFER or trip_type == TRIP_BOTH:
                form_offer = EditTripOfferOptionsForm(
                    prefix="offer", 
                    data=request.POST,
                    cartype_choices=cartypes
                )
            if trip_type == TRIP_DEMAND or trip_type == TRIP_BOTH:
                form_demand = EditTripDemandOptionsForm(
                    prefix="demand", 
                    data=request.POST,
                    cartype_choices=cartypes
                )
        error = False
        if form.is_valid() and not trip_from_search:
            trip_type = int(form['trip_type'].data)
            
            if trip_type != TRIP_DEMAND : 
                if not form_offer.is_valid():
                    error = True
    
            if trip_type != TRIP_OFFER:
                if not form_demand.is_valid():
                    error = True
    
            if error == False:
                finaldict = {}
                for f in (form, form_offer, form_demand):
                    if hasattr(f, 'cleaned_data'):
                        for key,value in f.cleaned_data.items():
                            finaldict.setdefault(key, value)
                if trip_id:
                    lib.edit_trip(trip_id=trip_id, **unicode_to_dict(dict(request.POST.lists())))
                else:
                    trip = lib.add_trip(**unicode_to_dict(dict(request.POST.lists())))
                if request.POST['return_trip'] == 'true':
                    return redirect(reverse('trips:create_return_trip', args=[trip.id]))
                else:
                    return redirect(reverse('trips:show_results', args=[trip.id]))
    else:
        if trip_id:
            #edition of an existing trip.
            trip = lib.get_trip(trip_id)
            form = EditTripForm(initial=trip)
            offer_initial = getattr(trip, 'offer',None)
            demand_initial = getattr(trip, 'demand', None)
            form_offer = EditTripOfferOptionsForm(initial=offer_initial, 
                prefix="offer", cartype_choices=cartypes)
            form_demand = EditTripDemandOptionsForm(initial=demand_initial, 
                prefix="demand", cartype_choices=cartypes)
        else:
            form = EditTripForm()
            form_offer = EditTripOfferOptionsForm(
                initial=userprofiledata, 
                prefix="offer", 
                cartype_choices=cartypes
            )
            form_demand = EditTripDemandOptionsForm(
                initial=userprofiledata, 
                prefix="demand",
                cartype_choices=cartypes
            )
    view_dict = {
        'form':form,
        'trip_from_search': trip_from_search,
        'form_offer_options': form_offer,
        'form_demand_options': form_demand,
        'default_zoom': settings.DEFAULT_MAP_CENTER_ZOOM, 
        'default_center': settings.DEFAULT_MAP_CENTER_POINT,
        'is_trip': True,
    }
    if trip_id:
        view_dict['trip'] = trip

    return render_to_response('add_trip.html', view_dict, context_instance=RequestContext(request))

@need_bvoauth_authentication()
@inject_lib(LibTrips)
def save_search(request, lib):
    """Display a page with all information about the trip.
    
    If request.POST is filled, try to save the data trough the API.
    
    """
    return create_trip(request, trip_from_search=True)

@need_bvoauth_authentication()
@inject_lib(LibTrips)
def create_return_trip(request, trip_id=None, lib=None):
    """Given an existing trip, pre-fill the field to create a return trip and
    redirect the user to the create trip action.
    """
    pass

def edit_trip(request, trip_id=None):
    """Edit a trip.
    
    This is an alias to the `create_trip` function, because the flow of creation
    also contains a flow of edition.
    """
    return create_trip(request, trip_id)

@need_bvoauth_authentication()
@inject_lib(LibTrips)
def delete_trip(request, trip_id=None, lib=None):
    """Deletes an existing trip.
    
    Try to delete a trip, if the API raise an error, display here the error 
    message, if everything is going fine, well, let's redirect to the list of
    trips.
    
    """
    try:
        lib.delete_trip(trip_id)
    except ResourceDoesNotExist, ResourceAccessForbidden:
        dict = {
        }
    return redirect(reverse('trips:list_mine'))
    
@inject_lib(LibTrips)
def get_city(request, lib):
    """Return a list of cities begining with the provided name. 
    
    """
    if 'value' in request.POST:
        value = request.POST['value']
        cities = lib.get_cities(value)
        return HttpResponse('<ul>%s</ul>' % ''.join(['<li>%s</li>' % u"%s (%02d)" 
            % (city['name'], city['zipcode']/1000) for city in cities]))

@need_bvoauth_authentication()
@inject_lib(LibTrips)
def switch_trip_alert(request, trip_id=None, lib=None):
    """Switch the alert on/off for a specific trip.

    """
    trip = lib.get_trip(trip_id)
    lib.set_alert(trip_id, not trip.alert)
    response_dict = {'status': 'ok', 'alert': not trip.alert} 
    resp = HttpResponse() 
    simplejson.dump(response_dict , resp, ensure_ascii=False,
        separators=(',',':')) 

    return resp

@inject_lib(LibTrips)
def calculate_buffer(request, lib):
    response_dict = lib.calculate_buffer(
        unicode_to_dict(dict(request.REQUEST.items())))

    resp = HttpResponse()
    simplejson.dump(response_dict, 
        resp, ensure_ascii=False, separators=(',',':'))

    return resp

@inject_lib(LibTrips)
def ogcserver(request, lib):
    return HttpResponse(lib.ogcserver(
        unicode_to_dict(dict(request.REQUEST.items()))), content_type="image/png")
