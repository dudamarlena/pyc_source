# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_apps/tethys_apps/base/controller.py
# Compiled at: 2014-11-13 14:51:49
from .url_map import UrlMapBase

def app_controller_maker(root_url):
    """
    Returns an AppController class that is bound to a specific root url. This method is deprecated. Use url_map_maker.
    """
    properties = {'root_url': root_url}
    return type('UrlMap', (UrlMapBase,), properties)