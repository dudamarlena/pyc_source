# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/meringue/decorators.py
# Compiled at: 2015-08-17 17:37:49
from functools import update_wrapper
from django.http import HttpResponseRedirect, HttpResponseForbidden

class CheckAccount(object):
    """
    "По образу и подобию django.contrib.auth.decorators._CheckLogin"(c)
    """

    def __init__(self, view_func, test_func, redirect_url=None):
        self.view_func = view_func
        self.test_func = test_func
        self.redirect_url = redirect_url
        update_wrapper(self, view_func)

    def __get__(self, obj, cls=None):
        view_func = self.view_func.__get__(obj, cls)
        return CheckAccount(view_func, self.test_func, self.redirect_url)

    def __call__(self, request, *args, **kwargs):
        if self.test_func(request.user):
            return self.view_func(request, *args, **kwargs)
        if self.redirect_url:
            return HttpResponseRedirect(self.redirect_url)
        return HttpResponseForbidden()


def anonymous_required(function=None, redirect_url=None):
    t = lambda u: u.is_anonymous()
    decorator = lambda f: CheckAccount(f, t, redirect_url)
    if function:
        return decorator(function)
    return decorator