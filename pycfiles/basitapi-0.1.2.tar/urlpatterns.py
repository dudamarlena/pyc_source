# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/DjangoProjects/basitapi/basitapi/urlpatterns.py
# Compiled at: 2013-01-16 05:18:32
from django.conf.urls import url
from django.core.urlresolvers import RegexURLPattern

def format_suffix_patterns(urlpatterns, replace=False):
    suffix_pattern = '\\.(?P<format>[a-z]+)$'
    ret = []
    for urlpattern in urlpatterns:
        regex = urlpattern.regex.pattern.rstrip('$') + suffix_pattern
        ret.append(RegexURLPattern(regex, urlpattern.callback, default_args=urlpattern.default_args, name=urlpattern.name))
        if replace == False:
            ret.append(urlpattern)

    return ret