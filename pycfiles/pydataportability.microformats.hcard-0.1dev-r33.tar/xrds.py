# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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