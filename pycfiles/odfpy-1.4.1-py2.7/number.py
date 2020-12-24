# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/number.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import NUMBERNS
from odf.element import Element
from odf.style import StyleElement

def AmPm(**args):
    return Element(qname=(NUMBERNS, 'am-pm'), **args)


def Boolean(**args):
    return Element(qname=(NUMBERNS, 'boolean'), **args)


def BooleanStyle(**args):
    return StyleElement(qname=(NUMBERNS, 'boolean-style'), **args)


def CurrencyStyle(**args):
    return StyleElement(qname=(NUMBERNS, 'currency-style'), **args)


def CurrencySymbol(**args):
    return Element(qname=(NUMBERNS, 'currency-symbol'), **args)


def DateStyle(**args):
    return StyleElement(qname=(NUMBERNS, 'date-style'), **args)


def Day(**args):
    return Element(qname=(NUMBERNS, 'day'), **args)


def DayOfWeek(**args):
    return Element(qname=(NUMBERNS, 'day-of-week'), **args)


def EmbeddedText(**args):
    return Element(qname=(NUMBERNS, 'embedded-text'), **args)


def Era(**args):
    return Element(qname=(NUMBERNS, 'era'), **args)


def Fraction(**args):
    return Element(qname=(NUMBERNS, 'fraction'), **args)


def Hours(**args):
    return Element(qname=(NUMBERNS, 'hours'), **args)


def Minutes(**args):
    return Element(qname=(NUMBERNS, 'minutes'), **args)


def Month(**args):
    return Element(qname=(NUMBERNS, 'month'), **args)


def Number(**args):
    return Element(qname=(NUMBERNS, 'number'), **args)


def NumberStyle(**args):
    return StyleElement(qname=(NUMBERNS, 'number-style'), **args)


def PercentageStyle(**args):
    return StyleElement(qname=(NUMBERNS, 'percentage-style'), **args)


def Quarter(**args):
    return Element(qname=(NUMBERNS, 'quarter'), **args)


def ScientificNumber(**args):
    return Element(qname=(NUMBERNS, 'scientific-number'), **args)


def Seconds(**args):
    return Element(qname=(NUMBERNS, 'seconds'), **args)


def Text(**args):
    return Element(qname=(NUMBERNS, 'text'), **args)


def TextContent(**args):
    return Element(qname=(NUMBERNS, 'text-content'), **args)


def TextStyle(**args):
    return StyleElement(qname=(NUMBERNS, 'text-style'), **args)


def TimeStyle(**args):
    return StyleElement(qname=(NUMBERNS, 'time-style'), **args)


def WeekOfYear(**args):
    return Element(qname=(NUMBERNS, 'week-of-year'), **args)


def Year(**args):
    return Element(qname=(NUMBERNS, 'year'), **args)