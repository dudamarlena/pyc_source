# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/lib/substrate/agar/env.py
# Compiled at: 2012-02-28 10:17:47
"""
The ``agar.env`` module contains a number of constants to help determine which environment code is running in.
"""
import os
from google.appengine.api.app_identity import get_application_id
from google.appengine.api import apiproxy_stub_map
server_software = os.environ.get('SERVER_SOFTWARE', '')
have_appserver = bool(apiproxy_stub_map.apiproxy.GetStub('datastore_v3'))
appid = None
if have_appserver:
    appid = get_application_id()
else:
    try:
        project_dirname = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        project_dir = os.path.abspath(project_dirname)
        from google.appengine.tools import dev_appserver
        appconfig, matcher, from_cache = dev_appserver.LoadAppConfig(project_dir, {})
        appid = appconfig.application
    except ImportError:
        dev_appserver = None
        appid = None

on_development_server = bool(have_appserver and (not server_software or server_software.lower().startswith('devel')))
on_server = bool(have_appserver and appid and server_software and not on_development_server)
on_integration_server = on_server and appid.lower().endswith('-int')
on_production_server = on_server and not on_integration_server