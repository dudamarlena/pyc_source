# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/scaler/middleware.py
# Compiled at: 2012-05-31 03:57:34
import time, re
from django.http import HttpResponseRedirect
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.conf import settings
_cache = {}
_request_response_times = {}
SERVER_BUSY_URL = reverse(settings.DJANGO_SCALER.get('server_busy_url_name', 'server-busy'))

def redirect_n_slowest_dummy():
    return 0


def redirect_n_slowest_from_cache():
    """Simple retrieval from whatever cache is in use"""
    return cache.get('django_scaler_n_slowest')


def redirect_percentage_slowest_dummy():
    return 0


def redirect_percentage_slowest_from_cache():
    return cache.get('django_scaler_percentage_slowest')


def redirect_regexes_dummy():
    return []


def redirect_regexes_from_cache():
    return cache.get('django_scaler_regexes')


class ScalerMiddleware:
    """Add as the first middleware in your settings file"""

    def process_request(self, request):
        if request.is_ajax() or request.META['PATH_INFO'] == SERVER_BUSY_URL:
            return
        else:
            n_slowest = settings.DJANGO_SCALER.get('redirect_n_slowest_function', redirect_n_slowest_dummy)()
            percentage_slowest = settings.DJANGO_SCALER.get('redirect_percentage_slowest_function', redirect_percentage_slowest_dummy)()
            regexes = settings.DJANGO_SCALER.get('redirect_regexes_function', redirect_regexes_dummy)()
            if not request.is_ajax():
                if n_slowest or percentage_slowest:
                    paths = sorted(_request_response_times, key=_request_response_times.__getitem__, reverse=True)
                if n_slowest:
                    li = paths[:n_slowest]
                    if request.META['PATH_INFO'] in li:
                        return HttpResponseRedirect(SERVER_BUSY_URL)
                if percentage_slowest:
                    n = int(round(percentage_slowest / 100.0 * len(paths)))
                    li = paths[:n]
                    if request.META['PATH_INFO'] in li:
                        return HttpResponseRedirect(SERVER_BUSY_URL)
                if regexes:
                    for regex in regexes:
                        m = re.match('%s' % regex, request.META['PATH_INFO'])
                        if m is not None:
                            return HttpResponseRedirect(SERVER_BUSY_URL)

            now = time.time()
            setattr(request, '_django_scaler_stamp', now)
            prefix = request.META['PATH_INFO'] + '-scaler-'
            key_stamp = prefix + 'stamp'
            key_hits = prefix + 'hits'
            key_trend = prefix + 'trend'
            key_redir = prefix + 'redir'
            stamp = _cache.get(key_stamp, 0)
            hits = _cache.get(key_hits, 0)
            trend = _cache.get(key_trend, [])
            redir = _cache.get(key_redir, now)
            if hits > settings.DJANGO_SCALER.get('trend_size', 100):
                avg = stamp * 1.0 / hits
                _request_response_times[request.META['PATH_INFO']] = avg
                slow_threshold = settings.DJANGO_SCALER.get('slow_threshold', 4.0)
                if sum(trend) * 1.0 / len(trend) > avg * slow_threshold:
                    redirect_for = settings.DJANGO_SCALER.get('redirect_for', 60)
                    if now - redir > redirect_for:
                        try:
                            del _cache[key_redir]
                        except KeyError:
                            pass
                        else:
                            _cache[key_trend] = []
                    else:
                        delattr(request, '_django_scaler_stamp')
                        _cache.setdefault(key_redir, now)
                        return HttpResponseRedirect(SERVER_BUSY_URL)
            return

    def process_response(self, request, response):
        t = getattr(request, '_django_scaler_stamp', None)
        if t is not None:
            diff = int((time.time() - t) * 1000)
            prefix = request.META['PATH_INFO'] + '-scaler-'
            key_stamp = prefix + 'stamp'
            key_hits = prefix + 'hits'
            key_trend = prefix + 'trend'
            stamp = _cache.get(key_stamp, 0)
            hits = _cache.get(key_hits, 0)
            trend = _cache.get(key_trend, [])
            _cache[key_stamp] = stamp + diff
            _cache[key_hits] = hits + 1
            trend_size = settings.DJANGO_SCALER.get('trend_size', 100)
            _cache[key_trend] = (trend + [diff])[-trend_size:]
        return response