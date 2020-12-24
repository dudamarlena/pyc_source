# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/basic/middleware/bot404.py
# Compiled at: 2018-03-27 09:45:07
# Size of source mod 2**32: 950 bytes
from django.conf import settings
from django.http import Http404

class Bot404Middleware(object):

    def __init__(self, get_response=None):
        if get_response:
            self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        enabled = getattr(settings, 'DJANGOCMS_MISC_BOT404', None)
        user_agent = getattr(request, 'user_agent', None)
        if enabled:
            if user_agent:
                if user_agent.is_bot:
                    raise Http404