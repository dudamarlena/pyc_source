# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/dprofiling/tests/views.py
# Compiled at: 2013-05-14 10:50:47
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View

class HelloWorld(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello World!')


class ExceptionView(View):

    def get(self, request, *args, **kwargs):
        raise Exception('Unhandled view exception')


class NotFoundView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponseNotFound('Not found')