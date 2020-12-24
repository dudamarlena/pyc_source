# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/presentation.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import PRESENTATIONNS
from odf.element import Element

def AnimationGroup(**args):
    return Element(qname=(PRESENTATIONNS, 'animation-group'), **args)


def Animations(**args):
    return Element(qname=(PRESENTATIONNS, 'animations'), **args)


def DateTime(**args):
    return Element(qname=(PRESENTATIONNS, 'date-time'), **args)


def DateTimeDecl(**args):
    return Element(qname=(PRESENTATIONNS, 'date-time-decl'), **args)


def Dim(**args):
    return Element(qname=(PRESENTATIONNS, 'dim'), **args)


def EventListener(**args):
    return Element(qname=(PRESENTATIONNS, 'event-listener'), **args)


def Footer(**args):
    return Element(qname=(PRESENTATIONNS, 'footer'), **args)


def FooterDecl(**args):
    return Element(qname=(PRESENTATIONNS, 'footer-decl'), **args)


def Header(**args):
    return Element(qname=(PRESENTATIONNS, 'header'), **args)


def HeaderDecl(**args):
    return Element(qname=(PRESENTATIONNS, 'header-decl'), **args)


def HideShape(**args):
    return Element(qname=(PRESENTATIONNS, 'hide-shape'), **args)


def HideText(**args):
    return Element(qname=(PRESENTATIONNS, 'hide-text'), **args)


def Notes(**args):
    return Element(qname=(PRESENTATIONNS, 'notes'), **args)


def Placeholder(**args):
    return Element(qname=(PRESENTATIONNS, 'placeholder'), **args)


def Play(**args):
    return Element(qname=(PRESENTATIONNS, 'play'), **args)


def Settings(**args):
    return Element(qname=(PRESENTATIONNS, 'settings'), **args)


def Show(**args):
    return Element(qname=(PRESENTATIONNS, 'show'), **args)


def ShowShape(**args):
    return Element(qname=(PRESENTATIONNS, 'show-shape'), **args)


def ShowText(**args):
    return Element(qname=(PRESENTATIONNS, 'show-text'), **args)


def Sound(**args):
    args.setdefault('type', 'simple')
    return Element(qname=(PRESENTATIONNS, 'sound'), **args)