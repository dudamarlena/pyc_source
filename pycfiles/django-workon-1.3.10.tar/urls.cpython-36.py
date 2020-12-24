# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/workon/urls.py
# Compiled at: 2018-07-29 15:28:56
# Size of source mod 2**32: 431 bytes
"""
Django-Select2 URL configuration.
Add `django_select` to your ``urlconf`` **if** you use any 'Model' fields::
    url(r'^internal/', include('workon.urls')),
"""
try:
    from django.urls import path, re_path
except:
    from django.conf.urls import url as re_path

from workon.views.select2 import AutoResponseView
urlpatterns = [
 re_path('^fields/auto.json$', (AutoResponseView.as_view()), name='django_select2-json')]