# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_django/app/views.py
# Compiled at: 2019-02-13 08:31:21
# Size of source mod 2**32: 641 bytes
from django.http import HttpResponse
from opentracing_utils import trace, extract_span_from_django_request, extract_span_from_kwargs

def home(request):
    return HttpResponse('TRACED')


def user(request):
    return HttpResponse('USER')


def error(request):
    raise RuntimeError('Failed request')


def bad_request(request):
    return HttpResponse(status=400)


@trace(span_extractor=extract_span_from_django_request, operation_name='nested_call', pass_span=True)
def nested(request, *args, **kwargs):
    current_span = extract_span_from_kwargs(**kwargs)
    current_span.set_tag('nested', True)
    return HttpResponse('NESTED')