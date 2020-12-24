# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/utopia/tools/provenance.py
# Compiled at: 2017-04-05 11:10:17
import datetime

def hasprovenance(value):
    return hasattr(value, '_provenance') and type(value._provenance) == dict


def provenance(value):
    try:
        return value._provenance
    except AttributeError:
        raise RuntimeError('No associated provenance found for this value')


def wrap_provenance(value, **kwargs):
    kwargs.setdefault('when', datetime.datetime.now())
    if isinstance(kwargs['when'], datetime.datetime):
        kwargs['when'] = kwargs['when'].isoformat()

    class sourced(type(value)):
        _provenance = kwargs

    sourced = sourced(value)
    return sourced