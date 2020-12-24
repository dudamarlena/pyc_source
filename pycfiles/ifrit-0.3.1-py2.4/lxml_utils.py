# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ifrit/lxml_utils.py
# Compiled at: 2007-02-17 13:26:16
""" ifrit utility implementations using lxml

"""
from lxml.etree import XML as _XML
from lxml.etree import parse as _parse
from lxml.etree import XMLParser
from zope.interface import directlyProvides
from ifrit.interfaces import IStringParser
from ifrit.interfaces import IStreamParser
_parser = XMLParser()

def fromstring(xmlstring):
    return _XML(xmlstring, _parser)


directlyProvides(fromstring, IStringParser)

def parse(xmlstream):
    return _parse(xmlstream, _parser)


directlyProvides(parse, IStreamParser)