# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/jmbo-and-friends/jmbo-analytics/jmbo_analytics/views/google_analytics.py
# Compiled at: 2016-08-25 04:11:26
import struct
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.conf import settings
from jmbo_analytics.utils import build_ga_params, set_cookie
from jmbo_analytics.tasks import send_ga_tracking
GIF_DATA = reduce(lambda x, y: x + struct.pack('B', y), [
 71, 73, 70, 56, 57, 97,
 1, 0, 1, 0, 128, 0,
 0, 0, 0, 0, 255, 255,
 255, 33, 249, 4, 1, 0,
 0, 0, 0, 44, 0, 0,
 0, 0, 1, 0, 1, 0,
 0, 2, 1, 68, 0, 59], '')

@never_cache
def google_analytics(request):
    """Image that sends data to Google Analytics."""
    response = HttpResponse('', 'image/gif', 200)
    response.write(GIF_DATA)
    if hasattr(settings, 'GOOGLE_ANALYTICS_IGNORE_PATH'):
        exclude = [ p for p in settings.GOOGLE_ANALYTICS_IGNORE_PATH if request.path.startswith(p) ]
        if any(exclude):
            return response
    event = request.GET.get('event', None)
    if event:
        event = event.split(',')
    path = request.path
    referer = request.META.get('HTTP_REFERER', '')
    params = build_ga_params(request, path, event, referer)
    send_ga_tracking.delay(params)
    set_cookie(params, response)
    return response