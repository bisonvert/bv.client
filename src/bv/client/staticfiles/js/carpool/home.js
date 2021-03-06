var geocoder;
var departure_request, departure_found, arrival_request, arrival_found;

Event.observe(window, 'load', function() {
    $('id_departure').focus();
    geocoder = new GClientGeocoder();
});

get_departure_point = function(point) {
    departure_request = true;
    if (!point) {
        alert(gettext("ERROR : Departure address not found."));
        departure_found = false;
    } else {
        departure_found = true;
        $('id_departure_point').setValue('POINT(' + point.lng() + ' ' + point.lat() + ')');
    }
};
get_arrival_point = function(point) {
    arrival_request = true;
    if (!point) {
        alert(gettext("ERROR : Arrival address not found."));
        arrival_found = false;
    } else {
        arrival_found = true;
        $('id_arrival_point').setValue('POINT(' + point.lng() + ' ' + point.lat() + ')');
    }
};

function checkFields(btn_element_id, type_value, event) {
    if ($('id_departure').getValue() && $('id_arrival').getValue()) {
        if (!$('id_departure_point').getValue()) {
            departure_request = false;
            geocoder.getLatLng(
                $('id_departure').getValue(),
                get_departure_point
            );
        } else {
            departure_request = true;
            departure_found = true;
        }
        if (!$('id_arrival_point').getValue()) {
            arrival_request = false;
            geocoder.getLatLng(
                $('id_arrival').getValue(),
                get_arrival_point
            );
        } else {
            arrival_request = true;
            arrival_found = true;
        }
        submitForm(btn_element_id, type_value);
    } else {
        alert(gettext("Please fill Departure and Arrival fields."));
    }
    if (undefined !== event) {
        Event.stop(event);
    }
}

function submitForm(btn_element_id, type_value) {
    if (departure_request && arrival_request) {
        if (departure_found && arrival_found) {
            $('id_type').setValue(type_value);
            $('quick_search_form').submit();
        }
    } else {
        setTimeout("submitForm('"+btn_element_id+"',"+type_value+");", 100);
    }
}

$('btn_search_demand').observe('click', function(event) {
    // 1: TYPE_OFFER
    checkFields('btn_search_demand', 0);
})

$('quick_search_form').observe('submit', function(event) {
    // 1: TYPE_DEMAND
    checkFields('btn_search_offer', 1, event);
})

callbackDeparture = function(element, query) {
    return callbackDepartureArrival(element, query, 'd', 'id_departure')
}
callbackArrival = function(element, query) {
    return callbackDepartureArrival(element, query, 'a', 'id_arrival')
}
function callbackDepartureArrival(element, query, element_short_id, element_id) {
    var found = false;
    places.keys().each(function(key) {
        if ($('place'+element_short_id+'_'+key).innerHTML == $(element_id).getValue()) {
            found = true;
            $(element_id+'_point').setValue(places.get(key));
//            $(element_id+'_favoriteplace').setValue(key);
        }
    });
    if (!found) {
        $(element_id+'_point').setValue("");
//        $(element_id+'_favoriteplace').setValue("");
    }
    return query;
}

if (with_autocomplete) {
    new Ajax.Autocompleter("id_departure", "id_departure_autocomplete", autocomplete_url, {paramName: autocomplete_paramName, callback: callbackDeparture, frequency: autocomplete_frequency, minChars: autocomplete_minChars});
    new Ajax.Autocompleter("id_arrival", "id_arrival_autocomplete", autocomplete_url, {paramName: autocomplete_paramName, callback: callbackArrival, frequency: autocomplete_frequency, minChars: autocomplete_minChars});
}

var departurePanel;
var arrivalPanel;
if (places.keys().length > 0) {
    departurePanel = new Panel("id_departure", "departure_panel");
    $('departure_panel_show').observe('click', function() {
        departurePanel.toggle.call(departurePanel);
    });
    $('departure_panel_hide').observe('click', function() {
        departurePanel.hide.call(departurePanel);
    });

    arrivalPanel = new Panel("id_arrival", "arrival_panel");
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
        $(element_id).setValue(place_element.innerHTML);
        $(element_id+'_point').setValue(places.get(key));
        $(element_id+'_favoriteplace').setValue(key);
        if (place_id_name == 'placed') {
            departurePanel.hide.call(departurePanel);
        } else {
            arrivalPanel.hide.call(arrivalPanel);
        }
    }
}
