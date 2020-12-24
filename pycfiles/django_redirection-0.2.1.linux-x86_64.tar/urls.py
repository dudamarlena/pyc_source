# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/django_redirection/urls.py
# Compiled at: 2014-08-31 08:45:49
""" django_redirector  urls

Providing generate_url function.
"""
from django.conf.urls import patterns, include, url
from django.conf import settings

def generate_url():
    """
    """
    target_urls = {}
    if hasattr(settings, 'DJANGO_REDIRECTER_SUPERUSER'):
        for key, item in settings.DJANGO_REDIRECTER_SUPERUSER.items():
            target_urls[key] = 'superuser'

    if hasattr(settings, 'DJANGO_REDIRECTER_STAFF'):
        for key, item in settings.DJANGO_REDIRECTER_STAFF.items():
            target_urls[key] = 'staff'

    if hasattr(settings, 'DJANGO_REDIRECTER_LOGIN'):
        for key, item in settings.DJANGO_REDIRECTER_LOGIN.items():
            target_urls[key] = 'login'

    if hasattr(settings, 'DJANGO_REDIRECTER_GROUP'):
        for key, item in settings.DJANGO_REDIRECTER_GROUP.items():
            target_urls[key] = 'group'

    urlpatterns = patterns('')
    if hasattr(settings, 'DJANGO_REDIRECTER_EXCEPT'):
        for key, item in settings.DJANGO_REDIRECTER_EXCEPT.items():
            if key[(-1)] != '/':
                key = key + '/'
            urlpatterns += patterns('', url('^%s(?P<suburl>.*)' % key, 'django_redirection.views.redirect_for_exceptions', {'tag': key}))

    for key in sorted(target_urls, key=len, reverse=True):
        if key[(-1)] != '/':
            key = key + '/'
        urlpatterns += patterns('', url('^%s(?P<suburl>.*)' % key, 'django_redirection.views.redirect_with_auth_%s' % target_urls[key], {'tag': key}))

    return urlpatterns