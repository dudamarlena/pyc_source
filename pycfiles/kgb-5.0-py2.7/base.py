# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/kgb/tests/base.py
# Compiled at: 2020-04-10 23:22:42
from __future__ import unicode_literals
import re, sys, textwrap
if sys.version_info[:2] >= (2, 7):
    import unittest
else:
    import unittest2 as unittest
from kgb.agency import SpyAgency

class MathClass(object):

    def do_math(self, a=1, b=2, *args, **kwargs):
        print self
        assert isinstance(self, MathClass)
        return a + b

    def do_math_pos(self, a, b):
        assert isinstance(self, MathClass)
        return a + b

    def do_math_mixed(self, a, b=2, *args, **kwargs):
        assert isinstance(self, MathClass)
        return a + b

    @classmethod
    def class_do_math(cls, a=2, b=5, *args, **kwargs):
        assert issubclass(cls, MathClass)
        return a * b

    @classmethod
    def class_do_math_pos(cls, a, b):
        assert issubclass(cls, MathClass)
        return a * b


class TestCase(unittest.TestCase):
    """Base class for test cases for kgb."""
    ws_re = re.compile(b'\\s+')

    def setUp(self):
        self.agency = SpyAgency()
        self.orig_class_do_math = MathClass.class_do_math

    def tearDown(self):
        MathClass.class_do_math = self.orig_class_do_math
        self.agency.unspy_all()

    def shortDescription(self):
        """Return the description of the current test.

        This changes the default behavior to replace all newlines with spaces,
        allowing a test description to span lines. It should still be kept
        short, though.

        Returns:
            bytes:
            The description of the test.
        """
        doc = self._testMethodDoc
        if doc is not None:
            doc = doc.split(b'\n\n', 1)[0]
            doc = self.ws_re.sub(b' ', doc).strip()
        return doc

    def make_func(self, code_str, func_name=b'func'):
        """Return a new function, created by the supplied Python code.

        This is used to create functions with signatures that depend on a
        specific version of Python, and would generate syntax errors on
        earlier versions.

        Args:
            code_str (unicode):
                The Python code used to create the function.

            func_name (unicode, optional):
                The expected name of the function.

        Returns:
            callable:
            The resulting function.

        Raises:
            Exception:
                There was an error with the supplied code.
        """
        scope = {}
        exec textwrap.dedent(code_str) in scope
        return scope[func_name]