# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/wkhtmltopdf/tests.py
# Compiled at: 2011-07-21 06:58:59
import os, time, unittest, urllib
from main import WKhtmlToPdf, wkhtmltopdf
from api import run_server, RequestHandler, HOST, PORT

class MainTestCase(unittest.TestCase):

    def setUp(self):
        self.url = 'http://www.example.com'
        self.output_file = '/tmp/example.pdf'
        self.wkhtmltopdf = WKhtmlToPdf(self.url, self.output_file)

    def test_wkhtmltopdf_options(self):
        self.assertEqual(self.wkhtmltopdf._create_option_list(), ['--enable-plugins', '--orientation Portrait', '--dpi 100'])
        self.wkhtmltopdf.flash_plugin = False
        self.assertEqual(self.wkhtmltopdf._create_option_list(), ['--orientation Portrait', '--dpi 100'])
        self.wkhtmltopdf.orientation = 'Landscape'
        self.assertEqual(self.wkhtmltopdf._create_option_list(), ['--orientation Landscape', '--dpi 100'])
        self.wkhtmltopdf.dpi = 300
        self.assertEqual(self.wkhtmltopdf._create_option_list(), ['--orientation Landscape', '--dpi 300'])
        self.wkhtmltopdf.disable_javascript = True
        self.assertEqual(self.wkhtmltopdf._create_option_list(), ['--disable-javascript', '--orientation Landscape', '--dpi 300'])
        self.wkhtmltopdf.delay = 1
        self.assertEqual(self.wkhtmltopdf._create_option_list(), ['--disable-javascript', '--redirect-delay 1', '--orientation Landscape', '--dpi 300'])
        self.wkhtmltopdf.no_background = True
        self.assertEqual(self.wkhtmltopdf._create_option_list(), ['--disable-javascript', '--no-background', '--redirect-delay 1', '--orientation Landscape', '--dpi 300'])
        self.wkhtmltopdf.grayscale = True
        self.assertEqual(self.wkhtmltopdf._create_option_list(), ['--disable-javascript', '--no-background', '--grayscale', '--redirect-delay 1', '--orientation Landscape', '--dpi 300'])

    def test_wkhtmltopdf_callable(self):
        wkhtmltopdf(self.url, self.output_file)
        self.assertTrue(os.path.exists(self.output_file))

    def tearDown(self):
        try:
            os.remove(self.output_file)
        except OSError:
            pass


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.url = 'http://www.example.com'
        self.output_file = '/tmp/example2.pdf'

    def test_api(self):
        urllib.urlopen('http://%s:%s/?url=%s&output_file=%s' % (HOST, PORT, self.url, self.output_file))
        self.assertTrue(os.path.exists(self.output_file))

    def tearDown(self):
        try:
            os.remove(self.output_file)
        except OSError:
            pass


if __name__ == '__main__':
    unittest.main()