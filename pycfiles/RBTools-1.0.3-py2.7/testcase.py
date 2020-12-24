# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/testing/testcase.py
# Compiled at: 2020-04-14 20:27:46
from __future__ import unicode_literals
import os, re, sys, unittest

class TestCase(unittest.TestCase):
    """The base class for RBTools test cases.

    Unlike the standard unittest.TestCase, this allows the test case
    description (generally the first line of the docstring) to wrap multiple
    lines.
    """
    ws_re = re.compile(b'\\s+')
    default_text_editor = b'%s %s' % (
     sys.executable,
     os.path.abspath(os.path.join(os.path.dirname(__file__), b'scripts', b'editor.py')))

    def setUp(self):
        super(TestCase, self).setUp()
        os.environ[str(b'RBTOOLS_EDITOR')] = str(self.default_text_editor)

    def shortDescription(self):
        """Returns the description of the current test.

        This changes the default behavior to replace all newlines with spaces,
        allowing a test description to span lines. It should still be kept
        short, though.
        """
        doc = self._testMethodDoc
        if doc is not None:
            doc = doc.split(b'\n\n', 1)[0]
            doc = self.ws_re.sub(b' ', doc).strip()
        return doc

    def assertRaisesMessage(self, expected_exception, expected_message):
        """Assert that a call raises an exception with the given message.

        Args:
            expected_exception (type):
                The type of exception that's expected to be raised.

            expected_message (unicode):
                The expected exception message.

        Raises:
            AssertionError:
                The assertion failure, if the exception and message isn't
                raised.
        """
        return self.assertRaisesRegexp(expected_exception, re.escape(expected_message))