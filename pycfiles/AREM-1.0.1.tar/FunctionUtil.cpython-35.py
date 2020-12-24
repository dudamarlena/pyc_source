# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/FunctionUtil.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 3784 bytes
__doc__ = '\nCreated on Dec 31, 2010\n\n@author: Mark V Systems Limited\n(c) Copyright 2010 Mark V Systems Limited, All rights reserved.\n'
import xml.dom, datetime
from arelle import ModelValue, XmlUtil
from arelle.ModelObject import ModelObject, ModelAttribute
from arelle.XPathContext import XPathException, FunctionArgType
from arelle.PythonUtil import pyTypeName

def anytypeArg(xc, args, i, type, missingArgFallback=None):
    if len(args) > i:
        item = args[i]
    else:
        item = missingArgFallback
    if isinstance(item, (tuple, list)):
        if len(item) > 1:
            raise FunctionArgType(i, type, item)
        if len(item) == 0:
            return ()
        item = item[0]
    return item


def atomicArg(xc, p, args, i, type, missingArgFallback=None, emptyFallback=()):
    item = anytypeArg(xc, args, i, type, missingArgFallback)
    if item == ():
        return emptyFallback
    return xc.atomize(p, item)


def stringArg(xc, args, i, type, missingArgFallback=None, emptyFallback=''):
    item = anytypeArg(xc, args, i, type, missingArgFallback)
    if item == ():
        return emptyFallback
    if isinstance(item, (ModelObject, ModelAttribute)):
        return item.text
    return str(item)


def numericArg(xc, p, args, i=0, missingArgFallback=None, emptyFallback=0, convertFallback=None):
    item = anytypeArg(xc, args, i, 'numeric?', missingArgFallback)
    if item == ():
        return emptyFallback
    numeric = xc.atomize(p, item)
    if not isinstance(numeric, _NUM_TYPES):
        if convertFallback is None:
            raise FunctionArgType(i, 'numeric?', numeric)
        try:
            numeric = float(numeric)
        except ValueError:
            numeric = convertFallback

    return numeric


def integerArg(xc, p, args, i=0, missingArgFallback=None, emptyFallback=0, convertFallback=None):
    item = anytypeArg(xc, args, i, 'integer?', missingArgFallback)
    if item == ():
        return emptyFallback
    numeric = xc.atomize(p, item)
    if not isinstance(numeric, _INT_TYPES):
        if convertFallback is None:
            raise FunctionArgType(i, 'integer?', numeric)
        try:
            numeric = _INT(numeric)
        except ValueError:
            numeric = convertFallback

    return numeric


def qnameArg(xc, p, args, i, type, missingArgFallback=None, emptyFallback=()):
    item = anytypeArg(xc, args, i, type, missingArgFallback)
    if item == ():
        return emptyFallback
    qn = xc.atomize(p, item)
    if not isinstance(qn, ModelValue.QName):
        raise FunctionArgType(i, type, qn)
    return qn


def nodeArg(xc, args, i, type, missingArgFallback=None, emptyFallback=None):
    item = anytypeArg(xc, args, i, type, missingArgFallback)
    if item == ():
        return emptyFallback
    if not isinstance(item, (ModelObject, ModelAttribute)):
        raise FunctionArgType(i, type, item)
    return item


def testTypeCompatiblity(xc, p, op, a1, a2):
    if isinstance(a1, ModelValue.DateTime) and isinstance(a2, ModelValue.DateTime):
        if a1.dateOnly == a2.dateOnly:
            return
    elif type(a1) == type(a2) or isinstance(a1, _NUM_TYPES) and isinstance(a2, _NUM_TYPES) or isinstance(a1, _STR_BASE) and isinstance(a2, _STR_BASE):
        return
    if op in ('+', '-'):
        if isinstance(a1, ModelValue.DateTime) and isinstance(a2, (ModelValue.YearMonthDuration, datetime.timedelta)) or isinstance(a1, datetime.date) and isinstance(a2, datetime.timedelta):
            return
    elif isinstance(a1, datetime.date) and isinstance(a2, datetime.date):
        return
    raise XPathException(p, 'err:XPTY0004', _('Value operation {0} incompatible arguments {1} ({2}) and {3} ({4})').format(op, a1, pyTypeName(a1), a2, pyTypeName(a2)))