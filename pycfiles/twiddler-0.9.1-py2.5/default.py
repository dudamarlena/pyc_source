# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/twiddler/output/default.py
# Compiled at: 2008-07-24 14:48:01
from elementtree.ElementTree import Comment
from elementtree.ElementTree import _escape_cdata
from elementtree.ElementTree import ProcessingInstruction
from elementtree.ElementTree import QName
from elementtree.ElementTree import _raise_serialization_error
from twiddler.elementtreeplus import DocType
from twiddler.elementtreeplus import XMLDeclaration
from twiddler.interfaces import IOutput
from zope.interface import directlyProvides

def _render(output, node, namespaces):
    tag = node.tag
    if tag is Comment:
        output.append('<!--%s-->' % _escape_cdata(node.text))
    else:
        if tag is ProcessingInstruction:
            output.append('<?%s?>' % _escape_cdata(node.text))
        else:
            if tag in (XMLDeclaration, DocType):
                output.append(node.text)
            elif tag is False:
                if node.text:
                    output.append(node.text)
                for n in node:
                    _render(output, n, namespaces)

            else:
                items = node.items()
                xmlns_items = []
                try:
                    if isinstance(tag, QName) or tag[:1] == '{':
                        (tag, xmlns) = fixtag(tag, namespaces)
                        if xmlns:
                            xmlns_items.append(xmlns)
                except TypeError:
                    _raise_serialization_error(tag)

            output.append('<' + tag)
            if items or xmlns_items:
                items.sort()
                for (k, v) in items:
                    try:
                        if isinstance(k, QName) or k[:1] == '{':
                            (k, xmlns) = fixtag(k, namespaces)
                            if xmlns:
                                xmlns_items.append(xmlns)
                    except TypeError:
                        _raise_serialization_error(k)

                    try:
                        if isinstance(v, QName):
                            (v, xmlns) = fixtag(v, namespaces)
                            if xmlns:
                                xmlns_items.append(xmlns)
                    except TypeError:
                        _raise_serialization_error(v)

                    output.append(' %s="%s"' % (k, v))

                for (k, v) in xmlns_items:
                    output.append(' %s="%s"' % (k, v))

        if node.text or len(node):
            output.append('>')
            if node.text:
                output.append(node.text)
            for n in node:
                _render(output, n, namespaces)

            output.append('</' + tag + '>')
        else:
            output.append(' />')
    for (k, v) in xmlns_items:
        del namespaces[v]

    if node.tail:
        output.append(node.tail)


def Default(root, *args, **kw):
    """Default output renderer"""
    output = []
    _render(output, root._root, {})
    return ('').join(output)


directlyProvides(Default, IOutput)