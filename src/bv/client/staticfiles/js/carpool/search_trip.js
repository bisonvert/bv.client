var departure_marker;
var arrival_marker;
var trip_route = null;

var trips = new Hash();
var departure_poly;
var arrival_poly;

var interval_min_radius = 6;
var interval_max_radius = 1;

var trip_pg = 10;
var trip_updater = new TripUpdater(trip_pg, trip_type, true);

var trip_offers_updater = new TripUpdater(trip_pg, TYPE_OFFER, false);
var trip_demands_updater = new TripUpdater(trip_pg, TYPE_DEMAND, false);

var departure_ready = true;
var departure_sync = true;
var arrival_ready = true;
var arrival_sync = true;
var map2recenter = false;

completeDragMarker = function(marker, pixel) {
    if (!marker) return;
    departure_sync = false;
    arrival_sync = false;
    if (trip_type != TYPE_DEMAND) {
        removeRoute();
    } else {
        displayDepartureRadiusCircle();
        displayArrivalRadiusCircle();
    }
    getTrips(true);
    if (trip_type != TYPE_DEMAND) {
        setDirections();
    }
    // check if it is not a result marker
    if (marker != departure_marker && marker != arrival_marker)
        return;
    var glonlat = OpenLayers.Layer.SphericalMercator.inverseMercator(marker.geometry.x, marker.geometry.y);
    new Ajax.Request('/ajax/reverse_geocode/', { method:'get',
        parameters: {
            lat: glonlat.lat,
            lng: glonlat.lon
        },
        onSuccess: function(transport){
            var json = transport.responseText.evalJSON();
            if (marker == departure_marker) {
                $('id_departure_name').setValue(json.city_name);
                $('id_departure_point').setValue('');
                var text = "<b>" + gettext('Departure') + ":</b><br />" + json.city_name;
                departure_sync = true;
            } else {
                $('id_arrival_name').setValue(json.city_name);
                $('id_arrival_point').setValue('');
                var text = "<b>" + gettext('Arrival') + ":</b><br />" + json.city_name;
                arrival_sync = true;
            }
            marker.attributes.name = text;
        }
    });
}

function setDeparturePoint(point, text) {
    hideMarkerPopup(departure_marker);
    markers.removeFeatures([departure_marker]);
    var marker_style = (trip_type != TYPE_OFFER) ? departure_passenger_style : departure_car_style;
    departure_marker = new OpenLayers.Feature.Vector(
        point,
        {id: "d", name: text},
        //marker_style
        departure_style
    );
    markers.addFeatures([departure_marker]);
    if (trip_type != TYPE_OFFER) {
        displayDepartureRadiusCircle();
    }
}

function departurePointGeocoder() {
    var departure_name = $('id_departure_name').getValue();
    if ($('id_departure_point').getValue()) {
        setDeparturePoint(
            wkt.read($('id_departure_point').getValue()).geometry,
            "<b>" + gettext("Departure") + ":</b><br />" + departure_name
        );
        departure_sync = true;
        return;
    }
    departure_ready = false;
    if (departure_name) {
        geocoder.getLatLng(
            departure_name,
            function(point) {
                if (!point) {
                    alert(gettext("ERROR : Departure address not found."));
                } else {
                    var lonlat = OpenLayers.Layer.SphericalMercator.forwardMercator(point.lng(), point.lat());
                    setDeparturePoint(
                        new OpenLayers.Geometry.Point(lonlat.lon, lonlat.lat),
                        "<b>" + gettext("Departure") + ":</b><br />" + departure_name
                    );
                }
                departure_sync = true;
                departure_ready = true;
            }
        );
    }
}

function setArrivalPoint(point, text) {
    hideMarkerPopup(arrival_marker);
    markers.removeFeatures([arrival_marker]);
    var marker_style = (trip_type != TYPE_OFFER) ? arrival_passenger_style : arrival_car_style;
    arrival_marker = new OpenLayers.Feature.Vector(
        point,
        {id: "a", name: text},
        //marker_style
        arrival_style
    );
    markers.addFeatures([arrival_marker]);
    if (trip_type != TYPE_OFFER) {
        displayArrivalRadiusCircle();
    }
}

function arrivalPointGeocoder() {
    var arrival_name = $('id_arrival_name').getValue();
    if ($('id_arrival_point').getValue()) {
        setArrivalPoint(
            wkt.read($('id_arrival_point').getValue()).geometry,
            "<b>" + gettext("Arrival") + ":</b><br />" + arrival_name
        );
        arrival_sync = true;
        return;
    }
    arrival_ready = false;
    if (arrival_name) {
        geocoder.getLatLng(
            arrival_name,
            function(point) {
                if (!point) {
                    alert(gettext("ERROR : Arrival address not found."));
                } else {
                    var lonlat = OpenLayers.Layer.SphericalMercator.forwardMercator(point.lng(), point.lat());
                    setArrivalPoint(
                        new OpenLayers.Geometry.Point(lonlat.lon, lonlat.lat),
                        "<b>" + gettext("Arrival") + ":</b><br />" + arrival_name
                    );
                }
                arrival_ready = true;
                arrival_sync = true;
            }
        );
    }
}

