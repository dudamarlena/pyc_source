# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sat5_insights_properties.py
# Compiled at: 2019-05-16 13:41:33
import pytest, doctest
from insights.tests import context_wrap
from insights.parsers import sat5_insights_properties, SkipException
from insights.parsers.sat5_insights_properties import Sat5InsightsProperties
INSIGHTS_PROPERTIES = ('\nportalurl = https://cert-api.access.redhat.com/r/insights\nenabled = true\ndebug = true\nrpmname = redhat-access-insights\n').strip()

def test_insights_properties():
    result = Sat5InsightsProperties(context_wrap(INSIGHTS_PROPERTIES))
    assert result['enabled'] == 'true'
    assert result.enabled is True
    assert result.get('debug') == 'true'
    assert result.get('rpmname') == 'redhat-access-insights'
    assert result['rpmname'] == 'redhat-access-insights'


def test_doc():
    env = {'insights_props': Sat5InsightsProperties(context_wrap(INSIGHTS_PROPERTIES))}
    failed, total = doctest.testmod(sat5_insights_properties, globs=env)
    assert failed == 0


def test_AB():
    with pytest.raises(SkipException):
        Sat5InsightsProperties(context_wrap(''))