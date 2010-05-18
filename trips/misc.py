from django.utils.html import escape
import time
import datetime
from django.core.urlresolvers import reverse

def get_trip_dict(trip):
    trip_dict = {
        'id': trip.id,
        'departure_city': escape(trip.departure_city),
        'departure_address': escape(trip.departure_address),
        'departure_point': trip.departure_point,
        'arrival_city': escape(trip.arrival_city),
        'arrival_address': escape(trip.arrival_address),
        'arrival_point': trip.arrival_point,
        'date': trip.date.strftime("%d/%m/%Y") if trip.date else None,
        'time': trip.time.strftime("%Hh") if trip.time else None,
#        'dows': trip.print_dows(),
        'seats_available': trip.offer.driver_seats_available if hasattr(trip,'offer') else None,
        'user_name': trip.user.username,
        'user_id': trip.user.id,
        'absolute_url': reverse('trips:show', args=[trip.id])
#        'mark': get_mark_average(trip.user_mark_sum, trip.user_mark_num),
    }
    return trip_dict
