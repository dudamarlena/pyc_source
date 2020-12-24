# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/fandango_search.py
# Compiled at: 2019-08-19 15:09:29
"""
fandango_search.py: methods for getting matching device/attribute/alias names 
from Tango database

These methods have been borrowed from fandango modules.
"""
from builtins import str
import re, taurus

def searchCl(regexp, target):
    return re.search(extend_regexp(regexp).lower(), target.lower())


def matchCl(regexp, target):
    return re.match(extend_regexp(regexp).lower(), target.lower())


def is_regexp(s):
    return any(c in s for c in '.*[]()+?')


def extend_regexp(s):
    s = str(s).strip()
    if '.*' not in s:
        s = s.replace('*', '.*')
    if '.*' not in s:
        if ' ' in s:
            s = s.replace(' ', '.*')
        if '/' not in s:
            s = '.*' + s + '.*'
    else:
        if not s.startswith('^'):
            s = '^' + s
        if not s.endswith('$'):
            s = s + '$'
    return s


def isString(s):
    typ = s.__class__.__name__.lower()
    return not hasattr(s, '__iter__') and 'str' in typ and 'list' not in typ


def isCallable(obj):
    return hasattr(obj, '__call__')


def isMap(obj):
    return hasattr(obj, 'has_key') or hasattr(obj, 'items')


def isDictionary(obj):
    return isMap(obj)


def isSequence(obj):
    typ = obj.__class__.__name__.lower()
    return (hasattr(obj, '__iter__') or 'list' in typ) and not isString(obj) and not isMap(obj)


def split_model_list(modelNames):
    """convert str to list if needed (commas and whitespace are considered as separators)"""
    if isString(modelNames):
        modelNames = str(modelNames).replace(',', ' ')
        modelNames = modelNames.split()
    if isSequence(modelNames):
        modelNames = [ str(s) for s in modelNames ]
    return modelNames


def get_matching_devices(expressions, limit=0, exported=False):
    """
    Searches for devices matching expressions, if exported is True only running devices are returned
    """
    db = taurus.Authority()
    all_devs = [ s.lower() for s in db.get_device_name('*', '*') ]
    result = [ e for e in expressions if e.lower() in all_devs ]
    expressions = [ extend_regexp(e) for e in expressions if e not in result ]
    result.extend([ d for d in all_devs if any(matchCl(extend_regexp(e), d) for e in expressions)
                  ])
    return result


def get_device_for_alias(alias):
    db = taurus.Authority()
    try:
        return db.get_device_alias(alias)
    except Exception as e:
        if 'no device found' in str(e).lower():
            return
        return

    return


def get_alias_for_device(dev):
    db = taurus.Authority()
    try:
        result = db.get_alias(dev)
        return result
    except Exception as e:
        if 'no alias found' in str(e).lower():
            return
        return

    return


def get_alias_dict(exp='*'):
    tango = taurus.Authority()
    return dict((k, tango.get_device_alias(k)) for k in tango.get_device_alias_list(exp))