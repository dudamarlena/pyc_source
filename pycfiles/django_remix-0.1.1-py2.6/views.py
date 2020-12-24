# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\remix\views.py
# Compiled at: 2009-07-31 16:05:32
from django.shortcuts import render_to_response
from django.template import RequestContext
from remix import *
from remix.models import *

def dashboard(request, url):
    """Renders a dashboard for the given URL to show how remixes were selected."""
    labels = []
    url = '/' + url
    for type in Label.objects.order_by('label'):
        labels.append({'url': url, 
           'label': type.label, 
           'candidates': find_remix_candidates(url, type.label)})

    return render_to_response('remix/dashboard.html', {'url': url, 'labels': labels}, context_instance=RequestContext(request))