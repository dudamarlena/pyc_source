# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/nestedelement.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import re

def nested_element(object, path):
    obj = object
    for part in re.split('\\.|/', path):
        if part == '':
            continue
        if part not in obj:
            raise KeyError('Missing key %s in %s' % (part, obj))
        obj = obj[part]

    return obj


class FilterModule(object):
    """Returns an nested element from an object tree by path (seperated by / or .)"""

    def filters(self):
        return {'nested_element': nested_element}