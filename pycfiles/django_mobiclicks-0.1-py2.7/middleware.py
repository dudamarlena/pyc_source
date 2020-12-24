# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mobiclicks/middleware.py
# Compiled at: 2013-11-28 10:36:39
import urllib, urlparse
from django.http import HttpResponseRedirect
from mobiclicks import conf
from mobiclicks.tasks import confirm_click

class MobiClicksMiddleware(object):
    """
    If a request is redirected from MobiClicks,
    stores the acquisition code in the session
    so that conversions can be tracked later.
    Also does click confirmation if it is enabled.
    """

    def process_request(self, request):
        if conf.CPA_TOKEN_PARAMETER_NAME in request.GET:
            request.session[conf.CPA_TOKEN_SESSION_KEY] = request.GET[conf.CPA_TOKEN_PARAMETER_NAME]
        if conf.CONFIRM_CLICKS and conf.CLICK_REF_PARAMETER_NAME in request.GET:
            confirm_click.delay(request.GET[conf.CLICK_REF_PARAMETER_NAME])

    def process_response(self, request, response):
        """
        Remove the add click-through parameter so that
        the confirmation request isn't duplicated
        when a redirect preserves the querystring
        """
        if isinstance(response, HttpResponseRedirect) and conf.CLICK_REF_PARAMETER_NAME in request.GET:
            url_parts = urlparse.urlparse(response['Location'])
            querydict = urlparse.parse_qs(url_parts.query)
            if conf.CLICK_REF_PARAMETER_NAME in querydict:
                del querydict[conf.CLICK_REF_PARAMETER_NAME]
                new_url_parts = url_parts[:4] + (
                 urllib.urlencode(querydict, True),
                 url_parts[5])
                response['Location'] = urlparse.urlunparse(new_url_parts)
        return response