function displayRoute() {
    trip_layer.addFeatures([trip_route]);
}

function removeRoute() {
    if (trip_route) {
        trip_layer.removeFeatures([trip_route]);
        trip_route = null;
    }
    if (simple_trip_buffer) {
        trip_layer.removeFeatures([simple_trip_buffer]);
        simple_trip_buffer = null;
    }
}

function displayDepartureRadiusCircle() {
    if (trip_type != TYPE_OFFER) return;
    removeDepartureRadiusCircle();
    departure_poly = new OpenLayers.Feature.Vector(getCircle(departure_marker.geometry, trip_radius), null, buffer_style);
    trip_layer.addFeatures([departure_poly]);
}

function removeDepartureRadiusCircle() {
    if (departure_poly) {
        trip_layer.removeFeatures([departure_poly]);
        departure_poly = null;
    }
}

function displayArrivalRadiusCircle() {
    if (trip_type != TYPE_DEMAND) return;
    removeArrivalRadiusCircle();
    arrival_poly = new OpenLayers.Feature.Vector(getCircle(arrival_marker.geometry, trip_radius), null, buffer_style);
    trip_layer.addFeatures([arrival_poly]);
}

function removeArrivalRadiusCircle() {
    if (arrival_poly) {
        trip_layer.removeFeatures([arrival_poly]);
        arrival_poly = null;
    }
}

function getTrips(redraw_route) {
    // wait for geocoding
    if (departure_ready && arrival_ready) {
        if (trip_type != TYPE_DEMAND && redraw_route) {
            removeRoute();
            setDirections();
        }
        retrieveTrips();
        if (map2recenter) {
            var dabounds = (new OpenLayers.Geometry.MultiPoint([departure_marker.geometry, arrival_marker.geometry])).getBounds();
            map.setCenter(dabounds.getCenterLonLat(), map.getZoomForExtent(dabounds));
            map2recenter = false;
        }
    } else {
        setTimeout("getTrips("+redraw_route+");", 100);
    }
}

function retrieveTrips() {
    if (trip_type == TYPE_DEMAND || trip_route != null) {
        $('wait').show();
        new Ajax.Request('/trips/get_matching_trips/', { method:'post',
            parameters: {
                departure_name: $('id_departure_name').getValue(),
                departure_point: wkt.write(
                        departure_marker
                    ),

                departure_sync: departure_sync,
                arrival_name: $('id_arrival_name').getValue(),
                arrival_point: wkt.write(
                        arrival_marker
                    ),

                arrival_sync: arrival_sync,
                geometry: (trip_type != TYPE_DEMAND) ? wkt.write(new OpenLayers.Feature.Vector(trip_route.geometry)) : "",
                interval_min: 7-interval_min_radius,
                interval_max: interval_max_radius,
                date: $('id_date').getValue(),
                offer_radius: (trip_type != TYPE_DEMAND) ? trip_radius : 0,
                demand_radius: (trip_type != TYPE_OFFER) ? trip_radius : 0,
                trip_type: trip_type
            },
            onSuccess: function(transport){
                var json = transport.responseText.evalJSON();
                if (trip_type != TYPE_DEMAND)
                    trip_demands_updater.updateTrips(json.trips, json.authenticated);
                if (trip_type != TYPE_OFFER)
                    trip_offers_updater.updateTrips(json.trips, json.authenticated);
                // trip_updater.updateTrips(json.trips, json.authenticated);
                $('wait').hide();
            },
            onFailure: function() {
                $('wait').hide();
            }
        });
    } else {
        setTimeout("retrieveTrips()", 100);
    }
}

/******************** GMAP **********************/
function setDirections() {
    var from = OpenLayers.Layer.SphericalMercator.inverseMercator(departure_marker.geometry.x, departure_marker.geometry.y);
    var to = OpenLayers.Layer.SphericalMercator.inverseMercator(arrival_marker.geometry.x, arrival_marker.geometry.y);
    gdir.load("from: " + from.lat + ", " + from.lon + " to: " + to.lat + ", " + to.lon, { getPolyline: true });
}

