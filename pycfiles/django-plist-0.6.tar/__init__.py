# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/steingrd/Django/django-plist/django_plist/__init__.py
# Compiled at: 2010-05-19 01:29:02
from itertools import imap
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_array(iterable, as_plist=None):
    if as_plist is not None:
        iterable = imap(as_plist, iterable)
    context = {'array': iterable}
    return render_to_response('django_plist/array.plist', context)


def render_dictionary(dictionary):
    if dictionary is None:
        dictionary = {}
    context = {'dictionary': dictionary}
    return render_to_response('django_plist/dictionary.plist', context)