# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/pydataportability/examples/scripts/twitter.py
# Compiled at: 2008-04-19 17:15:11
from zope.component import getUtility
from pkg_resources import resource_string
import pydataportability.microformats.hcard, pydataportability.microformats.xfn
from pydataportability.microformats.base.htmlparsers.etree import ElementTreeHTMLParser
from pydataportability.microformats.base.interfaces import IHTMLParser

def main():
    data = resource_string(__name__, 'mrtopf_tidy.html')
    parser = getUtility(IHTMLParser, name='elementtree')()
    mf = parser.fromString(data)
    mf.parse()
    for (name, result) in mf.microformats.items():
        print '**', name, '**'
        for r in result:
            print r