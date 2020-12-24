# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/gman/Documents/code/Flask-Blogging/test/test_core.py
# Compiled at: 2018-02-15 00:06:52
# Size of source mod 2**32: 1062 bytes
try:
    from builtins import str, range
except ImportError:
    pass

from unittest import TestCase
from flask_blogging import BloggingEngine, PostProcessor
from markdown.extensions.codehilite import CodeHiliteExtension
sample_markdown = '\n\n##This is a test\n\n\n    :::python\n    print("Hello, World")\n'
expected_markup = '<h2>This is a test</h2>\n<div class="codehilite"><pre><span class="k">print</span><span class="p">(</span><span class="s">&quot;Hello, World&quot;</span><span class="p">)</span>\n</pre></div>'

class TestCore(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_custom_md_extension(self):
        extn = CodeHiliteExtension({})
        engine = BloggingEngine(extensions=[extn])
        extns = engine.post_processor.all_extensions()
        self.assertEqual(len(extns), 3)
        self.assertTrue(isinstance(extns[(-1)], CodeHiliteExtension))