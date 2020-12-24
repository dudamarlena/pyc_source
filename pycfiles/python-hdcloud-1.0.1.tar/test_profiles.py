# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jacob/Projects/python-hdcloud/tests/test_profiles.py
# Compiled at: 2010-04-14 14:13:57
from __future__ import absolute_import
from hdcloud import Profile
from .fakeserver import FakeHDCloud
from .utils import assert_isinstance
hdcloud = FakeHDCloud()

def test_all_profiles():
    ps = hdcloud.profiles.all()
    hdcloud.assert_called('GET', '/encoding_profiles.json')
    [ assert_isinstance(p, Profile) for p in ps ]


def test_get_store():
    p = hdcloud.profiles.get(id=1)
    hdcloud.assert_called('GET', '/encoding_profiles/1.json')
    assert p.name == 'Example Profile'