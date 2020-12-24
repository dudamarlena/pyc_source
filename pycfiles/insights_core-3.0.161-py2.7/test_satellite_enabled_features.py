# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_satellite_enabled_features.py
# Compiled at: 2019-11-14 13:58:15
import doctest, pytest
from insights.parsers import satellite_enabled_features, SkipException
from insights.tests import context_wrap
enabled_features = '\n["ansible","dhcp","discovery",dynflow","logs","openscap","pulp","puppet","puppetca","ssh","templates","tftp"]\n'
empty_enabled_features = '\n[]\n'

def test_HTL_doc_examples():
    satellite_feature = satellite_enabled_features.SatelliteEnabledFeatures(context_wrap(enabled_features))
    globs = {'satellite_features': satellite_feature}
    failed, tested = doctest.testmod(satellite_enabled_features, globs=globs)
    assert failed == 0


def test_features_on_satellite():
    features = satellite_enabled_features.SatelliteEnabledFeatures(context_wrap(enabled_features))
    assert len(features) == 12
    assert features == ['ansible', 'dhcp', 'discovery', 'dynflow', 'logs', 'openscap', 'pulp', 'puppet', 'puppetca', 'ssh', 'templates', 'tftp']


def test_empty_features():
    with pytest.raises(SkipException):
        satellite_enabled_features.SatelliteEnabledFeatures(context_wrap(empty_enabled_features))