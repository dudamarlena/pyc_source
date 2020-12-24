# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/urlographer/sample_views.py
# Compiled at: 2013-06-26 14:11:51
from django.http import HttpResponse
from django.views.generic.base import View

def sample_view(request, **kwargs):
    return HttpResponse('test value=' + kwargs['test_val'])


class SampleClassView(View):
    test_val = 'not set'

    def get(self, request, *args, **kwargs):
        return HttpResponse('test value=' + self.test_val)


def sample_handler(request, response):
    response.content = 'modified content'
    return response


class SampleClassHandler(View):

    def get(self, request, response, *args, **kwargs):
        response.content = 'payment required'
        return response