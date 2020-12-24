# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/django_common/lib/python2.7/site-packages/django_common/http.py
# Compiled at: 2012-03-11 19:20:35
from StringIO import StringIO
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect, HttpResponseRedirect, Http404
from django.utils import simplejson

class JsonResponse(HttpResponse):

    def __init__(self, data={}, errors=[], success=True):
        """
    data is a map, errors a list
    """
        json = json_response(data=data, errors=errors, success=success)
        super(JsonResponse, self).__init__(json, mimetype='application/json')


def json_response(data={}, errors=[], success=True):
    data.update({'errors': errors, 
       'success': len(errors) == 0 and success})
    return simplejson.dumps(data)


class XMLResponse(HttpResponse):

    def __init__(self, data):
        """
    data is the entire xml body/document
    """
        super(XMLResponse, self).__init__(data, mimetype='text/xml')