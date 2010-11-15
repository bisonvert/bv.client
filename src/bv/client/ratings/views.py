# django imports
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponseServerError, HttpResponse, Http404
from django.template import RequestContext
from django.conf import settings

# bvclient imports
from bv.libclient.libratings import LibRatings
from bv.libclient.ext.dj import inject_lib, need_bvoauth_authentication

# ratings imports
from bv.client.ratings.forms import ReportForm
from bv.client.utils.paginator import compute_nb_pages

DEFAULT_ITEMS_PER_PAGE = settings.DEFAULT_ITEMS_PER_PAGE
items_per_page = getattr(settings, 'RATINGS_PER_PAGE', DEFAULT_ITEMS_PER_PAGE)

def render_template(template, context, request):
    return render_to_response(template, context,
    context_instance=RequestContext(request))

@inject_lib(LibRatings)
def list_ratings(request, method, template, template_variable_name="ratings", 
    page=1, extra_context={}, lib=None):
    """Return a simple template with a variable set to the lib method `method`.

    Accepts: 
        * a template_variable_name to set up the name of the variable to set in
          the template.
        * a template name to set up the template to use
        * page for the pagination purposes.
        * extra_context, to set up extra information in the context.

    """
    extra_context[template_variable_name] = getattr(lib, method)()
    extra_context['is_rating'] = True
    return render_template(template,extra_context, request)

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
        'is_rating': True,
    }, request) 
