# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/io/BaseIdXMLFile.py
# Compiled at: 2019-12-11 16:37:52
"""Base class for parsers which identify XML files.

   Defines the public interface available."""
from xml.etree.ElementTree import parse, fromstring, ElementTree
try:
    from xml.etree.ElementTree import ParseError
except ImportError:
    from xml.parsers.expat import ExpatError as ParseError

class BaseIdXMLFile(object):
    """Tries to identify the XML file type.

       Parse the file into an ElementTree, and then tests the Root element
       to see which xml file it matches.
       """

    def __init__(self):
        self._bSetExists = self._bParentExists = False
        self._sType = 'Unknown'
        self._sName = self._sParent = None
        return

    def _clear_id_results(self):
        """Reset identifier state."""
        self._bSetExists = False
        self._bParentExists = False
        self._sType = 'Unknown'
        self._sName = None
        self._sParent = None
        return

    name = property(fget=lambda self: self._sName, doc='The name from the XML file')
    parent_exists = property(fget=lambda self: self._bParentExists, doc='True if the parent card set already exists in the database')
    parent = property(fget=lambda self: self._sParent, doc='Name of the parent card set for this set, None if there is no parent')
    exists = property(fget=lambda self: self._bSetExists, doc='True if the card set already exists in the database')
    type = property(fget=lambda self: self._sType, doc='The type of the XML data')

    def _identify_tree(self, oTree):
        """Process the ElementTree to identify the XML file type."""
        raise NotImplementedError('provide _identify_tree')

    def can_parse(self):
        """Return True if this file can be parsed."""
        raise NotImplementedError('provide can_parse')

    def get_parser(self):
        """Return a copy of the correct file parser for this."""
        raise NotImplementedError('provide get_parser')

    def parse_string(self, sIn):
        """Parse the string sIn into the ElementTree"""
        try:
            oTree = ElementTree(fromstring(sIn))
        except ParseError:
            self._clear_id_results()
            return

        self._identify_tree(oTree)

    def parse(self, fIn, _oDummyHolder=None):
        """Parse the file fIn into the ElementTree."""
        try:
            oTree = parse(fIn)
        except ParseError:
            self._clear_id_results()
            return

        self._identify_tree(oTree)

    def id_file(self, sFileName):
        """Load the file sFileName, and try to identify it."""
        fIn = open(sFileName, 'rU')
        try:
            self.parse(fIn, None)
        finally:
            fIn.close()

        return