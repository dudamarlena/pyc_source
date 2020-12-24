# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/util/converters.py
# Compiled at: 2009-07-20 09:44:04


def asbool(obj):
    if isinstance(obj, (str, unicode)):
        obj = obj.strip().lower()
        if obj in ('true', 'yes', 'on', 'y', 't', '1'):
            return True
        if obj in ('false', 'no', 'off', 'n', 'f', '0'):
            return False
        raise ValueError('String is not true/false: %r' % obj)
    return bool(obj)


def aslist(obj, sep=None, strip=True):
    if isinstance(obj, (str, unicode)):
        lst = obj.split(sep)
        if strip:
            lst = [ v.strip() for v in lst ]
        return lst
    else:
        if isinstance(obj, (list, tuple)):
            return obj
        else:
            if obj is None:
                return []
            return [obj]
        return