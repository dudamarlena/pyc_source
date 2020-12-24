# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Dev\python\django-quickview\docs\examplesite\quickview\__init__.py
# Compiled at: 2013-02-26 03:19:44
# Size of source mod 2**32: 999 bytes
from django.conf.urls import url
from quickview.core_views import *
from quickview.exceptions import *
from quickview.model_views import *
from quickview.utils import *

def register_view(view):
    """

    """
    ViewRegistration.registered_views(view)
    return view


def discover_views(add_auth_pattern=True):
    """
    Discovers all quickviews in all installed apps and adds required urls. Also uses the ViewRegistration-class
    defined above to find information about views created by used the ModelQuickView-class as decorator.
    """
    ViewRegistration.scan_apps()
    urlpatterns = add_auth_pattern and [url('^accounts/login/$', 'django.contrib.auth.views.login', name='login-view'),
     url('^accounts/logout/$', 'django.contrib.auth.views.logout', name='logout-view')] or []
    for view in ViewRegistration.registered_views.values():
        urlpatterns += view.get_urls()

    return tuple(urlpatterns)