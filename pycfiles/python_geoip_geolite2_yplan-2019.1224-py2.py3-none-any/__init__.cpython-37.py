# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/geolite2/_geoip_geolite2/__init__.py
# Compiled at: 2019-02-25 04:53:22
# Size of source mod 2**32: 187 bytes
import os
database_name = 'GeoLite2-City.mmdb'

def loader(database, mod):
    filename = os.path.join(os.path.dirname(__file__), database_name)
    return mod.open_database(filename)