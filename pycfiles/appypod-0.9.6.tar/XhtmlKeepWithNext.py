# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/pod/test/contexts/XhtmlKeepWithNext.py
# Compiled at: 2009-09-30 05:37:25


class D:
    __module__ = __name__

    def getAt1(self):
        return '\n<p>Notifia</p>\n<ol>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li class="podItemKeepWithNext">Keep with next, without style mapping.</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <ul><li class="pmItemKeepWithNext">This one has \'keep with next\'</li>\n        <li>Hello</li>\n          <ol><li>aaaaaaaaaa aaaaaaaaaaaaaa</li>\n              <li>aaaaaaaaaa aaaaaaaaaaaaaa</li>\n              <li>aaaaaaaaaa aaaaaaaaaaaaaa</li>\n              <li class="pmItemKeepWithNext">This one has \'keep with next\'</li>\n          </ol>\n  </ul>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li>Een</li>\n  <li class="pmItemKeepWithNext">This one has \'keep with next\'</li>\n</ol>\n<ul>\n  <li>Un</li>\n  <li>Deux</li>\n  <li>Trois</li>\n  <li>Quatre</li>\n  <li class="pmItemKeepWithNext">VCinq (this one has \'keep with next\')</li>\n  <li class="pmItemKeepWithNext">Six (this one has \'keep with next\')</li>\n  <li class="pmItemKeepWithNext">Sept (this one has \'keep with next\')</li>\n</ul>'


dummy = D()