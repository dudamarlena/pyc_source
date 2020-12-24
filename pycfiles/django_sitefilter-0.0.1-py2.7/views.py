# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sitefilter/views.py
# Compiled at: 2012-11-20 08:29:49
from django.contrib.sites.models import Site
from django.http import Http404, HttpResponseRedirect
from sitefilter.models import get_current_site_filter

def manage(request, id):
    if not request.user.is_staff:
        raise Http404
    sitefilter = get_current_site_filter(request)
    site = Site.objects.get(id=id)
    if site in sitefilter.sites.all():
        sitefilter.sites.remove(site)
    else:
        sitefilter.sites.add(site)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])