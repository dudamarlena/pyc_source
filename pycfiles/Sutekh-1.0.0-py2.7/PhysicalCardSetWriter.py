# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/PhysicalCardSetWriter.py
# Compiled at: 2019-12-11 16:37:58
"""Write physical cards from a PhysicalCardSet

   Save to an XML file which looks like:
   <physicalcardset sutekh_xml_version='1.4' name='SetName' author='Author'>
     <comment>Deck Description</comment>
     <annotations> Various annotations
     More annotations
     </annotations>
     <card name='Some Card' count='5' expansion='Some Expansion' />
     <card name='Some Card' count='2'
        expansion='Some Other Expansion' />
     <card name='Some Other Card' count='2'
        expansion='Some Other Expansion' printing="Some Printing" />
   </physicalcardset>
   """
from sutekh.base.io.BaseCardSetIO import BaseCardXMLWriter

class PhysicalCardSetWriter(BaseCardXMLWriter):
    """Writer for Physical Card Sets.

       We generate an ElementTree representation of the Card Set, which
       can then easily be converted to an appropriate XML representation.
       """
    sMyVersion = '1.4'
    sTypeTag = 'physicalcardset'
    sVersionTag = 'sutekh_xml_version'