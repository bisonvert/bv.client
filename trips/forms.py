#python imports
import datetime

#django imports
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.forms.models import ModelForm, model_to_dict

#GIS import
from django.contrib.gis.geos.error import GEOSException
from django.contrib.gis.geos import GEOSGeometry

#utils import
from utils.fields import FrenchDateField, FrenchDecimalField, SelectableTimeField
from utils.widgets import FrenchDateInput, AutoCompleteTextInput, SelectableTimeWidget, NullBooleanSelect,CheckboxSelectMultipleAsArray

#constants
TRIP_OFFER = 0
TRIP_DEMAND = 1
TRIP_BOTH = 2

class BaseForm(forms.Form):
    """Base form for the carpool app"""
    
    def get_point(self, geom_wkt):
        """Return a geometry of type "point" from a WKT point"""
        try:
            geometry = GEOSGeometry(geom_wkt)
            if geometry is None or geometry.geom_type != 'Point':
                return None
            return geometry
        except (ValueError, GEOSException):
            return None
        
    def clean_route_point(self, point_name = None, 
            point_alternate_name = None, displayable_name = None, base_name = None):
        """Route point (departure/arrival) cleaner for forms
        
        Check that the WKT traject point is well filled, and match to a 
        geometry of type point.
        
        """
        if base_name:
            if not point_name:
                point_name = base_name + "_point"

            if not point_alternate_name:
                point_alternate_name = base_name
            
            if not displayable_name:
                displayable_name = base_name.capitalize()
        
        if (point_name in self.cleaned_data and self.cleaned_data[point_name]):
            point = self.get_point(self.cleaned_data[point_name])
            if point:
                return self.cleaned_data[point_alternate_name]
        raise forms.ValidationError(_(displayable_name+" address not found."))

class SearchTripForm(BaseForm):
    """Form to find a trip announce.
    
    Contains:

    + departure city
    + arrival city
    + start date

    Hidden fields are:
    
    + point for departure city (by geocoding)
    + point for arrival city (by geocoding)
    + id of the favorite departure point
    + id of the favorite arrival point
    + search type: driver or passenger
    
    """
    departure_point = forms.CharField(
        required=False,
        widget=forms.widgets.HiddenInput()
    )
    departure = forms.CharField(
        label=_("Departure:"),
        widget=AutoCompleteTextInput({'autocomplete': 'off'})
    )
    arrival_point = forms.CharField(
        required=False,
        widget=forms.widgets.HiddenInput()
    )
    arrival = forms.CharField(
        label=_("Arrival:"),
        widget=AutoCompleteTextInput({'autocomplete': 'off'})
    )
    type = forms.IntegerField(
        required=False,
        widget=forms.widgets.HiddenInput()
    )
    date = FrenchDateField(
        label=_("Date:"),
        required=False,
        initial=datetime.date.today(),
        widget=FrenchDateInput(attrs={
            'class':'type-date',
            'calendar_class':'calendarlink'
        })
    )

    def clean_departure(self):
        """Departure cleaner"""
        return self.clean_route_point(base_name = 'departure')

    def clean_arrival(self):
        """Arrival cleaner"""
        return self.clean_route_point(base_name = 'arrival')

