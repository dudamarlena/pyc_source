# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/lof.py
# Compiled at: 2011-08-30 06:36:54
from lxml import etree
from anolislib import utils

class lof(object):
    """Add a List of Figures."""

    def __init__(self, ElementTree, **kwargs):
        self.tables = []
        self.readDoc(ElementTree, 'Table', 'table', 'caption', self.tables)
        self.addList(ElementTree, self.tables, 'tables')

    def readDoc(self, ElementTree, name, localName, captionLocalName, figures):
        i = 0
        for element in ElementTree.getroot().findall('.//%s' % localName):
            i += 1
            if utils.elementHasClass(element, 'no-num'):
                continue
            if 'id' not in element.attrib:
                element.set('id', 'anolis-%s-%d' % (localName, i))
            id = element.get('id')
            cap = element.find('.//%s' % captionLocalName)
            if cap is None:
                cap = etree.Element('%s' % captionLocalName)
                cap.text = '(untitled)'
                element.append(cap)
            caption = utils.textContent(cap)
            cap.text = '%s %d: %s' % (name, i, cap.text)
            figures.append((id, caption))

        return

    def addList(self, ElementTree, figures, id):
        root = ElementTree.getroot().find(".//div[@id='anolis-listof%s']" % id)
        if root is None:
            raise SyntaxError, 'A <div id=anolis-listof%s> is required.' % id
        ol = etree.Element('ol')
        root.append(ol)
        for figure in figures:
            a = etree.Element('a', {'href': '#' + figure[0]})
            a.text = figure[1]
            li = etree.Element('li')
            li.append(a)
            ol.append(li)

        return