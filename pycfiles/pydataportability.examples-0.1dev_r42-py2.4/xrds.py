# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pydataportability/examples/scripts/xrds.py
# Compiled at: 2008-04-19 17:15:11
from pydataportability.xrds.parser import XRDSParser
from pkg_resources import resource_stream

def main():
    fp = resource_stream(__name__, 'xrds.xml')
    p = XRDSParser(fp)
    fp.close()
    for s in p.services:
        print 'Type:', s.type
        print 'Prio:', s.priority
        print 'LocalID:', s.localid
        for uri in s.uris:
            print '  ', uri.uri

        print
        print