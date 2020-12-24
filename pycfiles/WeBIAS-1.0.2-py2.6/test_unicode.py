# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/test/test_unicode.py
# Compiled at: 2015-04-13 16:10:48
"""Test handling of Unicode strings and plain Python strings"""
from gnosis.xml.pickle import loads, dumps
from gnosis.xml.pickle.util import setInBody
from types import StringType, UnicodeType
import funcs
funcs.set_parser()
ustring = 'Alef: %s, Omega: %s' % (unichr(1488), unichr(969))
pstring = 'Only US-ASCII characters'
estring = 'Only US-ASCII with line breaks\n\tthat was a tab'

class C:

    def __init__(self, ustring, pstring, estring):
        self.ustring = ustring
        self.pstring = pstring
        self.estring = estring


o = C(ustring, pstring, estring)
xml = dumps(o)
o2 = loads(xml)
if not isinstance(o2.ustring, UnicodeType):
    raise "AAGH! Didn't get UnicodeType"
if not isinstance(o2.pstring, StringType):
    raise "AAGH! Didn't get StringType for pstring"
if not isinstance(o2.estring, StringType):
    raise "AAGH! Didn't get StringType for estring"
if o.ustring != o2.ustring or o.pstring != o2.pstring or o.estring != o2.estring:
    raise 'ERROR(1)'
setInBody(StringType, 1)
xml = dumps(o)
o2 = loads(xml)
if not isinstance(o2.ustring, UnicodeType):
    raise "AAGH! Didn't get UnicodeType"
if not isinstance(o2.pstring, StringType):
    raise "AAGH! Didn't get StringType for pstring"
if not isinstance(o2.estring, StringType):
    raise "AAGH! Didn't get StringType for estring"
if o.ustring != o2.ustring or o.pstring != o2.pstring or o.estring != o2.estring:
    raise 'ERROR(1)'
setInBody(UnicodeType, 0)
try:
    xml = dumps(o)
    raise 'FAIL: We should not be allowed to put Unicode in attrs'
except TypeError:
    pass

print '** OK **'