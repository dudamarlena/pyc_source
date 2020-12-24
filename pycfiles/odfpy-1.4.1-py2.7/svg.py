# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/svg.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import SVGNS
from odf.element import Element
from odf.draw import DrawElement

def DefinitionSrc(**args):
    args.setdefault('type', 'simple')
    return Element(qname=(SVGNS, 'definition-src'), **args)


def Desc(**args):
    return Element(qname=(SVGNS, 'desc'), **args)


def FontFaceFormat(**args):
    return Element(qname=(SVGNS, 'font-face-format'), **args)


def FontFaceName(**args):
    return Element(qname=(SVGNS, 'font-face-name'), **args)


def FontFaceSrc(**args):
    return Element(qname=(SVGNS, 'font-face-src'), **args)


def FontFaceUri(**args):
    args.setdefault('type', 'simple')
    return Element(qname=(SVGNS, 'font-face-uri'), **args)


def Lineargradient(**args):
    return DrawElement(qname=(SVGNS, 'linearGradient'), **args)


def Radialgradient(**args):
    return DrawElement(qname=(SVGNS, 'radialGradient'), **args)


def Stop(**args):
    return Element(qname=(SVGNS, 'stop'), **args)


def Title(**args):
    return Element(qname=(SVGNS, 'title'), **args)