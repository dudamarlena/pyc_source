# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/objectify/test/test_xpath.py
# Compiled at: 2015-04-13 16:10:45
from gnosis.xml.objectify import make_instance
from gnosis.xml.objectify.utils import XPath
import sys
xml = '<foo>\n  <bar>this</bar>\n  <bar>that</bar>\n  <baz a1="fie" a2="fee">\n    stuff <bar>fo</bar>\n    <bar a1="fiddle">fum</bar>\n    and <bam><bar>fizzle</bar></bam>\n    more stuff\n  </baz>\n</foo>\n'
print xml
print
open('xpath.xml', 'w').write(xml)
o = make_instance(xml)
patterns = '/bar //bar //* /baz/*/bar\n              /bar[2] //bar[2..4]\n              //@a1 //bar/@a1 /baz/@* //@*\n              baz//bar/text() /baz/text()[3]'
for pattern in patterns.split():
    print 'XPath:', pattern
    for match in XPath(o, pattern):
        print ' ', match