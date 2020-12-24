# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yceruto/github/yceruto/django-ajax/django_ajax/middleware.py
# Compiled at: 2017-08-27 12:59:16
# Size of source mod 2**32: 753 bytes
"""
Middleware
"""
from __future__ import unicode_literals
from django_ajax.shortcuts import render_to_json

class AJAXMiddleware(object):
    __doc__ = '\n    AJAX Middleware that decides when to convert the response to JSON.\n    '

    def process_response(self, request, response):
        """
        If the request was made by AJAX then convert response to JSON,
        otherwise return the original response.
        """
        if request.is_ajax():
            return render_to_json(response)
        return response

    def process_exception(self, request, exception):
        """
        Catch exception if the request was made by AJAX,
        after will become up on JSON.
        """
        if request.is_ajax():
            return exception