# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/routing.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 1681 bytes
import logging
from mediagoblin.tools.routing import add_route, mount, url_map
from mediagoblin.tools.pluginapi import PluginManager
from mediagoblin.moderation.routing import moderation_routes
from mediagoblin.auth.routing import auth_routes
_log = logging.getLogger(__name__)

def get_url_map():
    add_route('index', '/', 'mediagoblin.views:root_view')
    (
     add_route('terms_of_service', '/terms_of_service', 'mediagoblin.views:terms_of_service'),)
    mount('/auth', auth_routes)
    mount('/mod', moderation_routes)
    import mediagoblin.submit.routing, mediagoblin.user_pages.routing, mediagoblin.edit.routing, mediagoblin.listings.routing, mediagoblin.notifications.routing, mediagoblin.oauth.routing, mediagoblin.api.routing
    for route in PluginManager().get_routes():
        add_route(*route)

    return url_map