function handleErrors(){
    if (gdir.getStatus().code == G_GEO_UNKNOWN_ADDRESS) {
        alert(gettext('Error : Address not found.'));
    } else if (gdir.getStatus().code == G_GEO_UNKNOWN_DIRECTIONS) {
        alert(interpolate(gettext('Route %s - %s not found.'), [$('id_departure_name').getValue(), $('id_arrival_name').getValue()]));
    } else if (gdir.getStatus().code == G_GEO_SERVER_ERROR) {
        alert(interpolate(gettext('Directions request could not be successfully processed.\nError code: %s'), [gdir.getStatus().code]));
    } else if (gdir.getStatus().code == G_GEO_BAD_KEY) {
        alert(interpolate(gettext('Invalid key.\nError code: %s'), [gdir.getStatus().code]));
    } else if (gdir.getStatus().code == G_GEO_BAD_REQUEST) {
        alert(interpolate(gettext('A directions request could not be successfully parsed.\nError code: %s'), [gdir.getStatus().code]));
    } else {
        alert(interpolate(gettext('An error occurs.\nError code: %s'), [gdir.getStatus().code]));
    }
}

function onGDirectionsLoad() {
    var points = new Array();
    var lonlat;
    for (var i=0; i < gdir.getPolyline().getVertexCount(); i++) {
        lonlat = OpenLayers.Layer.SphericalMercator.forwardMercator(
            gdir.getPolyline().getVertex(i).lng(), 
            gdir.getPolyline().getVertex(i).lat()
        );
        points[points.length] = new OpenLayers.Geometry.Point(lonlat.lon, lonlat.lat);
    }
    if (points.length == 1) {
        points[points.length] = points[0];
    }

    trip_route = new OpenLayers.Feature.Vector(
        new OpenLayers.Geometry.LineString(points), null, route_style
    )
    displayRoute();
    calculateSimpleTripBuffer(trip_route, map, trip_radius, null, trip_layer);
}
/****************** END GMAP ********************/

/************************* SLIDER ****************************/
onSlideRadius = function(v) {
    var value = v/1000 + ' km';
    $('verbose_radius').innerHTML = value;
}
onChangeRadius = function(v) {
    onSlideRadius(v);
    trip_radius = (v == 0) ? 500 : v;
    if (trip_type != TYPE_DEMAND) {
        calculateSimpleTripBuffer(trip_route, map, trip_radius, null, trip_layer);
    } else {
        displayDepartureRadiusCircle();
        displayArrivalRadiusCircle();
    }
    getTrips(false);
}
var slider = new Control.Slider('handle_radius','track_radius',{
        range: $R(0, 20000),
        values: [0, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000],
        increment: 1000,
        sliderValue: (trip_radius == 500) ? 0 : trip_radius,
        onSlide: onSlideRadius,
        onChange: onChangeRadius
    }
);
observeRadiusLeft('slider_left', slider);
observeRadiusRight('slider_right', slider);

onSlideIntervalMinRadius = function(v) {
    $('verbose_interval_min_radius').innerHTML= ((v==7) ? "-" : "") + (v-7) + 'j';
}
onChangeIntervalMinRadius = function(v) {
    onSlideIntervalMinRadius(v);
    interval_min_radius = v;
    getTrips(false);
}
var slider_interval_min = new Control.Slider('handle_interval_min_radius','track_interval_min_radius',{
        range: $R(0, 7),
        values: [0, 1, 2, 3, 4, 5, 6, 7],
        sliderValue: interval_min_radius,
        onSlide: onSlideIntervalMinRadius,
        onChange: onChangeIntervalMinRadius
    }
);
observeRadiusLeft('slider_interval_min_left', slider_interval_min);
observeRadiusRight('slider_interval_min_right', slider_interval_min);

onSlideIntervalMaxRadius = function(v) {
    $('verbose_interval_max_radius').innerHTML='+' + v + 'j';
}
onChangeIntervalMaxRadius = function(v) {
    onSlideIntervalMaxRadius(v);
    interval_max_radius = v;
    getTrips(false);
}
var slider_interval_max = new Control.Slider('handle_interval_max_radius','track_interval_max_radius',{
        range: $R(0, 7),
        values: [0, 1, 2, 3, 4, 5, 6, 7],
        sliderValue: interval_max_radius,
        onSlide: onSlideIntervalMaxRadius,
        onChange: onChangeIntervalMaxRadius
    }
);
observeRadiusLeft('slider_interval_max_left', slider_interval_max);
observeRadiusRight('slider_interval_max_right', slider_interval_max);

