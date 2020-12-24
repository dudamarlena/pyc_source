# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_getenforce.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import getenforce
from insights.tests import context_wrap
GETENFORCE1 = 'Enforcing'
GETENFORCE2 = 'Permissive'
GETENFORCE3 = 'Disabled'

class Testgetenforce:

    def test_getenforce(self):
        result = getenforce.getenforcevalue(context_wrap(GETENFORCE1))
        assert result.get('status') == 'Enforcing'
        result = getenforce.getenforcevalue(context_wrap(GETENFORCE2))
        assert result.get('status') == 'Permissive'
        result = getenforce.getenforcevalue(context_wrap(GETENFORCE3))
        assert result.get('status') == 'Disabled'