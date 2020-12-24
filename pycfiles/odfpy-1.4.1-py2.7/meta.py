# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/meta.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import METANS
from odf.element import Element

def AutoReload(**args):
    return Element(qname=(METANS, 'auto-reload'), **args)


def CreationDate(**args):
    return Element(qname=(METANS, 'creation-date'), **args)


def DateString(**args):
    return Element(qname=(METANS, 'date-string'), **args)


def DocumentStatistic(**args):
    return Element(qname=(METANS, 'document-statistic'), **args)


def EditingCycles(**args):
    return Element(qname=(METANS, 'editing-cycles'), **args)


def EditingDuration(**args):
    return Element(qname=(METANS, 'editing-duration'), **args)


def Generator(**args):
    return Element(qname=(METANS, 'generator'), **args)


def HyperlinkBehaviour(**args):
    return Element(qname=(METANS, 'hyperlink-behaviour'), **args)


def InitialCreator(**args):
    return Element(qname=(METANS, 'initial-creator'), **args)


def Keyword(**args):
    return Element(qname=(METANS, 'keyword'), **args)


def PrintDate(**args):
    return Element(qname=(METANS, 'print-date'), **args)


def PrintedBy(**args):
    return Element(qname=(METANS, 'printed-by'), **args)


def Template(**args):
    args.setdefault('type', 'simple')
    return Element(qname=(METANS, 'template'), **args)


def UserDefined(**args):
    return Element(qname=(METANS, 'user-defined'), **args)