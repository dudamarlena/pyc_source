# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/root_urls.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 252 bytes
__author__ = 'flanker'
from django.conf.urls import include, url
from django.contrib import admin
admin.autodiscover()
urls = [
 url('^repo/', include('moneta.repository.urls')),
 url('^core/', include('moneta.urls', namespace='moneta'))]