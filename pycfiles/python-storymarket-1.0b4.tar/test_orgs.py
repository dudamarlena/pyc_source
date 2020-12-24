# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-storymarket/tests/test_orgs.py
# Compiled at: 2010-07-12 12:22:30
from __future__ import absolute_import
from storymarket import Org
from .fakeserver import FakeStorymarket
from .utils import assert_list_api, assert_get_api
sm = FakeStorymarket()

def test_list_orgs():
    assert_list_api(sm, sm.orgs.all, Org, 'orgs/')


def test_get_org():
    assert_get_api(sm, sm.orgs.get, Org, 'orgs/1/')