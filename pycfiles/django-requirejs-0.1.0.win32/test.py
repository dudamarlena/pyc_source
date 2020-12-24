# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \dev\Python26\Lib\site-packages\requirejs\tests\test.py
# Compiled at: 2012-02-26 15:07:15
import os
from unittest import TestCase
from django.conf import settings
from requirejs.templateloader.filesystem import Loader
TEMPLATES_DIR = [os.path.join(os.path.dirname(__file__), 'templates')]
settings.STATICFILES_DIRS = [os.path.join(os.path.dirname(__file__), 'static')]

class TestLoader(TestCase):

    def atestBaseLoader(self):
        loader = Loader()
        self.assertEqual(loader.load_template_source(template_name='testBaseLoader.html', template_dirs=TEMPLATES_DIR)[0], 'testBaseLoader.html source')

    def atest_load_template_source(self):
        loader = Loader()
        loader.load_template_source(template_name='testBaseInclude.html', template_dirs=TEMPLATES_DIR)
        self.assertEqual(len(loader.included_files), 1)
        self.assertEqual(loader.included_files[0], 'jquery.js')

    def atest_process_template(self):
        loader = Loader()
        template = '\n        <!-- INCLUDE_JS_HERE -->\n\n        <script type="text/javascript">\n            //= include jquery.js # test comment\n            //= include jquery.js # test duplicate\n            //= include jquery.ui.js\n        </script>'
        processed_template = loader.process_template(template)
        self.assertEqual(len(loader.included_files), 2)
        self.assertEqual(loader.included_files[0], 'jquery.js')
        self.assertEqual(loader.included_files[1], 'jquery.ui.js')
        expected_processed_template = '\n        <script type="text/javascript" src="{{ STATIC_URL }}jquery.js"></script>\n        <script type="text/javascript" src="{{ STATIC_URL }}jquery.ui.js"></script>\n\n        <script type="text/javascript">\n            //= include jquery.js # test comment\n            //= include jquery.js # test duplicate\n            //= include jquery.ui.js\n        </script>'
        self.assertEqual(str(processed_template), str(expected_processed_template))

    def test_process_template_with_js(self):
        loader = Loader()
        template = '\n        <!-- INCLUDE_JS_HERE -->\n\n        <script type="text/javascript">\n            //= include test.js\n        </script>'
        processed_template = loader.process_template(template)
        self.assertEqual(len(loader.included_files), 3)
        self.assertEqual(loader.included_files[0], 'sub2.js')
        self.assertEqual(loader.included_files[1], 'sub1.js')
        self.assertEqual(loader.included_files[2], 'test.js')
        expected_processed_template = '\n        <script type="text/javascript" src="{{ STATIC_URL }}sub2.js"></script>\n        <script type="text/javascript" src="{{ STATIC_URL }}sub1.js"></script>\n        <script type="text/javascript" src="{{ STATIC_URL }}test.js"></script>\n\n        <script type="text/javascript">\n            //= include test.js\n        </script>'
        self.assertEqual(str(processed_template), str(expected_processed_template))

    def test_get_include_placeholder_indent(self):
        loader = Loader()
        indent = '      '
        template = '\n' + indent + '<!-- INCLUDE_JS_HERE -->'
        self.assertEqual(loader.get_include_placeholder_indent(template), indent)