# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/terms.py
# Compiled at: 2011-08-30 06:36:54
import re
from lxml import etree
from copy import deepcopy
from anolislib import utils

class terms(object):
    """Build and add an index of terms."""
    terms = None

    def __init__(self, ElementTree, **kwargs):
        self.terms = etree.Element('div', {'class': 'index-of-terms'})
        self.buildTerms(ElementTree, **kwargs)
        self.addTerms(ElementTree, **kwargs)

    def buildTerms(self, ElementTree, w3c_compat=False, **kwargs):
        self.terms.text = '\n'
        dfnList = ElementTree.findall('//dfn')
        if dfnList:
            indexNavTop = etree.Element('div', {'class': 'index-nav', 'id': 'index-terms_top'})
            indexNavTop.text = '\n'
            indexNavTop.tail = '\n'
            indexNavHelpers = {'top': indexNavTop}
            self.terms.append(indexNavHelpers['top'])
            termFirstLetter = None
            prevTermFirstLetter = None
            firstLetters = ['top']
            dfnList.sort(key=lambda dfn: utils.textContent(dfn).lower())
            for dfn in dfnList:
                term = deepcopy(dfn)
                term.tail = None
                termID = None
                dfnHasID = False
                if dfn.get('id'):
                    termID = dfn.get('id')
                    dfnHasID = True
                elif dfn.getparent().get('id'):
                    termID = dfn.getparent().get('id')
                if termID:
                    indexEntry = etree.Element('dl')
                    dfnSiblings = int(dfn.xpath('count(preceding-sibling::dfn[not(@id)])'))
                    if not dfnHasID and dfnSiblings > 0:
                        indexEntry = etree.Element('dl', {'id': termID + '_' + str(dfnSiblings) + '_index'})
                    else:
                        indexEntry = etree.Element('dl', {'id': termID + '_index'})
                    indexEntry.text = '\n'
                    termName = etree.Element('dt')
                    if 'id' in term.attrib:
                        del term.attrib['id']
                    term.tag = 'span'
                    term.tail = '\n'
                    termName.append(term)
                    termName.tail = '\n'
                    indexEntry.append(termName)
                    expr = "count(//dfn                            [normalize-space(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'))                            =normalize-space(translate($content,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'))])"
                    if ElementTree.xpath(expr, content=utils.textContent(term)) > 1:
                        dfnContext = etree.Element('dd', {'class': 'dfn-excerpt'})
                        dfnContext.text = '\n'
                        dfnContext.tail = '\n'
                        dfnParentNode = deepcopy(dfn.getparent())
                        if len(dfnParentNode) > 1 and not re.match('^[hH][1-6]$', dfnParentNode.tag):
                            if not dfnParentNode[0].tag == 'dfn':
                                dfnParentNode.text = '*** '
                            else:
                                dfnParentNode.text = ''
                            dfnParentNode.tag = 'span'
                            if 'id' in dfnParentNode.attrib:
                                del dfnParentNode.attrib['id']
                            descendants = dfnParentNode.xpath('.//*[self::dfn or @id]')
                            for descendant in descendants:
                                if descendant.tag == 'dfn':
                                    descendant.tag = 'span'
                                if 'id' in descendant.attrib:
                                    del descendant.attrib['id']
                                if utils.textContent(descendant).lower() == utils.textContent(term).lower():
                                    tail = ''
                                    if descendant.tail is not None:
                                        tail = descendant.tail
                                    descendant.clear()
                                    descendant.text = '...' + tail
                                elif descendant == descendants[0]:
                                    dfnParentNode.text = '*** '

                            dfnContext.append(dfnParentNode)
                            indexEntry.append(dfnContext)
                    termFirstLetter = utils.textContent(term)[0].upper()
                    if termFirstLetter != prevTermFirstLetter and termFirstLetter.isalpha():
                        firstLetters.append(termFirstLetter)
                        indexNavHelpers[termFirstLetter] = etree.Element('div', {'class': 'index-nav', 'id': 'index-terms_' + termFirstLetter})
                        prevTermFirstLetter = termFirstLetter
                        self.terms.append(indexNavHelpers[termFirstLetter])
                    instanceList = ElementTree.xpath("//a[substring-after(@href,'#')=$targetID]|//*[@id=$targetID]", targetID=termID)
                    if instanceList:
                        instanceItem = None
                        lastLinkToHeading = None
                        lastInstanceItem = None
                        for instance in instanceList:
                            instanceID = utils.generateID(instance, **kwargs)
                            instance.set('id', instanceID)
                            linkToHeading = self.getAncestorHeadingLink(instance, instanceID)
                            if not instance.tag == 'a':
                                linkToHeading.set('class', 'dfn-ref')
                            if lastLinkToHeading is None or utils.textContent(linkToHeading) != utils.textContent(lastLinkToHeading):
                                instanceItem = etree.Element('dd')
                                instanceItem.text = '\n'
                                lastLinkToHeading = linkToHeading
                                n = 1
                                if lastInstanceItem is not None:
                                    indexEntry.append(lastInstanceItem)
                                lastInstanceItem = instanceItem
                                linkToHeading.tail = '\n'
                                instanceItem.append(linkToHeading)
                                instanceItem.tail = '\n'
                            else:
                                n += 1
                                counterLink = etree.Element('a', {'href': '#' + instanceID, 'class': 'index-counter'})
                                if not instance.tag == 'a':
                                    counterLink.set('class', 'dfn-ref')
                                else:
                                    counterLink.set('class', 'index-counter')
                                counterLink.text = '(' + str(n) + ')'
                                counterLink.tail = '\n'
                                instanceItem.append(counterLink)
                            if n == 1:
                                indexEntry.append(instanceItem)

                    if not len(instanceList) > 1:
                        indexEntry.set('class', 'has-norefs')
                    self.terms.append(indexEntry)
                    indexEntry.tail = '\n'

            navLetters = etree.Element('p')
            navLetters.text = '\n'
            navLetters.tail = '\n'
            navLettersClones = {}
            firstLetters.append('end')
            firstLetters.reverse()
            while firstLetters:
                letter = firstLetters.pop()
                navLetter = etree.Element('a', {'href': '#index-terms_' + letter})
                navLetter.text = letter
                navLetter.tail = '\n'
                navLetters.append(navLetter)

            for key, navNode in indexNavHelpers.items():
                navLettersClones[key] = deepcopy(navLetters)
                navNode.text = '\n'
                navNode.append(navLettersClones[key])
                navNode.tail = '\n'

            navLettersEnd = deepcopy(navLetters)
            indexNavEnd = etree.Element('div', {'class': 'index-nav', 'id': 'index-terms_end'})
            indexNavEnd.text = '\n'
            indexNavEnd.tail = '\n'
            indexNavEnd.append(navLettersEnd)
            indexNavHelpers = {'end': indexNavEnd}
            self.terms.append(indexNavHelpers['end'])
        self.terms.tail = '\n'
        return

    def getAncestorHeadingLink(self, descendantNode, id):
        """ Given a node, return a link to the heading for the section that contains it."""
        node = descendantNode
        while node is not None:
            if isinstance(node.tag, str) and re.match('^[hH][1-6]$', node.tag):
                headingLink = deepcopy(node)
                headingLink.tag = 'a'
                headingLink.set('href', '#' + id)
                if 'id' in headingLink.attrib:
                    del headingLink.attrib['id']
                embeddedLinks = headingLink.xpath('.//*[self::dfn or @href or @id]')
                for descendant in embeddedLinks:
                    if descendant.tag == 'a' or descendant.tag == 'dfn':
                        descendant.tag = 'span'
                    if 'href' in descendant.attrib:
                        del descendant.attrib['href']
                    if 'id' in descendant.attrib:
                        del descendant.attrib['id']

                return headingLink
            if node.getprevious() == None:
                node = node.getparent()
            else:
                node = node.getprevious()
                if isinstance(node.tag, str) and node.get('class') == 'impl':
                    node = node.getchildren()[(-1)]

        return

    def addTerms(self, ElementTree, **kwargs):
        utils.replaceComment(ElementTree, 'index-terms', self.terms, **kwargs)