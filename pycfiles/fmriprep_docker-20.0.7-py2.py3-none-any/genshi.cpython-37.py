# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_vendor/html5lib/treewalkers/genshi.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 2309 bytes
from __future__ import absolute_import, division, unicode_literals
from genshi.core import QName
from genshi.core import START, END, XML_NAMESPACE, DOCTYPE, TEXT
from genshi.core import START_NS, END_NS, START_CDATA, END_CDATA, PI, COMMENT
from . import base
from ..constants import voidElements, namespaces

class TreeWalker(base.TreeWalker):

    def __iter__(self):
        previous = None
        for event in self.tree:
            if previous is not None:
                for token in self.tokens(previous, event):
                    yield token

            previous = event

        if previous is not None:
            for token in self.tokens(previous, None):
                yield token

    def tokens(self, event, next):
        kind, data, _ = event
        if kind == START:
            tag, attribs = data
            name = tag.localname
            namespace = tag.namespace
            converted_attribs = {}
            for k, v in attribs:
                if isinstance(k, QName):
                    converted_attribs[(k.namespace, k.localname)] = v
                else:
                    converted_attribs[(None, k)] = v

            if namespace == namespaces['html']:
                if name in voidElements:
                    for token in self.emptyTag(namespace, name, converted_attribs, not next or next[0] != END or next[1] != tag):
                        yield token

                else:
                    yield self.startTag(namespace, name, converted_attribs)
            else:
                pass
        if kind == END:
            name = data.localname
            namespace = data.namespace
            if namespace != namespaces['html'] or name not in voidElements:
                yield self.endTag(namespace, name)
        else:
            if kind == COMMENT:
                yield self.comment(data)
            else:
                if kind == TEXT:
                    for token in self.text(data):
                        yield token

                else:
                    if kind == DOCTYPE:
                        yield (self.doctype)(*data)
                    else:
                        if kind in (XML_NAMESPACE, DOCTYPE, START_NS, END_NS,
                         START_CDATA, END_CDATA, PI):
                            pass
                        else:
                            yield self.unknown(kind)