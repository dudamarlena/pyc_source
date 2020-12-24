# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jon/Documents/TiddlyWiki/Trunk/contributors/JonRobson/TiddlyWeb/plugins/geofilters/test/test_example.py
# Compiled at: 2010-04-12 06:30:51
"""
Test geotiddlers
test script provided by psd
"""
from tiddlyweb.model.tiddler import Tiddler
import tiddlywebplugins.geofilters as geofilters, gitscob
bag = gitscob.bag()
tiddlers = list(bag.gen_tiddlers())

def test_geoproximity():
    (match, distance) = geofilters.geoproximity(51.5, -0.12, 360, 48.85, 2.35, units='kms')
    assert match is True
    assert '%.0f' % distance == '343'
    (match, distance) = geofilters.geoproximity(51.5, -0.12, 224, 48.85, 2.35, units='miles')
    assert '%.0f' % distance == '213'


def test_geo_near_tiddlers():
    tiddler = Tiddler('North Sea', bag='gitscob')
    tiddler.fields = {'geo.lat': '55.0', 'geo.long': '1.9'}
    found = list(geofilters.geo_near_tiddlers(55.0, 1.9, 1.0, [tiddler]))
    assert len(found) == 1
    assert found[0].fields['_geo.proximity'] == '0.00'
    found = list(geofilters.geo_near_tiddlers(55.23636, -6.50888, 1.0, tiddlers))
    assert len(found) == 1
    found = list(geofilters.geo_near_tiddlers(55.86, -3.733, 25, tiddlers, 'miles'))
    assert len(found) == 2
    found = list(geofilters.geo_near_tiddlers(49.916, -6.41, 100, tiddlers, 'miles'))
    assert len(found) == 3