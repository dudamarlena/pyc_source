# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/settings.py
# Compiled at: 2019-10-15 04:50:26
import os, sys
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CURRENT_MODULE = sys.modules[__name__]
DEBUG = False
READ_ONLY = False
AUTO_OPEN_REGISTER = True
WEB_BASE_URL = None
API_BASE_URL = None
DATABASE_ENGINE = None
DATABASE_HOST = None
DATABASE_PORT = None
DATABASE_USER = None
DATABASE_PASSWORD = None
DATABASE_NAME = None
DATABASE_EXTRA = None
DATABASE_CONNECTIONS = None

def set_settings(settings):
    for key, value in settings.items():
        setattr(CURRENT_MODULE, key, value)