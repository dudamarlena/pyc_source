# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/ssi/views.py
# Compiled at: 2011-05-27 11:48:21
from django.http import HttpResponse
from django.template import Template, RequestContext
from django.core.cache import cache

def render_from_cache(request, cache_key):
    template = Template(cache.get(cache_key, ''))
    context = cache.get('%s:context' % cache_key, {})
    request_context = RequestContext(request, context)
    return HttpResponse(template.render(request_context))