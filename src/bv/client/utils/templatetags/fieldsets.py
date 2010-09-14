# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from django import template
from django import forms
from django.utils.datastructures import SortedDict


#python imports
import copy

register = template.Library()

class FieldSetNode(template.Node):
    def __init__(self, fields, destination_form, source_form):
        """Initialize a new FieldSetNode, where:
           * fields is the list of fields we want
           * destination_form is the name of the new form we want
           * source_form is the name of the form to look into.
        """
        self.fields = fields
        self.destination_form = destination_form
        self.source_form = source_form

    def render(self, context):
        try:
            form = template.Variable(self.source_form).resolve(context)
        except template.VariableDoesNotExist:
            raise template.TemplateSyntaxError('the variable %s is not assigned in the context' % self.source_form)

        new_form = copy.copy(form)
        new_form.fields = SortedDict([(key, form.fields[key]) for key in self.fields if key in form.fields])

        context[self.destination_form] = new_form

        return u''

@register.tag
def get_fieldset(parser, token):
    """Render given fields of a form as a subform.
    
    Usage ::
        
        {% get_fieldset name,password,etc as newform from form %}
    
    """
    try:
        name, fields, as_, variable_name, from_, form = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('bad arguments for %r'  % token.split_contents()[0])
    return FieldSetNode(fields.split(','), variable_name, form)
    

