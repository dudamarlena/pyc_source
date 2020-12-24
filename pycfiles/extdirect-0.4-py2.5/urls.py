# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/extdirect/django/urls.py
# Compiled at: 2009-09-20 21:52:30
from django.conf.urls.defaults import *
import registry

class UrlPatterns(object):

    def __iter__(self):
        urls = []
        for (klass, name, ns) in registry.classes():
            print klass, name, ns
            regex = '%s/$' % name
            urls.append((regex, klass()))

        return (x for x in patterns('', *urls))


urlpatterns = UrlPatterns()