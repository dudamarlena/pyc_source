# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/office.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import OFFICENS
from odf.element import Element
from odf.draw import StyleRefElement

def Annotation(**args):
    return StyleRefElement(qname=(OFFICENS, 'annotation'), **args)


def AnnotationEnd(**args):
    return StyleRefElement(qname=(OFFICENS, 'annotation-end'), **args)


def AutomaticStyles(**args):
    return Element(qname=(OFFICENS, 'automatic-styles'), **args)


def BinaryData(**args):
    return Element(qname=(OFFICENS, 'binary-data'), **args)


def Body(**args):
    return Element(qname=(OFFICENS, 'body'), **args)


def ChangeInfo(**args):
    return Element(qname=(OFFICENS, 'change-info'), **args)


def Chart(**args):
    return Element(qname=(OFFICENS, 'chart'), **args)


def DdeSource(**args):
    return Element(qname=(OFFICENS, 'dde-source'), **args)


def Document(version='1.2', **args):
    return Element(qname=(OFFICENS, 'document'), version=version, **args)


def DocumentContent(version='1.2', **args):
    return Element(qname=(OFFICENS, 'document-content'), version=version, **args)


def DocumentMeta(version='1.2', **args):
    return Element(qname=(OFFICENS, 'document-meta'), version=version, **args)


def DocumentSettings(version='1.2', **args):
    return Element(qname=(OFFICENS, 'document-settings'), version=version, **args)


def DocumentStyles(version='1.2', **args):
    return Element(qname=(OFFICENS, 'document-styles'), version=version, **args)


def Drawing(**args):
    return Element(qname=(OFFICENS, 'drawing'), **args)


def EventListeners(**args):
    return Element(qname=(OFFICENS, 'event-listeners'), **args)


def FontFaceDecls(**args):
    return Element(qname=(OFFICENS, 'font-face-decls'), **args)


def Forms(**args):
    return Element(qname=(OFFICENS, 'forms'), **args)


def Image(**args):
    return Element(qname=(OFFICENS, 'image'), **args)


def MasterStyles(**args):
    return Element(qname=(OFFICENS, 'master-styles'), **args)


def Meta(**args):
    return Element(qname=(OFFICENS, 'meta'), **args)


def Presentation(**args):
    return Element(qname=(OFFICENS, 'presentation'), **args)


def Script(**args):
    return Element(qname=(OFFICENS, 'script'), **args)


def Scripts(**args):
    return Element(qname=(OFFICENS, 'scripts'), **args)


def Settings(**args):
    return Element(qname=(OFFICENS, 'settings'), **args)


def Spreadsheet(**args):
    return Element(qname=(OFFICENS, 'spreadsheet'), **args)


def Styles(**args):
    return Element(qname=(OFFICENS, 'styles'), **args)


def Text(**args):
    return Element(qname=(OFFICENS, 'text'), **args)