# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8 :

from django import template

#python imports
import copy
import time
import datetime

register = template.Library()

@register.filter
def api_to_date(value):
    """Convert a date from YYY-MM-DD format to a real python date object.
    
    """
    return datetime.date(*time.strptime(value, '%Y-%m-%d')[:3])
    
@register.filter
def api_to_time(value):
    """Convert a date from  format to a real python datetime object.
    
    """
    if value is None:
        return None
    return datetime.time(*time.strptime(value, '%H:%M:%S')[3:6])
