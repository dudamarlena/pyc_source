# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/refs.py
# Compiled at: 2013-02-15 13:24:09
from lxml import etree
try:
    import json
except ImportError:
    import simplejson as json

from anolislib import utils

class refs(object):
    """Add references section."""

    def __init__(self, ElementTree, split_references_section=False, **kwargs):
        self.refs = {}
        self.usedrefs = []
        self.foundrefs = {}
        self.normativerefs = {}
        self.addReferencesLinks(ElementTree, **kwargs)
        self.usedrefs.sort()
        self.buildReferences(ElementTree, **kwargs)
        if not split_references_section:
            self.addReferencesList(ElementTree, **kwargs)
        else:
            self.addTwoReferencesLists(ElementTree, **kwargs)

    def addDD(self, dl, ref, informative):
        if isinstance(self.refs[ref], list):
            data = self.refs[ref]
        else:
            data = [
             self.refs[ref]]
        for r in data:
            dl.append(self.createReference(r, informative))

    def buildReferences(self, ElementTree, xref='data', **kwargs):
        list = open(xref + '/references.json', 'r')
        self.refs = json.load(list)
        list.close()

    def addTwoReferencesLists(self, ElementTree, **kwargs):
        informative = []
        normative = []
        for ref in self.usedrefs:
            if ref in self.normativerefs:
                normative.append(ref)
            else:
                informative.append(ref)

        self.addPartialReferencesList(ElementTree, normative, 'normative', **kwargs)
        self.addPartialReferencesList(ElementTree, informative, 'informative', **kwargs)

    def addPartialReferencesList(self, ElementTree, l, id, **kwargs):
        if not len(l):
            return
        else:
            root = ElementTree.getroot().find(".//div[@id='anolis-references-%s']" % id)
            if root is None:
                raise SyntaxError('A <div id=anolis-references-%s> is required.' % id)
            dl = etree.Element('dl')
            root.append(dl)
            for ref in l:
                if ref not in self.refs:
                    raise SyntaxError('Reference not defined: %s.' % ref)
                dt = etree.Element('dt')
                dt.set('id', 'refs' + ref)
                dt.text = '[' + ref + ']\n'
                dl.append(dt)
                self.addDD(dl, ref, False)

            return

    def addReferencesList(self, ElementTree, **kwargs):
        root = ElementTree.getroot().find(".//div[@id='anolis-references']")
        if root is None:
            raise SyntaxError('A <div id=anolis-references> is required.')
        dl = etree.Element('dl')
        root.append(dl)
        for ref in self.usedrefs:
            if ref not in self.refs:
                raise SyntaxError('Reference not defined: %s.' % ref)
            dt = etree.Element('dt')
            dt.set('id', 'refs' + ref)
            dt.text = '[' + ref + ']\n'
            dl.append(dt)
            self.addDD(dl, ref, ref not in self.normativerefs)

        return

    def createReference(self, ref, informative):
        cite = etree.Element('cite')
        if 'href' in ref:
            a = etree.Element('a')
            if 'title' in ref:
                a.text = ref['title']
            else:
                a.text = ref['href']
            a.set('href', ref['href'])
            cite.append(a)
        elif 'title' in ref:
            cite.text = ref['title']
        cite.tail = ''
        if 'authors' in ref:
            cite.tail += ', %s.' % self.formatAuthors(ref['authors'])
        else:
            cite.tail += '.'
        if 'publisher' in ref:
            cite.tail += ' %s.' % ref['publisher']
        if 'isbn' in ref:
            cite.tail += ' ISBN %s.' % ref['isbn']
        cite.tail += '\n\n'
        dd = etree.Element('dd')
        if informative:
            dd.text = '(Non-normative) '
        dd.append(cite)
        return dd

    def formatAuthors(self, authors):
        if len(authors) >= 4:
            return '%s, %s, %s et al.' % tuple(authors[:3])
        if len(authors) == 1:
            return '%s' % (authors[0],)
        last = authors.pop()
        return '%s and %s' % ((', ').join(authors), last)

    def addReferencesLinks(self, ElementTree, **kwargs):
        for element in ElementTree.getroot().findall('.//span[@data-anolis-ref]'):
            del element.attrib['data-anolis-ref']
            ref = element.text
            element.tag = 'a'
            element.set('href', '#refs' + ref)
            element.text = '[' + ref + ']'
            if not utils.elementHasClass(element, 'informative'):
                self.normativerefs[ref] = True
            if ref not in self.foundrefs:
                self.usedrefs.append(ref)
                self.foundrefs[ref] = True