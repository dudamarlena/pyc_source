# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/fc/tests/test_geocoords.py
# Compiled at: 2015-09-05 21:22:50
"""tests for GeoCoords

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.
"""
from dossier.fc import FeatureCollection
from dossier.fc.geocoords import GeoCoords, GeoCoordsSerializer

def test_geo_fcdefault():
    fc = FeatureCollection()
    assert isinstance(fc['!co_LOC'], GeoCoords)


def test_geo_default():
    fo = GeoCoords()
    assert fo['foo'] == []


def test_geo_roundtrip():
    fc = FeatureCollection()
    fc['!co_LOC']['foo'].append((-55, 22, 0, None))
    fc2 = FeatureCollection.loads(fc.dumps())
    assert fc['!co_LOC'] == fc2['!co_LOC']
    return


def test_geocoords():
    data = {'Boston': [(-72, 44, 2, None), (99, -22.0, None, 1434218285)]}
    geo = GeoCoords(data)
    out = GeoCoordsSerializer.dumps(geo)
    geo2 = GeoCoordsSerializer.loads(out)
    assert geo is not geo2
    assert geo == geo2
    return