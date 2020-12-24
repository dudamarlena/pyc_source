# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_metadata/safe.py
# Compiled at: 2010-01-20 18:10:58
from hachoir_core.error import HACHOIR_ERRORS, warning

def fault_tolerant(func, *args):

    def safe_func(*args, **kw):
        try:
            func(*args, **kw)
        except HACHOIR_ERRORS, err:
            warning('Error when calling function %s(): %s' % (func.__name__, err))

    return safe_func


def getFieldAttribute(fieldset, key, attrname):
    try:
        field = fieldset[key]
        if field.hasValue():
            return getattr(field, attrname)
    except HACHOIR_ERRORS, err:
        warning('Unable to get %s of field %s/%s: %s' % (attrname, fieldset.path, key, err))

    return


def getValue(fieldset, key):
    return getFieldAttribute(fieldset, key, 'value')


def getDisplay(fieldset, key):
    return getFieldAttribute(fieldset, key, 'display')