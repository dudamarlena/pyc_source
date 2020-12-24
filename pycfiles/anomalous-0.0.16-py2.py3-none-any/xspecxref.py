# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/xspecxref.py
# Compiled at: 2013-02-15 13:25:53
from __future__ import unicode_literals
from lxml import etree
try:
    import json
except ImportError:
    import simplejson as json

from anolislib import utils
instance_elements = frozenset([b'span', b'abbr', b'code', b'var', b'i'])
w3c_instance_elements = frozenset([b'abbr', b'acronym', b'b', b'bdo', b'big',
 b'code', b'del', b'em', b'i', b'ins',
 b'kbd', b'label', b'legend', b'q', b'samp',
 b'small', b'span', b'strong', b'sub',
 b'sup', b'tt', b'var'])
instance_not_in_stack_with = frozenset([b'dfn'])

class xspecxref(object):
    """Add cross-references."""

    def __init__(self, ElementTree, **kwargs):
        self.dfns = {}
        self.notfound = []
        self.buildReferences(ElementTree, **kwargs)
        self.addReferences(ElementTree, **kwargs)

    def buildReferences(self, ElementTree, xref, allow_duplicate_dfns=False, **kwargs):
        manifest = open(xref + b'/specs.json', b'r')
        specs = json.load(manifest)
        manifest.close()
        for k, v in specs.items():
            file = open(xref + b'/xrefs/' + v, b'r')
            dfn = json.load(file)
            file.close()
            self.dfns[k] = {b'url': dfn[b'url'], b'values': dfn[b'definitions']}

    def addReferences(self, ElementTree, w3c_compat=False, w3c_compat_xref_elements=False, w3c_compat_xref_a_placement=False, use_strict=False, **kwargs):
        for element in ElementTree.iter(tag=etree.Element):
            if (element.tag in instance_elements or (w3c_compat or w3c_compat_xref_elements) and element.tag in w3c_instance_elements) and element.get(b'data-anolis-spec') is not None:
                term = self.getTerm(element, **kwargs)
                spec = element.get(b'data-anolis-spec')
                if w3c_compat:
                    del element.attrib[b'data-anolis-spec']
                if element.get(b'class') is not None:
                    element.set(b'class', element.get(b'class') + b' external')
                else:
                    element.set(b'class', b'external')
                if spec not in self.dfns or not self.dfns[spec]:
                    raise SyntaxError(b'Specification not found: %s.' % spec)
                if not self.dfns[spec][b'values']:
                    raise SyntaxError(b'No values for specification: %s.' % spec)
                if term not in self.dfns[spec][b'values']:
                    self.notfound.append([term, spec])
                    continue
                obj = self.dfns[spec]
                goodParentingAndChildren = True
                for parent_element in element.iterancestors(tag=etree.Element):
                    if parent_element.tag in instance_not_in_stack_with or utils.isInteractiveContent(parent_element):
                        goodParentingAndChildren = False
                        break
                else:
                    for child_element in element.iterdescendants(tag=etree.Element):
                        if child_element.tag in instance_not_in_stack_with or utils.isInteractiveContent(child_element):
                            goodParentingAndChildren = False
                            break

                    if goodParentingAndChildren:
                        if element.tag == b'span':
                            element.tag = b'a'
                            element.set(b'href', obj[b'url'] + obj[b'values'][term])
                        else:
                            link = etree.Element(b'a', {b'href': obj[b'url'] + obj[b'values'][term]})
                            if w3c_compat or w3c_compat_xref_a_placement:
                                for node in element:
                                    link.append(node)

                                link.text = element.text
                                element.text = None
                                element.append(link)
                            else:
                                element.addprevious(link)
                                link.append(element)
                                link.tail = link[0].tail
                                link[0].tail = None

        if self.notfound:
            raise SyntaxError(b'Terms not defined: %s.' % self.notfound)
        return

    def getTerm(self, element, w3c_compat=False, w3c_compat_xref_normalization=False, **kwargs):
        if element.get(b'data-anolis-xref') is not None:
            term = element.get(b'data-anolis-xref')
        elif element.get(b'title') is not None:
            term = element.get(b'title')
        else:
            term = utils.textContent(element)
        term = term.strip(utils.spaceCharacters).lower()
        return utils.spacesRegex.sub(b' ', term)