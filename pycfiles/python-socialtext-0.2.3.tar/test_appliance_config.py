# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/justin/Projects/python-socialtext/tests/test_appliance_config.py
# Compiled at: 2011-12-23 09:02:47
from nose.tools import assert_equal, raises
from fakeserver import FakeServer
from utils import assert_isinstance
from socialtext.resources.appliance_config import ApplianceConfiguration
st = FakeServer()

def test_get_config():
    config = st.appliance_config.get()
    st.assert_called('GET', '/data/config')
    assert_isinstance(config, ApplianceConfiguration)
    config.get()
    st.assert_called('GET', '/data/config')
    assert_isinstance(config, ApplianceConfiguration)