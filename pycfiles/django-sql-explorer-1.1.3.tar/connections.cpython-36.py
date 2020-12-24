# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/connections.py
# Compiled at: 2019-07-02 16:47:10
# Size of source mod 2**32: 836 bytes
from explorer.app_settings import EXPLORER_CONNECTIONS, EXPLORER_DEFAULT_CONNECTION
from django.db import connections as djcs
from django.core.exceptions import ImproperlyConfigured
_connections = {c:c for c in djcs if c in EXPLORER_CONNECTIONS.values() if c in EXPLORER_CONNECTIONS.values()}

class ExplorerConnections(dict):

    def __getitem__(self, item):
        return djcs[item]


connections = ExplorerConnections(_connections)