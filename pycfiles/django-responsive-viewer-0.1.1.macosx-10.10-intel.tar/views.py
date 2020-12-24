# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/django_responsive_viewer/views.py
# Compiled at: 2015-05-18 01:00:20
from django.shortcuts import render
from django.conf import settings

def responsive_listing(request):
    pages_to_show = settings.RESPONSIVE_VIEWER
    layouts = getattr(settings, 'RESPONSIVE_SPECS', [])
    if request.GET.get('select-url'):
        first_url = request.GET.get('select-url')
    else:
        first_url = pages_to_show[0]
    return render(request, 'django_responsive_viewer/listing.html', context={'url_list': pages_to_show, 
       'first_url': first_url, 
       'layouts': layouts})