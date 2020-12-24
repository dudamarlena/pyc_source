# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/web/util.py
# Compiled at: 2015-09-05 21:24:22
"""Utility functions that don't belong elsewhere.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.
"""
from __future__ import absolute_import, division, print_function
from dossier.fc import FeatureCollection, FeatureTokens, StringCounter, GeoCoords

def fc_to_json(fc):
    if not isinstance(fc, FeatureCollection):
        return fc
    d = {}
    for name, feat in fc.iteritems():
        if isinstance(feat, (unicode, StringCounter, dict)):
            d[name] = feat
        elif isinstance(feat, FeatureTokens):
            d[name] = feat.to_dict()
        elif is_filterable_geo_feature(name, feat):
            d[name] = feat.to_dict()

    return d


def is_filterable_geo_feature(name, feat):
    want = FeatureCollection.GEOCOORDS_PREFIX + 'both_co_LOC_1'
    return isinstance(feat, GeoCoords) and name == want