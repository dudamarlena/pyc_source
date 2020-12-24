# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/test/contexts/XhtmlComplex.py
# Compiled at: 2009-09-30 05:37:25
xhtmlInput = '\n<p>Te<b>s</b>t1 : <b>bold</b>, i<i>tal</i>ics, exponent<sup>34</sup>, sub<sub>45</sub>.</p>\n<p>An <a href="http://www.google.com">hyperlink</a> to Google.</p>\n<ol><li>Number list, item 1</li>\n<ol><li>Sub-item 1</li><li>Sub-Item 2</li>\n<ol><li>Sub-sub-item A</li><li>Sub-sub-item B <i>italic</i>.</li></ol>\n</ol>\n</ol>\n<ul><li>A bullet</li>\n<ul><li>A sub-bullet</li>\n<ul><li>A sub-sub-bullet</li></ul>\n<ol><li>A sub-sub number</li><li>Another.<br /></li></ol>\n</ul>\n</ul>\n<h2>Heading<br /></h2>\nHeading Blabla.<br />\n<h3>SubHeading</h3>\nSubheading blabla.<br />\n'

class D:
    __module__ = __name__

    def getAt1(self):
        return xhtmlInput


dummy = D()