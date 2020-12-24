# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\testing\testcase.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import unicode_literals
import re, unittest

class TestCase(unittest.TestCase):
    """The base class for RBTools test cases.

    Unlike the standard unittest.TestCase, this allows the test case
    description (generally the first line of the docstring) to wrap multiple
    lines.
    """
    ws_re = re.compile(b'\\s+')

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