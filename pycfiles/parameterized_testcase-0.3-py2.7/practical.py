# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parameterized_testcase/test/practical.py
# Compiled at: 2011-08-19 00:39:38
from .. import parameterize

class Test:

    def test_basic(self):
        self.assertEqual(self.foo, 'foo')
        self.assertEqual(self.className, type(self).__name__)


params = {'a': {'foo': 'foo', 'className': 'Test_a'}, 
   'b': {'foo': 'foo', 'className': 'Test_b'}}
cases = list(parameterize([
 Test], params))