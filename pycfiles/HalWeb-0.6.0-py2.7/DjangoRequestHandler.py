# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/halicea/DjangoRequestHandler.py
# Compiled at: 2011-12-23 04:19:50
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from lib.halicea.HalRequestHandler import HalRequestHandler

class DjangoRequestHandler(HalRequestHandler):

    def __init__(self, *args, **kwargs):
        super(DjangoRequestHandler, self).__init__(*args, **kwargs)

    def __call__(self, request, *args, **kwargs):
        request = request
        response = HttpResponse()
        setattr(response, 'headers', response._headers)
        self.initialize(request, response)
        if self.request.method == 'POST':
            return self.post()
        else:
            if self.request.method == 'GET':
                return self.get()
            return

    def __respond(self, text):
        self.response.content = text
        return self.response

    def __redirect(self, uri, *args):
        return HttpResponseRedirect(uri, *args)