# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/io/WriteArdbHTML.py
# Compiled at: 2019-12-11 16:37:57
"""Export a card set to HTML."""
import time
from xml.etree.ElementTree import Element, SubElement, tostring
from sutekh.base.core.BaseAdapters import IAbstractCard
from sutekh.base.Utility import pretty_xml, norm_xml_quotes
from sutekh.core.ArdbInfo import ArdbInfo
from sutekh.SutekhInfo import SutekhInfo
from sutekh.SutekhUtility import monger_url, secret_library_url
HTML_STYLE = '\nbody {\n   background: #000000;\n   color: #AAAAAA;\n   margin: 0\n}\n\ndiv#crypt { background: #000000; }\n\ndiv#info {\n   background: #331111;\n   width: 100%;\n}\n\ndiv#library {\n   background: #000000\n   url("http://www.white-wolf.com/VTES/images/CardsImg.jpg")\n   no-repeat scroll top right;\n}\n\nh1 {\n   font-size: x-large;\n   margin-left: 1cm\n}\n\nh2 {\n   font-size: large;\n   margin-left: 1cm\n}\n\nh3 {\n   font-size: large;\n   border-bottom: solid;\n   border-width: 2px;\n}\n\nh4 {\n   font-size: medium;\n   margin-bottom: 0px\n}\n\ndiv#cardtext { background: #000000 }\n\ndiv#cardtext h4 { text-decoration: underline; }\n\ndiv#cardtext h5 {\n   font-weight: normal;\n   text-decoration: underline;\n   margin-left: 1em;\n   margin-bottom: 0.1em;\n}\n\ndiv#cardtext div.text { margin-left: 1em; }\n\ndiv#cardtext ul {\n   list-style-type: none;\n   margin-top: 0.1em;\n   margin-bottom: 0.1em;\n   padding-left: 1em;\n}\n\ndiv#cardtext .label { font-style: italic; }\n\ndiv#cardtext p {\n   margin-left: 0.3em;\n   margin-bottom: 0.1em;\n   margin-top: 0em;\n}\n\ntable { line-height: 70% }\n\n.generator {\n   color: #555555;\n   position: relative;\n   top: 20px;\n}\n\n.librarytype { }\n\n.stats {\n   color: #777777;\n   margin: 5px;\n}\n\n.tablevalue {\n    color: #aaaa88;\n    margin: 5px\n}\n\n.value { color: #aaaa88 }\n\nhr { color: sienna }\n\np { margin-left: 60px }\n\na {\n    color: #aaaa88;\n    margin: 5px;\n    text-decoration: none\n}\n\na:hover {\n    color: #ffffff;\n    margin: 5px;\n    text-decoration: none\n}\n'

def _sort_vampires(dVamps):
    """Sort the vampires by number, then capacity."""
    aSortedVampires = []
    for oCard, (iCount, _sSet) in dVamps.iteritems():
        if oCard.creed:
            iCapacity = oCard.life
            sClan = '%s (Imbued)' % [ x.name for x in oCard.creed ][0]
        else:
            iCapacity = oCard.capacity
            sClan = [ oClan.name for oClan in oCard.clan ][0]
        aSortedVampires.append(((iCount, iCapacity, oCard.name, sClan),
         oCard))

    aSortedVampires.sort(key=lambda x: x[0][2])
    aSortedVampires.sort(key=lambda x: (x[0][0], x[0][1]), reverse=True)
    return aSortedVampires


def _sort_lib(dLib):
    """Extract a list of cards sorted into types from the library"""
    dTypes = {}
    for oCard, (iCount, sType, _sSet) in dLib.iteritems():
        dTypes.setdefault(sType, [0])
        dTypes[sType][0] += iCount
        dTypes[sType].append((iCount, oCard.name))

    return sorted(dTypes.items())


def _add_span(oElement, sText, sClass=None, sId=None):
    """Add a span element to the element oElement"""
    oSpan = SubElement(oElement, 'span')
    oSpan.text = sText
    if sClass:
        oSpan.attrib['class'] = sClass
    if sId:
        oSpan.attrib['id'] = sId


def _add_text(oElement, oCard):
    """Add the card text to the ElementTree line by line"""
    oTextDiv = SubElement(oElement, 'div')
    oTextDiv.attrib['class'] = 'text'
    for sLine in oCard.text.splitlines():
        oPara = SubElement(oTextDiv, 'p')
        oPara.text = sLine


