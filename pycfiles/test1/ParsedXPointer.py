# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\XPointer\ParsedXPointer.py
# Compiled at: 2003-01-19 00:08:30
"""
A Parsed Token that represents a list of XPointers
WWW: http://4suite.org/XPointer        e-mail: support@4suite.org

Copyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.
See  http://4suite.org/COPYRIGHT  for license and copyright information
"""
from Ft.Xml.XPath import CoreFunctions
from Ft.Xml.XPointer import XPtrContext, XPtrException
from Ft.Xml.Domlette import GetAllNs

class BareName:
    __module__ = __name__

    def __init__(self, name):
        self.name = name

    def select(self, context):
        doc = context.node.rootNode
        result = CoreFunctions._FindIds(doc, self.name, [])
        if len(result) > 1:
            raise Exception('ID must be unique')
        elif result:
            return result[0].ownerElement
        raise XPtrException(XPtrException.SUB_RESOURCE_ERROR)

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<BareName at %x: %s>' % (id(self), self.name)

    def __repr__(self):
        return self.name


class ChildSequence:
    __module__ = __name__

    def __init__(self, sequence):
        if type(sequence[0]) != type(1):
            self.bareName = sequence[0]
            self.sequence = sequence[1:]
        else:
            self.bareName = None
            self.sequence = sequence
        return

    def select(self, context):
        if self.bareName:
            node = self.bareName.select(context)
        else:
            node = context.node.rootNode
        for index in self.sequence:
            try:
                node = node.childNodes[index]
            except IndexError:
                raise XPtrException(XPtrException.SUB_RESOURCE_ERROR)

        return node

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<ChildSequence at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        result = self.bareName and repr(self.bareName) or ''
        for index in self.sequence:
            result = result + '/%d' % index

        return result


class FullXPtr:
    __module__ = __name__

    def __init__(self, parts):
        self.parts = parts

    def select(self, document, contextNode, nss=None):
        nss = nss or {}
        nss.update(GetAllNs(document))
        context = XPtrContext.XPtrContext(document, 1, 1, contextNode, nss)
        for part in self.parts:
            node_set = part.evaluate(context)
            if len(node_set) == 1:
                return node_set[0]
            elif node_set:
                raise XPtrException(XPtrException.SUB_RESOURCE_ERROR)

        raise XPtrException(XPtrException.SUB_RESOURCE_ERROR)

    def pprint(self, indent=''):
        print indent + str(self)
        for part in self.parts:
            part.pprint(indent + '  ')

    def __str__(self):
        return '<FullXPtr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return reduce(lambda result, part: result + ' ' + repr(part), self.parts, '')