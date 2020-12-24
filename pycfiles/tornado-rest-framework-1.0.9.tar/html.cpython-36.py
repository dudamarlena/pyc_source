# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/70/_7dmwj6x12q099dhb0z0p7p80000gn/T/pycharm-packaging/djangorestframework/rest_framework/utils/html.py
# Compiled at: 2018-05-14 04:48:23
# Size of source mod 2**32: 2072 bytes
"""
Helpers for dealing with HTML input.
"""
import re
from django.utils.datastructures import MultiValueDict

def is_html_input(dictionary):
    return hasattr(dictionary, 'getlist')


def parse_html_list(dictionary, prefix=''):
    """
    Used to support list values in HTML forms.
    Supports lists of primitives and/or dictionaries.

    * List of primitives.

    {
        '[0]': 'abc',
        '[1]': 'def',
        '[2]': 'hij'
    }
        -->
    [
        'abc',
        'def',
        'hij'
    ]

    * List of dictionaries.

    {
        '[0]foo': 'abc',
        '[0]bar': 'def',
        '[1]foo': 'hij',
        '[1]bar': 'klm',
    }
        -->
    [
        {'foo': 'abc', 'bar': 'def'},
        {'foo': 'hij', 'bar': 'klm'}
    ]
    """
    ret = {}
    regex = re.compile('^%s\\[([0-9]+)\\](.*)$' % re.escape(prefix))
    for field, value in dictionary.items():
        match = regex.match(field)
        if not match:
            pass
        else:
            index, key = match.groups()
            index = int(index)
            if not key:
                ret[index] = value
            else:
                if isinstance(ret.get(index), dict):
                    ret[index][key] = value
                else:
                    ret[index] = MultiValueDict({key: [value]})

    return [ret[item] for item in sorted(ret)]


def parse_html_dict(dictionary, prefix=''):
    """
    Used to support dictionary values in HTML forms.

    {
        'profile.username': 'example',
        'profile.email': 'example@example.com',
    }
        -->
    {
        'profile': {
            'username': 'example',
            'email': 'example@example.com'
        }
    }
    """
    ret = MultiValueDict()
    regex = re.compile('^%s\\.(.+)$' % re.escape(prefix))
    for field in dictionary:
        match = regex.match(field)
        if not match:
            pass
        else:
            key = match.groups()[0]
            value = dictionary.getlist(field)
            ret.setlist(key, value)

    return ret