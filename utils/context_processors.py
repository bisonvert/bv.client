# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from django.conf import settings
import re

"""Context processors

Add variables to context for RequestContect responses  and generic views

A Context Processor must be added into settings
::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'myapp.mycontextprocessors.mycontextprocessor',
    )
    
Here's how to use the context processors
::

    from django.template import RequestContext
    from django.shortcuts import render_to_response

    return render_to_response('path/to/template.html', {
        'foo': bar, 
        'blah': toto
    }, context_instance=RequestContext(request))

"""

def admin_media_url(request):
    """ADMIN_MEDIA_URL: URL d'accès aux media admin."""
    return {
        'ADMIN_MEDIA_URL': settings.ADMIN_MEDIA_PREFIX
    }

def js_ext(request):
    """JS_EXT: Extension des fichiers javascript: .js ou -min.js en fonction
    du paramétrage.

    """
    return {
        'JS_EXT': settings.JS_EXT
    }
