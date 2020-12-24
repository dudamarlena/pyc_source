# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/PhysicalCardParser.py
# Compiled at: 2019-12-11 16:37:58
"""Read physical cards from an XML file which looks like:

   <cards sutekh_xml_version="1.0">
     <card id='3' name='Some Card' count='5' expansion="Some Expansion" />
     <card id='3' name='Some Card' count='2'
        Expansion="Some Other Expansion" />
     <card id='5' name='Some Other Card' count='2'
       expansion="Some Expansion" />
   </cards>
   into the default PhysicalCardSet 'My Collection'.
   """
from sutekh.io.BaseSutekhXMLParser import BaseSutekhXMLParser

class PhysicalCardParser(BaseSutekhXMLParser):
    """Implement the PhysicalCard Parser.

       We read the xml file into a ElementTree, then walk the tree to
       extract the cards.
       """
    aSupportedVersions = [
     '1.0', '0.0']
    sTypeTag = 'cards'
    sTypeName = 'Physical card list'

    def _convert_tree(self, oHolder):
        """parse the Element Tree into a card set holder"""
        self._check_tree()
        oHolder.name = 'My Collection'
        oRoot = self._oTree.getroot()
        for oElem in oRoot:
            if oElem.tag == 'card':
                self._parse_card(oElem, oHolder)