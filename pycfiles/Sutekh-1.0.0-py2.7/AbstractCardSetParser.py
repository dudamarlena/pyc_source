# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/AbstractCardSetParser.py
# Compiled at: 2019-12-11 16:37:58
"""Read cards from an XML file which looks like:

   <abstractcardset sutekh_xml_version='1.0' name='AbstractCardSetName'
      author='Author' comment='Comment'>
     <annotations>
     Annotations
     </annotations>
     <card id='3' name='Some Card' count='5' />
     <card id='5' name='Some Other Card' count='2' />
   </abstractcardset>
   into a PhysicalCardSet.
   """
from sutekh.io.BaseSutekhXMLParser import BaseSutekhXMLParser
from sutekh.base.core.BaseTables import MAX_ID_LENGTH

class AbstractCardSetParser(BaseSutekhXMLParser):
    """Impement the parser.

       read the tree into an ElementTree, and walk the tree to find the
       cards.
       """
    aSupportedVersions = [
     '1.1', '1.0']
    sTypeTag = 'abstractcardset'
    sTypeName = 'Abstract Card Set list'

    def _convert_tree(self, oHolder):
        """Convert the ElementTree into a CardSetHolder"""
        self._check_tree()
        oRoot = self._oTree.getroot()
        oHolder.name = ('(ACS) %s' % oRoot.attrib['name'])[:MAX_ID_LENGTH]
        oHolder.author = oRoot.attrib['author']
        oHolder.comment = oRoot.attrib['comment']
        oHolder.inuse = False
        for oElem in oRoot:
            if oElem.tag == 'annotations':
                oHolder.annotations = oElem.text
            elif oElem.tag == 'card':
                self._parse_card(oElem, oHolder)