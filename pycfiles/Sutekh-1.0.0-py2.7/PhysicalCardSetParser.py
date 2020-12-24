# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/PhysicalCardSetParser.py
# Compiled at: 2019-12-11 16:37:58
"""Read physical cards from an XML file which looks like:

   <physicalcardset sutekh_xml_version='1.4' name='SetName' author='Author'
      parent='Parent PCS name'>
     <comment>
     Deck Description
     </comment>
     <annotations>
     Annotations
     </annotations>
     <card name='Some Card' count='5' expansion='Some Expansion' />
     <card name='Some Card' count='2'
         expansion='Some Other Expansion' />
     <card name='Some Other Card' count='2'
         expansion='Some Other Expansion' />
   </physicalcardset>

   into a PhysicalCardSet.
   """
from sutekh.base.io.BaseCardSetIO import BaseCardSetParser
from sutekh.io.BaseSutekhXMLParser import BaseSutekhXMLParser

class PhysicalCardSetParser(BaseCardSetParser, BaseSutekhXMLParser):
    """Impement the parser.

       read the tree into an ElementTree, and walk the tree to find the
       cards.
       """
    aSupportedVersions = [
     '1.4', '1.3', '1.2', '1.1', '1.0']
    sTypeTag = 'physicalcardset'
    sTypeName = 'Physical Card Set list'