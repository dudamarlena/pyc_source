# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/utilities/error_views.py
# Compiled at: 2014-08-27 19:26:12
from django.http import *
from django.template import *
from django.template.loader import get_template
from django.template import RequestContext

def render_error_response(message='A system error occured.'):
    """Display a 500 error page with a message"""
    t = get_template('500.html')
    c = Context({'message': message})
    return HttpResponseServerError(t.render(c))


def render_forbidden_response(message="You're not allowed to do that."):
    """Display a 403 error page with a message"""
    t = get_template('500.html')
    c = Context({'message': message})
    return HttpResponseForbidden(t.render(c))