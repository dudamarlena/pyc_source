# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zenobius/Dev/django-apps/django-ikari/ikari/decorators.py
# Compiled at: 2013-08-02 00:03:15
from django.views.decorators.cache import patch_cache_control
from functools import wraps

def never_ever_cache(decorated_function):
    """Like Django @never_cache but sets more valid cache disabling headers.

    @never_cache only sets Cache-Control:max-age=0 which is not
    enough. For example, with max-axe=0 Firefox returns cached results
    of GET calls when it is restarted.
    """

    @wraps(decorated_function)
    def wrapper(*args, **kwargs):
        response = decorated_function(*args, **kwargs)
        patch_cache_control(response, no_cache=True, no_store=True, must_revalidate=True, max_age=0)
        return response

    return wrapper