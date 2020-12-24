# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_jit_tests.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 963 bytes
import unittest, jittor as jt
from jittor import LOG

def test(name):
    doc = eval(f"jt.tests.{name}.__doc__")
    doc = doc[doc.find('From'):].strip()
    LOG.i(f"Run test {name} {doc}")
    exec(f"jt.tests.{name}()")


tests = [name for name in dir(jt.tests) if not name.startswith('__')]
src = 'class TestJitTests(unittest.TestCase):\n'
for name in tests:
    doc = eval(f"jt.tests.{name}.__doc__")
    doc = doc[doc.find('From'):].strip()
    src += f'\n    def test_{name}(self):\n        test("{name}")\n    '

LOG.vvv('eval src\n' + src)
exec(src)
if __name__ == '__main__':
    unittest.main()