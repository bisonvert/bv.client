# django imports
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError, HttpResponse, Http404
from django.template import RequestContext
from django.conf import settings

# bvclient imports
from bvlibclient import LibTalks, LibUsers, LibTrips
from bvlibclient.ext.dj import inject_lib, need_bvoauth_authentication

# bvclient imports
from talks.forms import ContactUserForm

DEFAULT_ITEMS_PER_PAGE = settings.DEFAULT_ITEMS_PER_PAGE
items_per_page = getattr(settings, 'TALKS_PER_PAGE', DEFAULT_ITEMS_PER_PAGE)

@need_bvoauth_authentication()
@inject_lib(LibTalks)
def list_talks(request, page=1, lib=None):
    """Request all the talks of the logged user.

    """
    count = lib.count_talks()
    return render_to_response('list_talks.html', {
        'talks': lib.list_talks(page, items_per_page), 
        'count': count, 
        'page': int(page),
        'listpages': range(1, count // items_per_page +2),
    }, context_instance=RequestContext(request))

@need_bvoauth_authentication()
@inject_lib(LibTalks)
def contact_user(request, trip_id=None, lib=None):
    """Create a new negociation about an announce
    
    Create the negotiation, the message, send a mail to the user trip, and
    redirect user to the list of negociations
    
    If a negociation already exists for this announce and this user (the logged 
    one), redirect the user to the add message view
    
    If one of the email field is empty, redirect user to the contact error view

    This view is only accessible by connected users.

    """
    if lib.talk_exists_for_trip(trip_id):
        return redirect('talks:add_message', int(trip_id))

    if request.POST :
        form = ContactUserForm(data=request.POST)
        if form.is_valid():
            talk_id = lib.create_talk(trip_id, form.cleaned_data['message'])
            return redirect('talks:list_messages', talk_id)
    else:
        # check if a conversation about this trip already exists
        form = ContactUserForm()
    
    libtrips = LibTrips(**lib.get_params())
    trip  = libtrips.get_trip(trip_id)

    return render_to_response('contact_user.html', {
        'from_user' : request.bvuser,
        'to_user' : trip.user,
        'form' : form,
        'trip': trip,
    }, context_instance=RequestContext(request))

@need_bvoauth_authentication()
@inject_lib(LibTalks)
def list_messages(request, page=1, talk_id=None, lib=None):
    """Add a message to an existing talk.
    
    """
    if request.POST:
        form = ContactUserForm(data=request.POST)
        if form.is_valid():
            lib.add_message_to_talk(talk_id=talk_id, 
                message=form.cleaned_data['message'])
            return redirect("talks:list_messages", talk_id)
    else:
        form = ContactUserForm()
    
    talk = lib.get_talk(talk_id)
    messages = lib.list_talk_messages(talk_id)
    
    if request.bvuser.id == talk.from_user.id:
        to_user = talk.trip.user
    else:
        to_user = talk.from_user

    return render_to_response('list_messages.html', {
        'to_user' : to_user,
        'talk' : talk,
        'form' : form,
        'messages': messages,
    }, context_instance=RequestContext(request))

@need_bvoauth_authentication()
@inject_lib(LibTalks)
def cancel_talk(request, talk_id=None, lib=None):
    """Cancel the negociation talk.

    Cancelling a negociation talk must have a reason, so we use the contact
    form.

    """
    if request.POST:
        form = ContactUserForm(data=request.POST)
        if form.is_valid():
            lib.delete_talk(talk_id, form.cleaned_data['message'])
            return redirect("talks:list")
    else:
        form = ContactUserForm()

    talk = lib.get_talk(talk_id)
    return render_to_response('cancel_talk.html', {
        'talk' : talk,
        'form' : form,
    }, context_instance=RequestContext(request))

@need_bvoauth_authentication()
@inject_lib(LibTalks)
def validate_talk(request, talk_id=None, lib=None):
    """Validate the talk

    """
    lib.validate_talk(talk_id)
    return redirect('talks:confirm_validate')