/************* AUTO COMPLETE & FAVORITE PLACES ***************/
callbackDeparture = function(element, query) {
    return callbackDepartureArrival(element, query, 'd', 'id_departure')
}
callbackArrival = function(element, query) {
    return callbackDepartureArrival(element, query, 'a', 'id_arrival')
}
function callbackDepartureArrival(element, query, element_short_id, element_id) {
    var found = false;
    places.keys().each(function(key) {
        if ($('place'+element_short_id+'_'+key).innerHTML == $(element_id+'_name').getValue()) {
            found = true;
            $(element_id+'_point').setValue(places.get(key));
            $(element_id+'_favoriteplace').setValue(key);
        }
    });
    if (!found) {
        $(element_id+'_point').setValue("");
    }
    return query;
}

new Ajax.Autocompleter("id_departure_name", "id_departure_autocomplete", autocomplete_url, {paramName: autocomplete_paramName, callback: callbackDeparture, frequency: autocomplete_frequency, minChars: autocomplete_minChars});
new Ajax.Autocompleter("id_arrival_name", "id_arrival_autocomplete", autocomplete_url, {paramName: autocomplete_paramName, callback: callbackArrival, frequency: autocomplete_frequency, minChars: autocomplete_minChars});

var departurePanel;
var arrivalPanel;
if (places.keys().length > 0) {
    departurePanel = new Panel("id_departure_name", "departure_panel");
    $('departure_panel_show').observe('click', function() {
        departurePanel.toggle.call(departurePanel);
    });
    $('departure_panel_hide').observe('click', function() {
        departurePanel.hide.call(departurePanel);
    });

    arrivalPanel = new Panel("id_arrival_name", "arrival_panel");
    $('arrival_panel_show').observe('click', function() {
        arrivalPanel.toggle.call(arrivalPanel);
    });
    $('arrival_panel_hide').observe('click', function() {
        arrivalPanel.hide.call(arrivalPanel);
    });

    places.keys().each(function(key) {
        $('placed_'+key).observe('click', function(event) {
            selectPlace(event.element(), 'placed', 'id_departure');
        });
        $('placea_'+key).observe('click', function(event) {
            selectPlace(event.element(), 'placea', 'id_arrival');
        });
    });
}

function selectPlace(place_element, place_id_name, element_id) {
    var regex = new RegExp("^"+place_id_name+"_([0-9]+)$");
    var match = regex.exec(place_element.id);
    if (match != null) {
        key = match[1];
        $(element_id+'_name').setValue(place_element.innerHTML);
        $(element_id+'_point').setValue(places.get(key));
        $(element_id+'_favoriteplace').setValue(key);
        if (place_id_name == 'placed') {
            departurePanel.hide.call(departurePanel);
        } else {
            arrivalPanel.hide.call(arrivalPanel);
        }
    }
}

/************************* TOOLTIPS **************************/
new Tip($('help_slider_date'), help_slider_date_tt);
new Tip($('help_slider_radius'), help_slider_radius_tt);
if ($('help_button_save'))
    new Tip($('help_button_save'), help_button_save_tt);

/************************* EVENTS ****************************/
Event.observe(window, 'load', initOL);

$('form_search_trip').observe('submit', function(event) {
    departurePointGeocoder();
    arrivalPointGeocoder();
    map2recenter = true;
    getTrips(true);
    Event.stop(event);
});

if ($('form_save_trip')) {
    $('form_save_trip').observe('submit', function(event) {
		if (trip_type != TYPE_OFFER){
			var verbose_trip_name = gettext("Demand");
			var radius_name = 'id_demand-radius';
		} else {
			var verbose_trip_name = gettext("Offer");
			var radius_name = 'id_offer-radius';
		}
		$('id_departure_city').value = $('id_departure_name').value;
		$('id_arrival_city').value = $('id_arrival_name').value;
		$(radius_name).value = trip_radius;
		$('id_trip_type').value = trip_type;
		$('id_name').value = $('id_departure_name').value + " - " + $('id_arrival_name').value + " (" + verbose_trip_name + ")";
		$('form_search_trip').action = search_trip_url;
		$('form_search_trip').submit();
		Event.stop(event);
//        var departure = $H({
//            'city': $('id_departure_name').getValue(),
//            'point': wkt.write(departure_marker),
//        });
//        var arrival = $H({
//            'city': $('id_arrival_name').getValue(),
//            'point': wkt.write(arrival_marker),
//        });
//        var trip_details = $H({
//            'type': (trip_type == TYPE_DEMAND) ? TYPE_OFFER : TYPE_DEMAND,
//            'departure': departure,
//            'arrival': arrival,
//            'date': $('id_date').getValue(),
//            'interval_min_radius': 7-interval_min_radius,
//            'interval_max_radius': interval_max_radius,
//            'radius': trip_radius
//        });
//        $('trip_details').setValue(trip_details.toJSON());
    });
}



$('id_date').observe('change', function() {
    getTrips(false);
});
