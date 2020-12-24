# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: _geoip_geolite2/__init__.py
# Compiled at: 2018-11-20 12:15:09
import os
database_name = 'GeoLite2-City.mmdb'

def loader(database, mod):
    filename = os.path.join(os.path.dirname(__file__), database_name)
    return mod.open_database(filename)