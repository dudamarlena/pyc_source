# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/djangomako/shortcuts.py
# Compiled at: 2008-09-28 17:18:47
from django.http import HttpResponse
import middleware

def render_to_string(template_name, data_dictionary):
    template = middleware.lookup.get_template(template_name)
    result = template.render(**data_dictionary)
    return result


def render_to_response(template_name, data_dictionary, **kwargs):
    """
    Returns a HttpResponse whose content is filled with the result of calling
    lookup.get_template(args[0]).render with the passed arguments.
    """
    return HttpResponse(render_to_string(template_name, data_dictionary), **kwargs)