# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/atulvarma/Documents/18f/django-uswds-forms/example/app/views.py
# Compiled at: 2017-05-12 18:22:47
# Size of source mod 2**32: 823 bytes
from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import render
from collections import OrderedDict
from .example import Example
EXAMPLE_NAMES = [
 'radios',
 'checkboxes',
 'date',
 'errors',
 'everything']
EXAMPLES = OrderedDict([(name, Example(name)) for name in EXAMPLE_NAMES])

def ctx(**kwargs):
    return {**{'EXAMPLES':EXAMPLES, 
     'DOCS_URL':settings.DOCS_URL}, **kwargs}


def example(request, name):
    example = EXAMPLES.get(name)
    if example is None:
        return HttpResponseNotFound('Example not found.')
    else:
        return render(request, 'example.html', ctx(rendered_example=(example.render(request)),
          example=example))


def home(request):
    return render(request, 'home.html', ctx())