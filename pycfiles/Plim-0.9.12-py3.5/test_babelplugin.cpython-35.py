# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/adapters/test_babelplugin.py
# Compiled at: 2015-10-10 10:15:03
# Size of source mod 2**32: 1051 bytes
from __future__ import unicode_literals
from plim.adapters.babelplugin import extract
from plim.util import StringIO
from .. import TestCaseBase

class TestBabelPlugin(TestCaseBase):

    def test_babel_extractor(self):
        fileobj = StringIO(self.get_file_contents('babelplugin_test.plim'))
        keywords = ['_', 'gettext', 'ungettext', 'pluralize']
        extracted = [(data[1], data[2]) for data in extract(fileobj, keywords, [], {})]
        assert ('_', 'Test') in extracted
        assert ('_', 'View more') in extracted
        assert ('pluralize', ('${num} conversation has been marked as read.', '${num} conversations have been marked as read.', None, None)) in extracted
        assert ('ungettext', ('{num} conversation has been marked as read.', '{num} conversations have been marked as read.', None)) in extracted
        assert ('gettext', 'N') not in extracted