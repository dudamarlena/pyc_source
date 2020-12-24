# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/form.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import FORMNS
from odf.element import Element

def Button(**args):
    return Element(qname=(FORMNS, 'button'), **args)


def Checkbox(**args):
    return Element(qname=(FORMNS, 'checkbox'), **args)


def Column(**args):
    return Element(qname=(FORMNS, 'column'), **args)


def Combobox(**args):
    return Element(qname=(FORMNS, 'combobox'), **args)


def ConnectionResource(**args):
    return Element(qname=(FORMNS, 'connection-resource'), **args)


def Date(**args):
    return Element(qname=(FORMNS, 'date'), **args)


def File(**args):
    return Element(qname=(FORMNS, 'file'), **args)


def FixedText(**args):
    return Element(qname=(FORMNS, 'fixed-text'), **args)


def Form(**args):
    return Element(qname=(FORMNS, 'form'), **args)


def FormattedText(**args):
    return Element(qname=(FORMNS, 'formatted-text'), **args)


def Frame(**args):
    return Element(qname=(FORMNS, 'frame'), **args)


def GenericControl(**args):
    return Element(qname=(FORMNS, 'generic-control'), **args)


def Grid(**args):
    return Element(qname=(FORMNS, 'grid'), **args)


def Hidden(**args):
    return Element(qname=(FORMNS, 'hidden'), **args)


def Image(**args):
    return Element(qname=(FORMNS, 'image'), **args)


def ImageFrame(**args):
    return Element(qname=(FORMNS, 'image-frame'), **args)


def Item(**args):
    return Element(qname=(FORMNS, 'item'), **args)


def ListProperty(**args):
    return Element(qname=(FORMNS, 'list-property'), **args)


def ListValue(**args):
    return Element(qname=(FORMNS, 'list-value'), **args)


def Listbox(**args):
    return Element(qname=(FORMNS, 'listbox'), **args)


def Number(**args):
    return Element(qname=(FORMNS, 'number'), **args)


def Option(**args):
    return Element(qname=(FORMNS, 'option'), **args)


def Password(**args):
    return Element(qname=(FORMNS, 'password'), **args)


def Properties(**args):
    return Element(qname=(FORMNS, 'properties'), **args)


def Property(**args):
    return Element(qname=(FORMNS, 'property'), **args)


def Radio(**args):
    return Element(qname=(FORMNS, 'radio'), **args)


def Text(**args):
    return Element(qname=(FORMNS, 'text'), **args)


def Textarea(**args):
    return Element(qname=(FORMNS, 'textarea'), **args)


def Time(**args):
    return Element(qname=(FORMNS, 'time'), **args)


def ValueRange(**args):
    return Element(qname=(FORMNS, 'value-range'), **args)