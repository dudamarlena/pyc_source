# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/IdentifyXMLFile.py
# Compiled at: 2019-12-11 16:37:58
"""Attempts to identify a XML file as either PhysicalCardSet, PhysicalCard
   or AbstractCardSet (the last two to support legacy backups)."""
from sutekh.base.core.CardSetUtilities import check_cs_exists
from sutekh.base.io.BaseIdXMLFile import BaseIdXMLFile
from sutekh.io.AbstractCardSetParser import AbstractCardSetParser
from sutekh.io.PhysicalCardParser import PhysicalCardParser
from sutekh.io.PhysicalCardSetParser import PhysicalCardSetParser

class IdentifyXMLFile(BaseIdXMLFile):
    """Tries to identify the XML file type.

       Parse the file into an ElementTree, and then tests the Root element
       to see which xml file it matches.
       """

    def _identify_tree(self, oTree):
        """Process the ElementTree to identify the XML file type."""
        self._clear_id_results()
        oRoot = oTree.getroot()
        if oRoot.tag == 'abstractcardset':
            self._sType = 'AbstractCardSet'
            self._sName = '(ACS) ' + oRoot.attrib['name']
            self._bSetExists = check_cs_exists(self._sName.encode('utf8'))
            self._bParentExists = True
        elif oRoot.tag == 'physicalcardset':
            self._sType = 'PhysicalCardSet'
            self._sName = oRoot.attrib['name']
            self._bSetExists = check_cs_exists(self._sName.encode('utf8'))
            if 'parent' in oRoot.attrib:
                self._sParent = oRoot.attrib['parent']
                self._bParentExists = check_cs_exists(self._sParent.encode('utf8'))
            else:
                self._bParentExists = True
        elif oRoot.tag == 'cards':
            self._sType = 'PhysicalCard'
            self._sName = 'My Collection'
            self._bSetExists = check_cs_exists(self._sName.encode('utf8'))
            self._bParentExists = True
        elif oRoot.tag == 'cardmapping':
            self._sType = 'PhysicalCardSetMappingTable'
            self._sName = self._sType
            self._bSetExists = False
            self._bParentExists = False

    def can_parse(self):
        """True if we can parse the card set."""
        if self._sType == 'PhysicalCard' or self._sType == 'PhysicalCardSet' or self._sType == 'AbstractCardSet':
            return True
        return False

    def get_parser(self):
        """Return the correct parser."""
        if self._sType == 'PhysicalCard':
            return PhysicalCardParser()
        else:
            if self._sType == 'PhysicalCardSet':
                return PhysicalCardSetParser()
            if self._sType == 'AbstractCardSet':
                return AbstractCardSetParser()
            return