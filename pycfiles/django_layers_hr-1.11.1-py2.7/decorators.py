# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/layers/decorators.py
# Compiled at: 2018-03-27 03:51:51
from functools import wraps
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import available_attrs
from django.conf import settings
from layers import get_current_layer

def exclude_from_layers(layers):

    def decorator(view_func):

        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(view_or_request, *args, **kwargs):
            request = getattr(view_or_request, 'request', view_or_request)
            layer = get_current_layer(request)
            if layer and layer in layers:
                return render_to_response('layers/exclude_from_layers.html', {'layer': layer, 'request': request})
            return view_func(view_or_request, *args, **kwargs)

        return _wrapped_view

    return decorator