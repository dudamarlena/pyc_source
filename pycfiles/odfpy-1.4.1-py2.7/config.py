# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/config.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import CONFIGNS
from odf.element import Element

def ConfigItem(**args):
    return Element(qname=(CONFIGNS, 'config-item'), **args)


def ConfigItemMapEntry(**args):
    return Element(qname=(CONFIGNS, 'config-item-map-entry'), **args)


def ConfigItemMapIndexed(**args):
    return Element(qname=(CONFIGNS, 'config-item-map-indexed'), **args)


def ConfigItemMapNamed(**args):
    return Element(qname=(CONFIGNS, 'config-item-map-named'), **args)


def ConfigItemSet(**args):
    return Element(qname=(CONFIGNS, 'config-item-set'), **args)