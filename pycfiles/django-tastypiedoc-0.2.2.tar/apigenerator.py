# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/chris/workspace/wifarer/django-tastypiedoc/tastypiedoc/api/apigenerator.py
# Compiled at: 2013-10-16 19:30:53
from ..views import ApiDisplay
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.core.urlresolvers import RegexURLResolver, RegexURLPattern

class ApiGenerator(object):

    def __init__(self, urls=None):
        self.entities = []
        self.api_root = 'api'
        self.make_urls(urls, self.api_root)

    def make_urls(self, url_group, namespace):
        for u in url_group:
            if type(u) == RegexURLPattern:
                self.itemize_pattern(u, namespace)
            if type(u) == RegexURLResolver:
                self.itemize_resolver(u, namespace)

        self.urls = patterns('', url('^$', ApiDisplay(self.entities).index))

    def itemize_resolver(self, resolver, namespace):
        ns = '%s:%s' % (namespace, resolver.namespace)
        self.make_urls(resolver.urlconf_name, ns)

    def itemize_pattern(self, pat, namespace):
        if not pat.name:
            return
        self.entities.append({'namespace': namespace, 
           'name': pat.name})