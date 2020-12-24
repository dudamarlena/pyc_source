# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pydataportability/examples/scripts/twitter2.py
# Compiled at: 2008-04-19 17:34:36
from zope.component import getUtility
from pkg_resources import resource_string
import pydataportability.microformats.hcard, pydataportability.microformats.xfn
from pydataportability.microformats.base.htmlparsers.etree import ElementTreeHTMLParser
from pydataportability.microformats.base.interfaces import IHTMLParser

def main():
    data = resource_string(__name__, 'mrtopf.html')
    parser = getUtility(IHTMLParser, name='beautifulsoup')()
    mf = parser.fromString(data)
    mf.parse()
    for (name, result) in mf.microformats.items():
        print '**', name, '**'
        for r in result:
            print r