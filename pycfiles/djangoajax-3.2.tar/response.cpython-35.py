# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yceruto/github/yceruto/django-ajax/django_ajax/response.py
# Compiled at: 2017-08-27 12:59:16
# Size of source mod 2**32: 893 bytes
"""
Responses
"""
from __future__ import unicode_literals
from django.conf import settings
from django.http import HttpResponse
from django_ajax.encoder import serialize_to_json

class JSONResponse(HttpResponse):
    __doc__ = '\n    Return a JSON serialized HTTP response\n    '

    def __init__(self, data, *args, **kwargs):
        """
        This returns a object that we send as json content using
        utils.serialize_to_json, that is a wrapper to json.dumps
        method using a custom class to handle models and querysets. Put your
        options to serialize_to_json in kwargs, other options are used by
        response.
        """
        if 'sort_keys' not in kwargs:
            kwargs['sort_keys'] = settings.DEBUG
        super(JSONResponse, self).__init__(content=serialize_to_json(data, *args, **kwargs), content_type='application/json')