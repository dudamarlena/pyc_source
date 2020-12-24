# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ifrit/objectify_utils.py
# Compiled at: 2007-02-19 21:24:50
""" ifrit utility implementations using lxml.objectify

Note:  nodes returned from this module can *not* have marker interfaces
       added to them at the instance level, due to restricttions in the
       base class (extension type) required by objectify.

$Id: objectify_utils.py,v 1.5 2007/02/20 02:24:50 tseaver Exp $
"""
from lxml.etree import XMLParser
from lxml.etree import parse as _parse
from lxml.etree import XML as _XML
from lxml.objectify import ObjectifyElementClassLookup
from zope.interface import directlyProvides
from zope.interface import implements
from ifrit.interfaces import IStringParser
from ifrit.interfaces import IStreamParser
_lookup = ObjectifyElementClassLookup()
_parser = XMLParser(remove_blank_text=True)
_parser.setElementClassLookup(_lookup)

def fromstring(xmlstring):
    return _XML(xmlstring, _parser)


directlyProvides(fromstring, IStringParser)

def parse(xmlstream):
    return _parse(xmlstream, _parser)


directlyProvides(parse, IStreamParser)