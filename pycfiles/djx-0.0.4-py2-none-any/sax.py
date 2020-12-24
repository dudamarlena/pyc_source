# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-HZd96S/pip/pip/_vendor/html5lib/treeadapters/sax.py
# Compiled at: 2019-02-14 00:35:07
from __future__ import absolute_import, division, unicode_literals
from xml.sax.xmlreader import AttributesNSImpl
from ..constants import adjustForeignAttributes, unadjustForeignAttributes
prefix_mapping = {}
for prefix, localName, namespace in adjustForeignAttributes.values():
    if prefix is not None:
        prefix_mapping[prefix] = namespace

def to_sax(walker, handler):
    """Call SAX-like content handler based on treewalker walker

    :arg walker: the treewalker to use to walk the tree to convert it

    :arg handler: SAX handler to use

    """
    handler.startDocument()
    for prefix, namespace in prefix_mapping.items():
        handler.startPrefixMapping(prefix, namespace)

    for token in walker:
        type = token[b'type']
        if type == b'Doctype':
            continue
        elif type in ('StartTag', 'EmptyTag'):
            attrs = AttributesNSImpl(token[b'data'], unadjustForeignAttributes)
            handler.startElementNS((token[b'namespace'], token[b'name']), token[b'name'], attrs)
            if type == b'EmptyTag':
                handler.endElementNS((token[b'namespace'], token[b'name']), token[b'name'])
        elif type == b'EndTag':
            handler.endElementNS((token[b'namespace'], token[b'name']), token[b'name'])
        elif type in ('Characters', 'SpaceCharacters'):
            handler.characters(token[b'data'])
        elif type == b'Comment':
            pass
        elif not False:
            raise AssertionError(b'Unknown token type')

    for prefix, namespace in prefix_mapping.items():
        handler.endPrefixMapping(prefix)

    handler.endDocument()