# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/pyflakes/pyflakes/test/harness.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 2404 bytes
import ast, textwrap, unittest
from pyflakes import checker
__all__ = [
 'TestCase', 'skip', 'skipIf']
skip = unittest.skip
skipIf = unittest.skipIf

class TestCase(unittest.TestCase):
    withDoctest = False

    def flakes(self, input, *expectedOutputs, **kw):
        tree = ast.parse(textwrap.dedent(input))
        file_tokens = checker.make_tokens(textwrap.dedent(input))
        if kw.get('is_segment'):
            tree = tree.body[0]
            kw.pop('is_segment')
        w = (checker.Checker)(tree, file_tokens=file_tokens, withDoctest=self.withDoctest, **kw)
        outputs = [type(o) for o in w.messages]
        expectedOutputs = list(expectedOutputs)
        outputs.sort(key=(lambda t: t.__name__))
        expectedOutputs.sort(key=(lambda t: t.__name__))
        self.assertEqual(outputs, expectedOutputs, 'for input:\n%s\nexpected outputs:\n%r\nbut got:\n%s' % (input, expectedOutputs, '\n'.join([str(o) for o in w.messages])))
        return w

    if not hasattr(unittest.TestCase, 'assertIs'):

        def assertIs(self, expr1, expr2, msg=None):
            if expr1 is not expr2:
                self.fail(msg or '%r is not %r' % (expr1, expr2))

    if not hasattr(unittest.TestCase, 'assertIsInstance'):

        def assertIsInstance(self, obj, cls, msg=None):
            """Same as self.assertTrue(isinstance(obj, cls))."""
            if not isinstance(obj, cls):
                self.fail(msg or '%r is not an instance of %r' % (obj, cls))

    if not hasattr(unittest.TestCase, 'assertNotIsInstance'):

        def assertNotIsInstance(self, obj, cls, msg=None):
            """Same as self.assertFalse(isinstance(obj, cls))."""
            if isinstance(obj, cls):
                self.fail(msg or '%r is an instance of %r' % (obj, cls))

    if not hasattr(unittest.TestCase, 'assertIn'):

        def assertIn(self, member, container, msg=None):
            """Just like self.assertTrue(a in b)."""
            if member not in container:
                self.fail(msg or '%r not found in %r' % (member, container))

    if not hasattr(unittest.TestCase, 'assertNotIn'):

        def assertNotIn(self, member, container, msg=None):
            """Just like self.assertTrue(a not in b)."""
            if member in container:
                self.fail(msg or '%r unexpectedly found in %r' % (member, container))