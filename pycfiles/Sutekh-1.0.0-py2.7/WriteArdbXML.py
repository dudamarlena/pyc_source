# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteArdbXML.py
# Compiled at: 2019-12-11 16:37:57
"""Given a list of Abstract Cards in a set, write a XML file compatable with
   the Anarch Revolt Deck Builder."""
import time
from xml.etree.ElementTree import Element, SubElement
from sutekh.base.Utility import move_articles_to_back
from sutekh.core.ArdbInfo import ArdbInfo
from sutekh.base.io.IOBase import BaseXMLWriter

class WriteArdbXML(ArdbInfo, BaseXMLWriter):
    """Reformat cardset to elementTree and export it to a ARDB
       compatible XML file."""

    def _add_date_version(self, oRoot):
        """Add the standard data to the root element"""
        sDateWritten = time.strftime('%Y-%m-%d', time.localtime())
        oRoot.attrib['generator'] = 'Sutekh [ %s ]' % self.sVersionString
        oRoot.attrib['formatVersion'] = self.sFormatVersion
        oRoot.attrib['databaseVersion'] = self.sDatabaseVersion
        oDateElem = SubElement(oRoot, 'date')
        oDateElem.text = sDateWritten

    def _ardb_crypt_card(self, oCardElem, oAbsCard, sSet):
        """Fill in name, set and advanced elements for a crypt card"""
        oAdvElem = SubElement(oCardElem, 'adv')
        oNameElem = SubElement(oCardElem, 'name')
        sName = move_articles_to_back(oAbsCard.name)
        if oAbsCard.level is not None:
            oAdvElem.text = 'Advanced'
            oNameElem.text = sName.replace(' (Advanced)', '')
        else:
            oNameElem.text = sName
        oSetElem = SubElement(oCardElem, 'set')
        oSetElem.text = sSet
        return

    def _ardb_lib_card(self, oCardElem, oAbsCard, sSet):
        """Fill in name and set for a library card"""
        oNameElem = SubElement(oCardElem, 'name')
        oNameElem.text = move_articles_to_back(oAbsCard.name)
        oSetElem = SubElement(oCardElem, 'set')
        oSetElem.text = sSet

    def _gen_tree(self, oHolder):
        """Creates the actual XML document into memory."""
        dCards = self._get_cards(oHolder.cards)
        dVamps, dCryptStats = self._extract_crypt(dCards)
        dLib, iLibSize = self._extract_library(dCards)
        oRoot = Element('deck')
        self._add_date_version(oRoot)
        oNameElem = SubElement(oRoot, 'name')
        oNameElem.text = oHolder.name
        oAuthElem = SubElement(oRoot, 'author')
        oAuthElem.text = oHolder.author
        oDescElem = SubElement(oRoot, 'description')
        oDescElem.text = oHolder.comment
        oCryptElem = SubElement(oRoot, 'crypt', size=str(dCryptStats['size']), min=str(dCryptStats['min']), max=str(dCryptStats['max']), avg='%.2f' % dCryptStats['avg'])
        self.format_vamps(oCryptElem, dVamps)
        oLibElem = SubElement(oRoot, 'library', size=str(iLibSize))
        self.format_library(oLibElem, dLib)
        return oRoot

    def format_vamps(self, oCryptElem, dVamps):
        """Convert the Vampire dictionary into ElementTree representation."""
        for (oCard, sSet), iNum in sorted(dVamps.iteritems(), key=lambda x: (
         x[0][0].name,
         x[0][1], x[1])):
            oCardElem = SubElement(oCryptElem, 'vampire', databaseID=str(oCard.id), count=str(iNum))
            self._ardb_crypt_card(oCardElem, oCard, sSet)
            oDiscElem = SubElement(oCardElem, 'disciplines')
            oDiscElem.text = self._gen_disciplines(oCard)
            oClanElem = SubElement(oCardElem, 'clan')
            oCapElem = SubElement(oCardElem, 'capacity')
            if oCard.creed:
                oClanElem.text = 'Imbued'
                oCapElem.text = str(oCard.life)
            else:
                oClanElem.text = [ x.name for x in oCard.clan ][0]
                oCapElem.text = str(oCard.capacity)
            oGrpElem = SubElement(oCardElem, 'group')
            oGrpElem.text = str(oCard.group)
            if oCard.title:
                oTitleElem = SubElement(oCardElem, 'title')
                oTitleElem.text = [ oC.name for oC in oCard.title ][0]
            oTextElem = SubElement(oCardElem, 'text')
            oTextElem.text = oCard.text

    def format_library(self, oLibElem, dLib):
        """Format the dictionary of library cards for the element tree."""
        for (oCard, sTypeString, sSet), iNum in sorted(dLib.iteritems(), key=lambda x: (x[0][0].name, x[0][2], x[1])):
            oCardElem = SubElement(oLibElem, 'card', databaseID=str(oCard.id), count=str(iNum))
            self._ardb_lib_card(oCardElem, oCard, sSet)
            if oCard.costtype is not None:
                oCostElem = SubElement(oCardElem, 'cost')
                oCostElem.text = '%d %s' % (oCard.cost, oCard.costtype)
            if oCard.clan:
                oReqElem = SubElement(oCardElem, 'requirement')
                oReqElem.text = ('.').join([ x.name for x in oCard.clan ])
            oTypeElem = SubElement(oCardElem, 'type')
            oTypeElem.text = sTypeString
            if oCard.discipline:
                oDiscElem = SubElement(oCardElem, 'disciplines')
                oDiscElem.text = self._gen_disciplines(oCard)
            oTextElem = SubElement(oCardElem, 'text')
            oTextElem.text = oCard.text

        return