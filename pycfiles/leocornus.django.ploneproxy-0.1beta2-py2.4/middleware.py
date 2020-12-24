# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/leocornus/django/ploneproxy/authen/middleware.py
# Compiled at: 2010-05-18 09:02:18
"""
middlewares for the leocornus.django.ploneproxy.authen
"""
from mod_python import Cookie
from leocornus.django.ploneproxy.authen.models import PloneAuthenState
__author__ = 'Sean Chen'
__email__ = 'sean.chen@leocorn.com'

class PloneCookieMiddleware(object):
    """
    this middleware is try to issue the plone cookie at the first
    right time!
    This middleare is depends on SessionMiddleware and
    AuthenticationMiddleare.  And it should located before those
    2 middlewares.
    """
    __module__ = __name__

    def process_response(self, request, response):
        """
        This is the response within Django context.  If this is success
        response, we should set up cookie so the mod_python request
        has everything ready to go!
        
        check the plone authentecation state table to see if there is newer cookie
        issued for this user?
        - if there is newer cookie, set up the newer cookie.  Normally,
          this only happens when user log in successfully!
          - once set up the newer cookie, we will remove the object from
            the PloneAuthenState.
        - if there is no newer cookie, continue!
        """
        if hasattr(request, 'user') and request.user.is_authenticated():
            try:
                state = PloneAuthenState.objects.get(user_id=request.user.id)
                response.set_cookie(str(state.cookie_name), state.cookie_value, path='/')
                state.delete()
            except PloneAuthenState.DoesNotExist:
                pass

        return response