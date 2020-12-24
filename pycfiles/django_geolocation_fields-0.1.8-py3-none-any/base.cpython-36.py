# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/thanku/d2eb0a8f-a395-470c-95a2-0c07302a97a5/My Files/Do not Alter/Files/Dambe/Cours/Documents/Mes Cours/C++/Project/django-geolocation-fields/geolocation_fields/models/base.py
# Compiled at: 2020-01-21 17:46:01
# Size of source mod 2**32: 216 bytes
"""
This is the base class for all the Geometric fields we will be creating
"""
import geojson

class BasePoint(geojson.Point):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)