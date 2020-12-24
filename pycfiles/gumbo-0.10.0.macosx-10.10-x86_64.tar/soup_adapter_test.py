# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/gumbo/soup_adapter_test.py
# Compiled at: 2015-04-30 22:50:43
"""Tests for the Gumbo's BeautifulSoup Python adapter."""
__author__ = 'jdtang@google.com (Jonathan Tang)'
import unittest, soup_adapter

class SoupAdapterTest(unittest.TestCase):

    def testSimpleParse(self):
        soup = soup_adapter.parse('\n        <ul>\n          <li class=odd><a href="one.html">One</a>\n          <li class="even"><a href="two.html">Two</a>\n          <li class=\'odd\'><a href="three.html">Three</a>\n          <li class="even"><a href="four.html">Four</a>\n        </ul>\n        ')
        head = soup.head
        self.assertEquals(soup, head.parent.parent)
        self.assertEquals('head', head.name)
        self.assertEquals(0, len(head))
        body = soup.body
        self.assertEquals(head, body.previousSibling)
        self.assertEquals(2, len(body))
        self.assertEquals('ul', body.contents[0].name)
        self.assertEquals(body, head.next)
        self.assertEquals(head, body.previous)
        list_items = body.findAll('li')
        self.assertEquals(4, len(list_items))
        evens = body('li', 'even')
        self.assertEquals(2, len(evens))
        a2 = body.find('a', href='two.html')
        self.assertEquals('a', a2.name)
        self.assertEquals('Two', a2.contents[0])
        self.assertEquals(a2, evens[0].next)
        self.assertEquals(evens[0], a2.previous)
        li2 = a2.parent
        self.assertEquals('li', li2.name)
        self.assertEquals('even', li2['class'])
        self.assertEquals(list_items[1], li2)
        self.assertEquals(evens[0], li2)


if __name__ == '__main__':
    unittest.main()