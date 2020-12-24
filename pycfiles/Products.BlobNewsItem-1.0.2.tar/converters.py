# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteDeploy-1.5.0-py2.6.egg/paste/deploy/converters.py
# Compiled at: 2012-02-27 07:41:55
from paste.deploy.compat import basestring

def asbool(obj):
    if isinstance(obj, basestring):
        obj = obj.strip().lower()
        if obj in ('true', 'yes', 'on', 'y', 't', '1'):
            return True
        if obj in ('false', 'no', 'off', 'n', 'f', '0'):
            return False
        raise ValueError('String is not true/false: %r' % obj)
    return bool(obj)


def asint(obj):
    try:
        return int(obj)
    except (TypeError, ValueError):
        raise ValueError('Bad integer value: %r' % obj)


def aslist(obj, sep=None, strip=True):
    if isinstance(obj, basestring):
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