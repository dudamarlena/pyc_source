# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/django/ploneproxy/authen/backends.py
# Compiled at: 2010-05-27 10:40:05
"""
Django authentication backend implementation for ploneproxy.
"""
import urllib, httplib2
from Cookie import SimpleCookie
from django.db import connection
from django.contrib.auth.models import User
from django.conf import settings
from leocornus.django.ploneproxy.utils import LEOCORNUS_HTTP_HEADER_KEY
from leocornus.django.ploneproxy.utils import LEOCORNUS_HTTP_HEADER_VALUE
from leocornus.django.ploneproxy.authen.models import PloneAuthenState
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class PloneModelBackend(object):
    """
    Authenticates against a Plone site!
    """
    __module__ = __name__

    def authenticate(self, username=None, password=None, loginurl=None):
        ploneCookie = self.authPloneUser(username, password, loginurl)
        if ploneCookie:
            (cookieName, cookieValue) = ploneCookie
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = User.objects.create(username=username)
                user.set_unusable_password()
            else:
                ploneCookie = PloneAuthenState(user_id=user.id, status='valid', cookie_name=cookieName, cookie_value=cookieValue)
                ploneCookie.save()
                return user
        else:
            return
        return

    def authPloneUser(self, username, password, loginurl):
        http = httplib2.Http()
        headers = {}
        headers['Content-type'] = 'application/x-www-form-urlencoded'
        headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers[LEOCORNUS_HTTP_HEADER_KEY] = LEOCORNUS_HTTP_HEADER_VALUE
        login_form = {}
        login_form['__ac_name'] = username
        login_form['__ac_password'] = password
        login_form['cookies_enabled'] = '1'
        login_form['js_enabled'] = '0'
        login_form['form.submitted'] = '1'
        body = urllib.urlencode(login_form)
        try:
            (res, cont) = http.request(loginurl, 'POST', headers=headers, body=body)
        except Exception:
            return

        if res.has_key('set-cookie'):
            cookie = SimpleCookie()
            cookie.load(res['set-cookie'])
            cookieName = settings.PLONEPROXY_COOKIE_NAME
            defaultCookieName = '__ac'
            if cookie.has_key(cookieName):
                cookieValue = cookie.get(cookieName).value
                return (cookieName, cookieValue)
            elif cookie.has_key(defaultCookieName):
                cookieValue = cookie.get(defaultCookieName).value
                return (defaultCookieName, cookieValue)
        return

    def has_perm(self, user_obj, perm):
        return perm in self.get_all_permissions(user_obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True

        return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return

        return