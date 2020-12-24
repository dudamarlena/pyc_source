# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/base/cllsd_test.py
# Compiled at: 2008-07-21 18:55:15
from indra.base import llsd, lluuid
from datetime import datetime
import cllsd, time, sys

class myint(int):
    __module__ = __name__


values = (
 '&<>', '膬j', llsd.uri('http://foo<'), lluuid.LLUUID(), llsd.LLSD(['thing']), 1, myint(31337), sys.maxint + 10, llsd.binary('foo'), [], {}, {'f&ሒ': 3}, 3.1, True, None, datetime.fromtimestamp(time.time()))

def valuator(values):
    for v in values:
        yield v


longvalues = ()
for v in values + longvalues:
    print '%r => %r' % (v, cllsd.llsd_to_xml(v))

a = [[{'a': 3}]] * 1000000
s = time.time()
print hash(cllsd.llsd_to_xml(a))
e = time.time()
t1 = e - s
print t1
s = time.time()
print hash(llsd.LLSDXMLFormatter()._format(a))
e = time.time()
t2 = e - s
print t2
print 'Speedup:', t2 / t1