# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from django import template
from django.core.urlresolvers import reverse
register = template.Library()

class PaginatorNode(template.Node):
    def __init__(self, pagination, total, current_page, url):
        self.url = url.encode()
        self.pagination = pagination
        self.total = total
        self.current_page = current_page

    def render(self, context):
        page_number = self.total // self.pagination or 1
        output = u""
        for page in range(1, page_number + 1):
            output += "<span%s><a href='%s'>%s</a></span>" % (
                ' class="current"' if page == self.current_page else '', 
                reverse('%s %s' % (self.url, page)), 
                page
            )
        return output

@register.tag
def get_paginator(parser, token):
    """Return a paginator
    
    """
    try:
        name, pagination, total, current_page, url = token.split_contents()
    
    except ValueError:
        raise template.TemplateSyntaxError('bad argument for %r' % token.split_contents()[0])
    return PaginatorNode(int(pagination), int(total), int(current_page), url)
