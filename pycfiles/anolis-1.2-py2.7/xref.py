# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/xref.py
# Compiled at: 2013-02-16 15:38:05
from __future__ import unicode_literals
import re
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
non_alphanumeric_spaces = re.compile(b'[^a-zA-Z0-9 \\-\\_\\/\\|]+')

class xref(object):
    """Add cross-references."""

    def __init__(self, ElementTree, dump_xrefs=b'', dump_backrefs=False, **kwargs):
        self.dfns = {}
        self.instances = {}
        self.buildReferences(ElementTree, dump_backrefs=dump_backrefs, **kwargs)
        if dump_xrefs:
            self.dump(self.getDfns(dump_xrefs), dump_xrefs, **kwargs)
        self.addReferences(ElementTree, dump_backrefs=dump_backrefs, **kwargs)
        if dump_backrefs:
            self.dump(self.instances, b'backrefs.json', **kwargs)

    def buildReferences(self, ElementTree, allow_duplicate_dfns=False, **kwargs):
        for dfn in ElementTree.iter(b'dfn'):
            terms = self.getTerm(dfn, **kwargs).split(b'|')
            for term in set(t for t in terms if t):
                if not allow_duplicate_dfns and term in self.dfns:
                    raise DuplicateDfnException(b'The term "%s" is defined more than once' % term)
                link_to = dfn
                for parent_element in dfn.iterancestors(tag=etree.Element):
                    if parent_element.tag in utils.heading_content:
                        link_to = parent_element
                        break

                id = utils.generateID(link_to, **kwargs)
                link_to.set(b'id', id)
                self.dfns[term] = id
                self.instances[term] = []

    def getDfns(self, dump_xrefs, **kwargs):
        try:
            fp = open(dump_xrefs, b'r')
            data = json.load(fp)
            fp.close()
            data[b'definitions'] = self.dfns
            return data
        except IOError:
            raise XrefsFileNotCreatedYetException(b"No such file or directory: '%s'. Please create it first.\nIt should contain a an object with a 'url' property (whose value ends with a '#')." % dump_xrefs)

    def dump(self, obj, f, **kwargs):
        d = json.dumps(obj, sort_keys=True, allow_nan=False, indent=2, separators=(',',
                                                                                   ': '))
        fp = open(f, b'w')
        fp.write(d + b'\n')
        fp.close()

    def addReferences(self, ElementTree, w3c_compat=False, w3c_compat_xref_elements=False, w3c_compat_xref_a_placement=False, use_strict=False, dump_backrefs=False, **kwargs):
        for element in ElementTree.iter(tag=etree.Element):
            if element.tag in instance_elements or (w3c_compat or w3c_compat_xref_elements) and element.tag in w3c_instance_elements:
                term = self.getTerm(element, w3c_compat=w3c_compat, **kwargs)
                if term in self.dfns:
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
                                element.set(b'href', b'#' + self.dfns[term])
                                link = element
                            else:
                                link = etree.Element(b'a', {b'href': b'#' + self.dfns[term]})
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
                            if dump_backrefs:
                                t = utils.non_ifragment.sub(b'-', term.strip(utils.spaceCharacters)).strip(b'-')
                                id = b'instance_' + t + b'_' + str(len(self.instances[term]))
                                link.set(b'id', id)
                                self.instances[term].append(id)
                elif use_strict and term and not utils.elementHasClass(element, b'secno') and b'data-anolis-spec' not in element.attrib and b'data-anolis-ref' not in element.attrib and element.getparent().tag not in instance_not_in_stack_with:
                    raise SyntaxError(b'Term not defined: %s, %s.' % (term, element))

        return

    def getTerm(self, element, w3c_compat=False, w3c_compat_xref_normalization=False, **kwargs):
        if element.get(b'data-anolis-xref') is not None:
            term = element.get(b'data-anolis-xref')
        elif element.get(b'title') is not None:
            term = element.get(b'title')
        else:
            term = utils.textContent(element)
        term = term.strip(utils.spaceCharacters).lower()
        term = utils.spacesRegex.sub(b' ', term)
        if w3c_compat or w3c_compat_xref_normalization:
            term = non_alphanumeric_spaces.sub(b'', term)
        return term


class DuplicateDfnException(utils.AnolisException):
    """Term already defined."""
    pass


class XrefsFileNotCreatedYetException(utils.AnolisException):
    """The argument to --dump-xrefs does not exist yet."""
    pass