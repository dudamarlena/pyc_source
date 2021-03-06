# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/asciify.py
# Compiled at: 2016-11-12 07:38:04
import unicodedata

def _remove_accents(data):
    """
    Changes accented letters to non-accented approximation, like Nestle

    """
    return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore')


def _asciify_list(data):
    """ Ascii-fies list values """
    ret = []
    for item in data:
        if isinstance(item, unicode):
            item = _remove_accents(item)
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _asciify_list(item)
        elif isinstance(item, dict):
            item = _asciify_dict(item)
        ret.append(item)

    return ret


def _asciify_dict(data):
    """ Ascii-fies dict keys and values """
    ret = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = _remove_accents(key)
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = _remove_accents(value)
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _asciify_list(value)
        elif isinstance(value, dict):
            value = _asciify_dict(value)
        ret[key] = value

    return ret


def asciify(data):
    if isinstance(data, list):
        return _asciify_list(data)
    if isinstance(data, dict):
        return _asciify_dict(data)
    if isinstance(data, unicode):
        data = _remove_accents(data)
        return data.encode('utf-8')
    if isinstance(data, str):
        return data
    raise TypeError('Input must be dict, list, str or unicode')