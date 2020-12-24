# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/content_negotiation.py
# Compiled at: 2019-08-16 17:27:44
from __future__ import absolute_import
from rest_framework.negotiation import DefaultContentNegotiation
from rest_framework.parsers import FormParser, MultiPartParser

class ConditionalContentNegotiation(DefaultContentNegotiation):
    """
    Overrides the parsers on POST to support file uploads.
    """

    def select_parser(self, request, parsers):
        if request.method == 'POST':
            parsers = [
             FormParser(), MultiPartParser()]
        return super(ConditionalContentNegotiation, self).select_parser(request, parsers)