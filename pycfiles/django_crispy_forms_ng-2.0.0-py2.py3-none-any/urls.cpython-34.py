# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-crispy-forms/django-crispy-forms-ng/crispy_forms/tests/urls.py
# Compiled at: 2015-04-08 06:40:44
# Size of source mod 2**32: 292 bytes
import django
if django.VERSION >= (1, 5):
    from django.conf.urls import patterns, url
else:
    from django.conf.urls.defaults import patterns, url

def simpleAction(request):
    pass


urlpatterns = patterns('', url('^simple/action/$', simpleAction, name='simpleAction'))