# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/domstripper/test_domstripper.py
# Compiled at: 2008-11-19 03:58:00
import re
from cStringIO import StringIO
import unittest
from domstripper import DOMStripper

class TestDOMStripper(unittest.TestCase):

    def setUp(self):
        pass

    def _trim_whitespace(self, html):
        return re.sub('>\\s+<', '><', html).strip()

    def test_stripper(self):
        doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n'
        html = doctype + '<html><head><title>Title</title><meta content="incomplete"></head>\n        <body valign="top"><div id="main">Some stuff</div>\n          <div id="junk">We dont want to keep this.</div>\n        <blockquote>Blockquote 1</blockquote>\n        <blockquote>Blockquote 2</blockquote>\n        <a href="junk">More junk</a>\n        </body></html>'
        file = StringIO(html)
        stripper = DOMStripper(file, ['#main', 'blockquote'])
        html = stripper.getvalue()
        html = self._trim_whitespace(html)
        expect = doctype + '<html>\n        <head>\n        <title>Title</title>\n        <meta content="incomplete"/>\n        </head>\n        <body valign="top">\n          <div id="main">Some stuff</div>\n          <blockquote>Blockquote 1</blockquote>\n          <blockquote>Blockquote 2</blockquote>\n          \n        </body>\n        </html>'
        expect = self._trim_whitespace(expect)
        self.assertEqual(html, expect)

    def test_keep_just_links(self):
        doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n'
        html = doctype + '<html><head><title>Title</title></head><body>\n        <p><a href="google">Google</a></p>\n        <div><a href="yahoo">Yahoo</a></div>\n        <a href="strong"><strong>included</strong></a>\n        </body></html>'
        file = StringIO(html)
        stripper = DOMStripper(file, ['a'])
        html = stripper.getvalue()
        html = self._trim_whitespace(html)
        expect = doctype + '<html><head><title>Title</title></head><body>\n        <a href="google">Google</a>\n        <a href="yahoo">Yahoo</a>\n        <a href="strong"><strong>included</strong></a>\n        </body></html>'
        expect = self._trim_whitespace(expect)
        if html != expect:
            print 'GOT'
            print html
            print 'EXPECTED'
            print expect
        self.assertEqual(html, expect)


if __name__ == '__main__':
    unittest.main()