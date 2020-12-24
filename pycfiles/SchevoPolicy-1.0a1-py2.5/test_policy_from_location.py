# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/test/test_policy_from_location.py
# Compiled at: 2008-01-19 12:32:25
"""schevopolicy.schema.policy_from_location unit tests.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevo.test import EvolvesSchemata
from schevopolicy.schema import policy_from_location
LOCATION = 'schevopolicy.test.test_policy'
SOURCE = '\nfrom schevo.schema import *\nschevo.schema.prep(locals())\n\nclass Foo(E.Entity):\n\n    name = f.unicode()\n\n    _key(name)\n'

class BasePolicyFromLocation(EvolvesSchemata):
    """Using the same schema source but with two different schema
    versions, tests the loading of associated policy from a location
    on disk.
    """
    schemata = [
     SOURCE,
     SOURCE]
    skip_evolution = True


class TestPolicyFromLocation1(BasePolicyFromLocation):
    """The policy associated with version 1 allows creation of new Foo
    entities for all contexts."""
    schema_version = 1

    def test(self):
        policy = policy_from_location(db, LOCATION)
        context = None
        rdb = policy(context)
        assert list(rdb.Foo.t) == ['create']
        return


class TestPolicyFromLocation2(BasePolicyFromLocation):
    """The policy associated with version 2 disallows creation of new
    Foo entities for all contexts."""
    schema_version = 2

    def test(self):
        policy = policy_from_location(db, LOCATION)
        context = None
        rdb = policy(context)
        assert list(rdb.Foo.t) == []
        return


optimize.bind_all(sys.modules[__name__])