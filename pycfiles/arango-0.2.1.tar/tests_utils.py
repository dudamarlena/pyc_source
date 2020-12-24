# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maxk/Projects/OpenSource/arango-python/arango/tests/tests_utils.py
# Compiled at: 2013-03-08 14:06:20
from nose.tools import assert_equal
from arango.utils import json
from .tests_base import TestsBase

class TestsUtils(TestsBase):

    def test_json_loads_dumps(self):
        resource = {'a': 1, 'b': [1, 2]}
        result = json.dumps(json.loads('{"a": 1, "b": [1, 2]}'))
        assert_equal(json.dumps(resource), result)
        assert_equal(json.loads(result), resource)