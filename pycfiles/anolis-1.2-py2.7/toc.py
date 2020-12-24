# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/toc.py
# Compiled at: 2013-03-18 06:45:15
from __future__ import unicode_literals
from lxml import etree
from copy import deepcopy
from anolislib import utils
from anolislib.processes import outliner
remove_elements_from_toc = frozenset([b'dfn'])
remove_attributes_from_toc = frozenset([b'id'])

class toc(object):
    """Build and add TOC."""
    toc = None

    def __init__(self, ElementTree, **kwargs):
        self.toc = etree.Element(b'ol', {b'class': b'toc'})
        self.buildToc(ElementTree, **kwargs)
        self.addToc(ElementTree, **kwargs)

    def buildToc(self, ElementTree, min_depth=2, max_depth=6, w3c_compat=False, w3c_compat_class_toc=False, **kwargs):
        outline_creator = outliner.Outliner(ElementTree, **kwargs)
        outline = outline_creator.build(**kwargs)
        sections = [ (section, 0) for section in reversed(outline) ]
        num = []
        while sections:
            section, depth = sections.pop()
            if section.header is not None:
                if section.header.tag == b'hgroup':
                    i = 1
                    while 1:
                        if i <= 6:
                            header_text = section.header.find(b'.//h%i' % i)
                            if header_text is not None:
                                break
                            i += 1
                    else:
                        header_text = None

                else:
                    header_text = section.header
            else:
                header_text = None
            if header_text is not None:
                for element in header_text.findall(b'.//span'):
                    if utils.elementHasClass(element, b'secno'):
                        utils.copyContentForRemoval(element, text=False, children=False)
                        element.getparent().remove(element)

            if depth >= min_depth - 1 and depth <= max_depth - 1:
                corrected_depth = depth - min_depth + 1
                if corrected_depth + 1 < len(num):
                    del num[corrected_depth + 1:]
                elif corrected_depth == len(num):
                    num.append(0)
                if header_text is not None and not utils.elementHasClass(header_text, b'no-num') or header_text is None and section:
                    num[(-1)] += 1
                if header_text is not None and not utils.elementHasClass(header_text, b'no-toc') or header_text is None and section:
                    i = 0
                    toc_section = self.toc
                    while i < corrected_depth:
                        try:
                            if len(toc_section[(-1)]) == 0 or toc_section[(-1)][(-1)].tag != b'ol':
                                toc_section[(-1)].append(etree.Element(b'ol'))
                                utils.indentNode(toc_section[(-1)][(-1)], ((i + 1) * 2), **kwargs)
                                if w3c_compat or w3c_compat_class_toc:
                                    toc_section[(-1)][(-1)].set(b'class', b'toc')
                        except IndexError:
                            toc_section.append(etree.Element(b'li'))
                            utils.indentNode(toc_section[0], ((i + 1) * 2 - 1), **kwargs)
                            toc_section[0].append(etree.Element(b'ol'))
                            utils.indentNode(toc_section[0][0], ((i + 1) * 2), **kwargs)
                            if w3c_compat or w3c_compat_class_toc:
                                toc_section[0][0].set(b'class', b'toc')

                        assert toc_section[(-1)].tag == b'li'
                        assert toc_section[(-1)][(-1)].tag == b'ol'
                        toc_section = toc_section[(-1)][(-1)]
                        i += 1

                    item = etree.Element(b'li')
                    toc_section.append(item)
                    utils.indentNode(item, ((i + 1) * 2 - 1), **kwargs)
                if header_text is not None:
                    id = utils.generateID(header_text, **kwargs)
                    if header_text.get(b'id') is not None:
                        del header_text.attrib[b'id']
                    section.header.set(b'id', id)
                    header_text[0:0] = utils.elementHasClass(header_text, b'no-num') or [
                     etree.Element(b'span', {b'class': b'secno'})]
                    header_text[0].tail = header_text.text
                    header_text.text = None
                    header_text[0].text = (b'.').join(b'%s' % n for n in num)
                    header_text[0].text += b' '
                if not utils.elementHasClass(header_text, b'no-toc'):
                    link = deepcopy(header_text)
                    item.append(link)
                    link.tag = b'a'
                    link.set(b'href', b'#' + id)
                    utils.removeInteractiveContentChildren(link)
                    for element_name in remove_elements_from_toc:
                        for element in link.findall(b'.//' + element_name):
                            utils.copyContentForRemoval(element)
                            element.getparent().remove(element)

                    for element in link.iter(tag=etree.Element):
                        for attribute_name in remove_attributes_from_toc:
                            if element.get(attribute_name) is not None:
                                del element.attrib[attribute_name]

                    link.tail = None
                    if not utils.textContent(header_text) == utils.textContent(link):
                        raise AssertionError
            sections.extend([ (child_section, depth + 1) for child_section in reversed(section)
                            ])

        return

    def addToc(self, ElementTree, **kwargs):
        utils.replaceComment(ElementTree, b'toc', self.toc, **kwargs)


class DifferentParentException(utils.AnolisException):
    """begin-toc and end-toc do not have the same parent."""
    pass