class EditTripForm(BaseForm):
#    def __init__(self, instance=None, *args, **kwargs):
#        super(EditTripForm, self).__init__(instance=instance, *args, **kwargs)
#        if instance:
#            if instance.offer and instance.demand:
#                trip_type_value = Trip.BOTH
#            elif instance.offer:
#                trip_type_value = Trip.OFFER
#            elif instance.demand:
#                trip_type_value = Trip.DEMAND
#            else:
#                trip_type_value = Trip.BOTH
#                                
#            self.fields['trip_type'].initial = trip_type_value
        
    trip_type = forms.ChoiceField(
        label=_("Route type"),
        required=True,
        choices=((TRIP_DEMAND, _("Demand")),(TRIP_OFFER, _("Offer")),(TRIP_BOTH, _("Both"))),
    )
    name = forms.CharField(
        label=_("Announce name:"),
        required=True,
        max_length=200,
    )
    departure_city = forms.CharField(
        label=_("Departure city:"),
        required=True,
        max_length=200,
        widget=AutoCompleteTextInput()
    )
    departure_address = forms.CharField(
        label=_("Departure address:"),
        required=False,
        max_length=200,
    )
    arrival_city = forms.CharField(
        label=_("Arrival city:"),
        required=True,
        max_length=200,
        widget=AutoCompleteTextInput()
    )
    arrival_address = forms.CharField(
        label=_("Arrival address:"),
        required=False,
        max_length=200,
    )
    comment = forms.CharField(
        label=_("Comment:"),
        max_length=300,
        required=False,
        widget=forms.widgets.Textarea(),
    )
    alert = forms.BooleanField(
        label=_("Email alert:"),
        required=False,
        widget=forms.widgets.CheckboxInput({'class': 'checkbox'}),
    )
    # date params
    regular = forms.BooleanField(
        widget=forms.widgets.Select(choices=((False, _("Punctual")),(True, _("Regular")))),
        label=_("Trip frequency"),
        required=False,
    )
    date = FrenchDateField(
        label=_("Date"),
        required=False,
    )
    interval_min = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=0,
    )
    interval_max = forms.IntegerField(
        widget=forms.HiddenInput(),
        initial=0,
    )
    time = SelectableTimeField(
        label=_("Departure at about"),
        required=False,
        widget=SelectableTimeWidget
    )
    departure_point = forms.CharField(
        widget=forms.widgets.HiddenInput()
    )
    arrival_point = forms.CharField(
        widget=forms.widgets.HiddenInput()
    )
    dows = forms.MultipleChoiceField(
        widget=CheckboxSelectMultipleAsArray,
        required=False,
        choices=((0,_('Mon')),(1,_('Tue')), (2,_('Wed')), (3,_('Thu')), (4,_('Fri')), (5,_('Sat')), (6,_('Sun'))),
    )

class EditTripOptionsForm(BaseForm):
    def __init__(self, cartype_choices=None, *args, **kwargs):
        """Add a way to directly specify the list of choices when 
        initializing the form.

        """
        super(EditTripOptionsForm, self).__init__(*args, **kwargs)
        if cartype_choices:
            for cartype_field in ('passenger_car_type', 'driver_car_type'):
                field = self.fields.get(cartype_field, False)
                if field:
                    field._set_choices(cartype_choices)
            
class EditTripOfferOptionsForm(EditTripOptionsForm):
    driver_km_price = FrenchDecimalField(
        label=_("Asking price by kilometer:"),
        max_digits=7,
        decimal_places=2,
        required=False,
    )
    driver_smokers_accepted = forms.NullBooleanField(
        label=_("Smokers accepted:"),
        required=False,
        widget=NullBooleanSelect,
    )
    driver_pets_accepted = forms.NullBooleanField(
        label=_("Pets accepted:"),
        required=False,
        widget=NullBooleanSelect,
    )
    driver_place_for_luggage = forms.NullBooleanField(
        label=_("Place for luggages:"),
        required=False,
        widget=NullBooleanSelect,
    )
    driver_car_type = forms.ChoiceField(
        label=_("Car type:"),
        required=False,
    )
    driver_seats_available = forms.IntegerField(
        label=_("Seat number by default:"),
        required=False,
        widget=forms.widgets.TextInput({'size': '5'})
    )
    route = forms.CharField(
        widget=forms.widgets.HiddenInput()
    )
    steps = forms.CharField(
        widget=forms.widgets.HiddenInput()
    )
    radius = forms.IntegerField(
        initial=500,
        widget=forms.widgets.HiddenInput()
    )

class EditTripDemandOptionsForm(EditTripOptionsForm):
    passenger_max_km_price = FrenchDecimalField(
        label=_("Maximum price by kilometer:"),
        max_digits=7,
        decimal_places=2,
        required=False
    )   
    passenger_smokers_accepted = forms.BooleanField(
        label=_("Smokers accepted first:"),
        required=False,
        widget=forms.widgets.CheckboxInput({'class': 'checkbox'})
    )   
    passenger_pets_accepted = forms.BooleanField(
        label=_("Pets accepted first:"),
        required=False,
        widget=forms.widgets.CheckboxInput({'class': 'checkbox'})
    )
    passenger_place_for_luggage = forms.BooleanField(
        label=_("Place for luggages first:"),
        required=False,
        widget=forms.widgets.CheckboxInput({'class': 'checkbox'})
    )
    passenger_car_type = forms.ChoiceField(
        label=_("Car type first:"),
        required=False,
    )
    passenger_min_remaining_seats = forms.IntegerField(
        label=_("Minimum remaining seats:"),
        required=False,
        widget=forms.widgets.TextInput({'size': '5'})
    )
    radius = forms.IntegerField(
        initial=500,
        widget=forms.widgets.HiddenInput()
    )

    @property
    def cartype_choices(self):
        return self._cartype_choices

