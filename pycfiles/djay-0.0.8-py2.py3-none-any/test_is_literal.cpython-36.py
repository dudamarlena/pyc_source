# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/test_is_literal.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 4004 bytes
from pyflakes.messages import IsLiteral
from pyflakes.test.harness import TestCase

class Test(TestCase):

    def test_is_str(self):
        self.flakes("\n        x = 'foo'\n        if x is 'foo':\n            pass\n        ", IsLiteral)

    def test_is_bytes(self):
        self.flakes("\n        x = b'foo'\n        if x is b'foo':\n            pass\n        ", IsLiteral)

    def test_is_unicode(self):
        self.flakes("\n        x = u'foo'\n        if x is u'foo':\n            pass\n        ", IsLiteral)

    def test_is_int(self):
        self.flakes('\n        x = 10\n        if x is 10:\n            pass\n        ', IsLiteral)

    def test_is_true(self):
        self.flakes('\n        x = True\n        if x is True:\n            pass\n        ')

    def test_is_false(self):
        self.flakes('\n        x = False\n        if x is False:\n            pass\n        ')

    def test_is_not_str(self):
        self.flakes("\n        x = 'foo'\n        if x is not 'foo':\n            pass\n        ", IsLiteral)

    def test_is_not_bytes(self):
        self.flakes("\n        x = b'foo'\n        if x is not b'foo':\n            pass\n        ", IsLiteral)

    def test_is_not_unicode(self):
        self.flakes("\n        x = u'foo'\n        if x is not u'foo':\n            pass\n        ", IsLiteral)

    def test_is_not_int(self):
        self.flakes('\n        x = 10\n        if x is not 10:\n            pass\n        ', IsLiteral)

    def test_is_not_true(self):
        self.flakes('\n        x = True\n        if x is not True:\n            pass\n        ')

    def test_is_not_false(self):
        self.flakes('\n        x = False\n        if x is not False:\n            pass\n        ')

    def test_left_is_str(self):
        self.flakes("\n        x = 'foo'\n        if 'foo' is x:\n            pass\n        ", IsLiteral)

    def test_left_is_bytes(self):
        self.flakes("\n        x = b'foo'\n        if b'foo' is x:\n            pass\n        ", IsLiteral)

    def test_left_is_unicode(self):
        self.flakes("\n        x = u'foo'\n        if u'foo' is x:\n            pass\n        ", IsLiteral)

    def test_left_is_int(self):
        self.flakes('\n        x = 10\n        if 10 is x:\n            pass\n        ', IsLiteral)

    def test_left_is_true(self):
        self.flakes('\n        x = True\n        if True is x:\n            pass\n        ')

    def test_left_is_false(self):
        self.flakes('\n        x = False\n        if False is x:\n            pass\n        ')

    def test_left_is_not_str(self):
        self.flakes("\n        x = 'foo'\n        if 'foo' is not x:\n            pass\n        ", IsLiteral)

    def test_left_is_not_bytes(self):
        self.flakes("\n        x = b'foo'\n        if b'foo' is not x:\n            pass\n        ", IsLiteral)

    def test_left_is_not_unicode(self):
        self.flakes("\n        x = u'foo'\n        if u'foo' is not x:\n            pass\n        ", IsLiteral)

    def test_left_is_not_int(self):
        self.flakes('\n        x = 10\n        if 10 is not x:\n            pass\n        ', IsLiteral)

    def test_left_is_not_true(self):
        self.flakes('\n        x = True\n        if True is not x:\n            pass\n        ')

    def test_left_is_not_false(self):
        self.flakes('\n        x = False\n        if False is not x:\n            pass\n        ')

    def test_chained_operators_is_true(self):
        self.flakes('\n        x = 5\n        if x is True < 4:\n            pass\n        ')

    def test_chained_operators_is_str(self):
        self.flakes("\n        x = 5\n        if x is 'foo' < 4:\n            pass\n        ", IsLiteral)

    def test_chained_operators_is_true_end(self):
        self.flakes('\n        x = 5\n        if 4 < x is True:\n            pass\n        ')

    def test_chained_operators_is_str_end(self):
        self.flakes("\n        x = 5\n        if 4 < x is 'foo':\n            pass\n        ", IsLiteral)