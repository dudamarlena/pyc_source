# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-storymarket/tests/test_schemes.py
# Compiled at: 2010-07-12 12:21:49
from __future__ import absolute_import
from storymarket import PricingScheme, RightsScheme
from .fakeserver import FakeStorymarket
from .utils import assert_list_api, assert_get_api
sm = FakeStorymarket()

def test_list_pricing_schemes():
    assert_list_api(sm, sm.pricing.all, PricingScheme, 'pricing/')


def test_list_rights_schemes():
    assert_list_api(sm, sm.rights.all, RightsScheme, 'rights/')


def test_get_pricing_scheme():
    assert_get_api(sm, sm.pricing.get, PricingScheme, 'pricing/1/')


def test_get_rights_scheme():
    assert_get_api(sm, sm.rights.get, RightsScheme, 'rights/1/')