class WriteArdbHTML(ArdbInfo):
    """Export a Card set to a 'nice' HTML file.

       We create a ElementTree that represents the XHTML file,
       and then dump that to file.
       This tries to match the HTML file produced by ARDB.
       """

    def __init__(self, sLinkMode='Monger', bDoText=False):
        super(WriteArdbHTML, self).__init__()
        self._sLinkMode = sLinkMode
        self._bDoText = bDoText

    def write(self, fOut, oHolder):
        """Handle the response to the dialog"""
        oRoot = self._gen_tree(oHolder)
        fOut.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
        sData = tostring(oRoot)
        sData = norm_xml_quotes(sData)
        fOut.write(sData)

    def _gen_tree(self, oHolder):
        """Convert the Cards to a element tree containing 'nice' HTML"""
        oDocRoot = Element('html', xmlns='http://www.w3.org/1999/xhtml', lang='en')
        oDocRoot.attrib['xml:lang'] = 'en'
        oBody = self._add_header(oDocRoot, oHolder)
        dCards = self._get_cards(oHolder.cards)
        aSortedVampires = self._add_crypt(oBody, dCards)
        aSortedLibCards = self._add_library(oBody, dCards)
        if self._bDoText:
            oCardText = SubElement(oBody, 'div', id='cardtext')
            oTextHead = SubElement(oCardText, 'h3')
            oTextHead.attrib['class'] = 'cardtext'
            _add_span(oTextHead, 'Card Texts')
            self._add_crypt_text(oCardText, aSortedVampires)
            self._add_library_text(oCardText, aSortedLibCards)
        oGenerator = SubElement(oBody, 'div')
        _add_span(oGenerator, 'Crafted with : Sutekh [ %s ]. [ %s ]' % (
         SutekhInfo.VERSION_STR,
         time.strftime('%Y-%m-%d', time.localtime())), 'generator')
        pretty_xml(oDocRoot)
        return oDocRoot

    def _add_header(self, oDocRoot, oHolder):
        """Add the header and title of the HTML file."""
        oHead = SubElement(oDocRoot, 'head')
        oEncoding = SubElement(oHead, 'meta')
        oEncoding.attrib['http-equiv'] = 'content-type'
        oEncoding.attrib['content'] = 'text/html; charset="us-ascii"'
        oStyle = SubElement(oHead, 'style', type='text/css')
        oStyle.text = HTML_STYLE
        oTitle = SubElement(oHead, 'title')
        if oHolder.author:
            oTitle.text = 'VTES deck : %s by %s' % (oHolder.name,
             oHolder.author)
        else:
            oTitle.text = 'VTES deck : %s' % oHolder.name
        oBody = SubElement(oDocRoot, 'body')
        oInfo = SubElement(oBody, 'div', id='info')
        oName = SubElement(oInfo, 'h1', id='nametitle')
        _add_span(oName, 'Deck Name :')
        _add_span(oName, oHolder.name, 'value', 'namevalue')
        oAuthor = SubElement(oInfo, 'h2', id='authortitle')
        _add_span(oAuthor, 'Author : ')
        _add_span(oAuthor, oHolder.author, 'value', 'authornamevalue')
        oDesc = SubElement(oInfo, 'h2', id='description')
        _add_span(oDesc, 'Description : ')
        oPara = SubElement(oInfo, 'p')
        _add_span(oPara, oHolder.comment, 'value', 'descriptionvalue')
        return oBody

    def _gen_link(self, oCard, oSpan, sName, bVamp):
        """Add a href for the card"""
        oRowHREF = oSpan
        if self._sLinkMode == 'Monger':
            oRowHREF = SubElement(oSpan, 'a', href=monger_url(oCard, bVamp))
        elif self._sLinkMode == 'Secret Library':
            oRowHREF = SubElement(oSpan, 'a', href=secret_library_url(oCard, bVamp))
        if bVamp:
            oRowHREF.text = sName.replace(' (Advanced)', '')
        else:
            oRowHREF.text = sName

    def _add_crypt(self, oBody, dCards):
        """Add the crypt to the file"""

        def start_section(oBody, dCards):
            """Format the start of the crypt section"""
            dVamps, dCryptStats = self._extract_crypt(dCards)
            oCrypt = SubElement(oBody, 'div', id='crypt')
            oCryptTitle = SubElement(oCrypt, 'h3', id='crypttitle')
            _add_span(oCryptTitle, 'Crypt')
            _add_span(oCryptTitle, '[%(size)d vampires] Capacity min : %(min)d max : %(max)d average : %(avg).2f' % dCryptStats)
            aSortedVampires = _sort_vampires(self._group_sets(dVamps))
            return (oCrypt, aSortedVampires)

        def add_row(oCryptTBody, tVampInfo, oCard):
            """Add a row to the display table"""
            oTR = SubElement(oCryptTBody, 'tr')
            oTD = SubElement(oTR, 'td')
            _add_span(oTD, '%dx' % tVampInfo[0], 'tablevalue')
            oTD = SubElement(oTR, 'td')
            oSpan = SubElement(oTD, 'span')
            oSpan.attrib['class'] = 'tablevalue'
            self._gen_link(oCard, oSpan, tVampInfo[2], True)
            oTD = SubElement(oTR, 'td')
            if oCard.level is not None:
                _add_span(oTD, '(Advanced)', 'tablevalue')
            oTD = SubElement(oTR, 'td')
            _add_span(oTD, str(tVampInfo[1]), 'tablevalue')
            oTD = SubElement(oTR, 'td')
            _add_span(oTD, self._gen_disciplines(oCard), 'tablevalue')
            oTD = SubElement(oTR, 'td')
            if oCard.title:
                _add_span(oTD, [ oTitle.name for oTitle in oCard.title ][0], 'tablevalue')
            oTD = SubElement(oTR, 'td')
            _add_span(oTD, '%s (group %d)' % (tVampInfo[3], oCard.group), 'tablevalue')
            return

        oCrypt, aSortedVampires = start_section(oBody, dCards)
        oCryptTBody = SubElement(SubElement(SubElement(oCrypt, 'div', id='crypttable'), 'table', summary='Crypt card table'), 'tbody')
        for tVampInfo, oCard in aSortedVampires:
            add_row(oCryptTBody, tVampInfo, oCard)

        return aSortedVampires

    def _add_library(self, oBody, dCards):
        """Add the library cards to the tree"""

        def start_section(oBody, dCards):
            """Set up the header for this section"""
            dLib, iLibSize = self._extract_library(dCards)
            aSortedLibCards = _sort_lib(self._group_sets(dLib))
            oLib = SubElement(oBody, 'div', id='library')
            oLibTitle = SubElement(oLib, 'h3', id='librarytitle')
            _add_span(oLibTitle, 'Library')
            _add_span(oLibTitle, '[%d cards]' % iLibSize, 'stats', 'librarystats')
            return (oLib, aSortedLibCards)

        def add_row(oTBody, iCount, sName):
            """Add a row to the display table"""
            oCard = IAbstractCard(sName)
            oTR = SubElement(oTBody, 'tr')
            oTD = SubElement(oTR, 'td')
            _add_span(oTD, '%dx' % iCount, 'tablevalue')
            oTD = SubElement(oTR, 'td')
            oSpan = SubElement(oTD, 'span')
            oSpan.attrib['class'] = 'tablevalue'
            self._gen_link(oCard, oSpan, sName, False)

        oLib, aSortedLibCards = start_section(oBody, dCards)
        oLibTable = SubElement(oLib, 'div')
        oLibTable.attrib['class'] = 'librarytable'
        for sType, aList in aSortedLibCards:
            oTypeHead = SubElement(oLibTable, 'h4')
            oTypeHead.attrib['class'] = 'librarytype'
            _add_span(oTypeHead, sType)
            _add_span(oTypeHead, '[%d]' % aList[0], 'stats')
            oTBody = SubElement(SubElement(oLibTable, 'table', summary='Library card table'), 'tbody')
            for iCount, sName in sorted(aList[1:], key=lambda x: x[1]):
                add_row(oTBody, iCount, sName)

        return aSortedLibCards

    def _add_crypt_text(self, oCardText, aSortedVampires):
        """Add the text of the crypt to the element tree"""
        oCryptTextHead = SubElement(oCardText, 'h4')
        oCryptTextHead.attrib['class'] = 'librarytype'
        oCryptTextHead.text = 'Crypt'
        for tVampInfo, oCard in aSortedVampires:
            oCardName = SubElement(oCardText, 'h5')
            oCardName.text = tVampInfo[2]
            oList = SubElement(oCardText, 'ul')
            oListItem = SubElement(oList, 'li')
            _add_span(oListItem, 'Capacity:', 'label')
            _add_span(oListItem, str(tVampInfo[1]), 'capacity')
            oListItem = SubElement(oList, 'li')
            _add_span(oListItem, 'Group:', 'label')
            _add_span(oListItem, str(oCard.group), 'group')
            oListItem = SubElement(oList, 'li')
            _add_span(oListItem, 'Clan:', 'label')
            _add_span(oListItem, tVampInfo[3], 'clan')
            oListItem = SubElement(oList, 'li')
            _add_span(oListItem, 'Disciplines:', 'label')
            _add_span(oListItem, self._gen_disciplines(oCard), 'disciplines')
            _add_text(oCardText, oCard)

    def _add_library_text(self, oCardText, aSortedLibCards):
        """Add the text of the library cards to the tree."""

        def gen_requirements(oCard):
            """Extract the requirements from the card"""
            oList = Element('ul')
            aClan = [ x.name for x in oCard.clan ]
            if aClan:
                oListItem = SubElement(oList, 'li')
                _add_span(oListItem, 'Requires:', 'label')
                _add_span(oListItem, ('/').join(aClan), 'requirement')
            if oCard.costtype is not None:
                oListItem = SubElement(oList, 'li')
                _add_span(oListItem, 'Cost:', 'label')
                _add_span(oListItem, '%d %s' % (oCard.cost,
                 oCard.costtype), 'cost')
            sDisciplines = self._gen_disciplines(oCard)
            if sDisciplines != '':
                oListItem = SubElement(oList, 'li')
                _add_span(oListItem, 'Disciplines:', 'label')
                _add_span(oListItem, sDisciplines, 'disciplines')
            return oList

        for sType, aList in aSortedLibCards:
            oTypeHead = SubElement(oCardText, 'h4')
            oTypeHead.attrib['class'] = 'libraryttype'
            oTypeHead.text = sType
            for sName in sorted([ x[1] for x in aList[1:] ]):
                oCard = IAbstractCard(sName)
                oCardHead = SubElement(oCardText, 'h5')
                oCardHead.attrib['class'] = 'cardname'
                oCardHead.text = sName
                oReqList = gen_requirements(oCard)
                if len(oReqList):
                    oCardText.append(oReqList)
                _add_text(oCardText, oCard)