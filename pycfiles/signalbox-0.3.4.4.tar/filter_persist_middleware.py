# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/middleware/filter_persist_middleware.py
# Compiled at: 2014-08-27 19:26:12
from django import http

class FilterPersistMiddleware(object):

    def process_request(self, request):
        if '/admin/' not in request.path:
            return
        else:
            if not request.META.has_key('HTTP_REFERER'):
                return
            popup = 'pop=1' in request.META['QUERY_STRING']
            path = request.path
            query_string = request.META['QUERY_STRING']
            session = request.session
            if session.get('redirected', False):
                del session['redirected']
                return
            referrer = request.META['HTTP_REFERER'].split('?')[0]
            referrer = referrer[referrer.find('/admin'):len(referrer)]
            key = 'key' + path.replace('/', '_')
            if popup:
                key = 'popup' + path.replace('/', '_')
            if path == referrer:
                if query_string == '':
                    if session.get(key, False):
                        del session[key]
                    return
                request.session[key] = query_string
            elif session.get(key, False):
                query_string = request.session.get(key)
                redirect_to = path + '?' + query_string
                request.session['redirected'] = True
                return http.HttpResponseRedirect(redirect_to)
            return