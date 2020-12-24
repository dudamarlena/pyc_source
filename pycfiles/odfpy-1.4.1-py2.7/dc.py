# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/dc.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import DCNS
from odf.element import Element

def Creator(**args):
    return Element(qname=(DCNS, 'creator'), **args)


def Date(**args):
    return Element(qname=(DCNS, 'date'), **args)


def Description(**args):
    return Element(qname=(DCNS, 'description'), **args)


def Language(**args):
    return Element(qname=(DCNS, 'language'), **args)


def Subject(**args):
    return Element(qname=(DCNS, 'subject'), **args)


def Title(**args):
    return Element(qname=(DCNS, 'title'), **args)