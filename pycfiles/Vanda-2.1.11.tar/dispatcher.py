# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/vanda/vanda/apps/multilang/dispatcher.py
# Compiled at: 2013-03-19 08:49:35
import datetime
from django.utils.translation import activate
from django.core.urlresolvers import resolve
from django.conf import settings
from django.http import Http404

def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 31536000
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), '%a, %d-%b-%Y %H:%M:%S GMT')
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)
    return


def set_path(request, path):
    request.path = path
    request.path_info = path
    request.META['PATH_INFO'] = path


def dispatch_url(request, lang=None):
    """
    Dispatch the urls again against the LEAF_URLCONF.
    """
    _lang = lang
    need_cookie = True
    if _lang:
        if request.path.startswith('/%s/' % _lang) or request.path == '/%s' % _lang:
            path = request.path[len(_lang) + 1:]
            request.path = path
            request.path_info = path
            request.META['PATH_INFO'] = path
            if 'lang' in request.GET:
                request.session['django_language'] = request.GET['lang']
                need_cookie = True
    else:
        if settings.LANGUAGE_COOKIE_NAME in request.COOKIES:
            _lang = request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
            request.session['django_language'] = _lang
            need_cookie = False
        elif 'django_language' in request.session:
            _lang = request.session['django_language']
        else:
            _lang = settings.LANGUAGES[0][0]
        try:
            view = resolve(request.path, settings.LEAF_URLCONF)
        except Http404:
            try:
                if not request.path.endswith('/'):
                    request.path = '%s/' % request.path
                    view = resolve(request.path, settings.LEAF_URLCONF)
                else:
                    raise
            except Http404:
                raise

    request.session['django_language'] = _lang
    activate(_lang)
    setattr(settings, 'LANGUAGE_CODE', _lang)
    response = view.func(request, *view.args, **view.kwargs)
    if need_cookie:
        set_cookie(response, settings.LANGUAGE_COOKIE_NAME, _lang)
    return response