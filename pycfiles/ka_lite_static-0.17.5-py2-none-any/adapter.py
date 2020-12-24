# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/db/backends/spatialite/adapter.py
# Compiled at: 2018-07-11 18:15:30
from django.db.backends.sqlite3.base import Database
from django.contrib.gis.db.backends.adapter import WKTAdapter

class SpatiaLiteAdapter(WKTAdapter):
    """SQLite adaptor for geometry objects."""

    def __conform__(self, protocol):
        if protocol is Database.PrepareProtocol:
            return str(self)