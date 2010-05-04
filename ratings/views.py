# django imports
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError, HttpResponse, Http404
from django.template import RequestContext
from django.conf import settings

# bvclient imports
from bvlibclient import LibRatings, LibUsers
from bvlibclient.ext.dj import inject_lib, need_bvoauth_authentication

# ratings imports
from ratings.forms import ReportForm

DEFAULT_ITEMS_PER_PAGE = settings.DEFAULT_ITEMS_PER_PAGE
items_per_page = getattr(settings, 'RATINGS_PER_PAGE', DEFAULT_ITEMS_PER_PAGE)

def render_template(template, context, request):
    return render_to_response(template, context,
    context_instance=RequestContext(request))

@inject_lib(LibRatings)
def list_ratings(request, method, template, template_variable_name="ratings", page=1, lib=None):
    """Return a simple template with a variable set to the lib method `method`.

    """
    objects = getattr(lib, method)()
    return render_template(template,{template_variable_name: objects}, request)

@inject_lib(LibRatings)
def rate_user(request, temprating_id=None, lib=None):
    if request.POST:
        form = ReportForm(data=request.POST)
        if form.is_valid():
            lib.rate_user(temprating_id, mark=form.cleaned_data['mark'], 
                comment=form.cleaned_data['comment'])
            return redirect('ratings:list')
    else:
        form = ReportForm()
    
    temprating = lib.get_temprating(temprating_id)

    return render_template('ratings/rate_user.html', {
        'form':form,
        'tempreport': temprating,
    }, request) 
