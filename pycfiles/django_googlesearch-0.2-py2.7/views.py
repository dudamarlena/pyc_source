# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/googlesearch/views.py
# Compiled at: 2015-04-21 15:30:36
from django.http import HttpResponse
from django.template import RequestContext, loader

def cref_cse(request):
    return HttpResponse(loader.render_to_string('googlesearch/cref_cse.xml', {}, context_instance=RequestContext(request)), mimetype='text/xml')