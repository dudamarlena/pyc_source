# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/util/tests/test_djblets_js_tags.py
# Compiled at: 2019-06-12 01:17:17
"""Unit tests for djblets.util.templatetags.djblets_js."""
from __future__ import unicode_literals
from djblets.testing.testcases import TestCase
from djblets.util.templatetags.djblets_js import json_dumps

class JSONDumpsFilterTests(TestCase):
    """Unit tests for the {{...|json_dumps}} template filter."""

    def test_prevents_xss(self):
        """Testing {{...|json_dumps}} doesn't allow XSS injection"""
        obj = {b'xss': b'</script><script>alert(1);</script>'}
        self.assertEqual(json_dumps(obj), b'{"xss": "\\u003C/script\\u003E\\u003Cscript\\u003Ealert(1);\\u003C/script\\u003E"}')