# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/locationExtractor/locationExtractor.py
# Compiled at: 2014-05-15 08:44:31
import pycountry
from locations import Locations

def detect(haystack):
    location = Locations.detect(haystack)
    if location != None:
        location['country'] = pycountry.countries.get(alpha2=location['code']).name
        return location
    else:
        return