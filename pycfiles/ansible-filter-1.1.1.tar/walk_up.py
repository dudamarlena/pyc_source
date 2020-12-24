# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/walk_up.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors
import re, sys

def nested_element(object, path):
    obj = object
    for part in re.split('\\.|/', path):
        if part == '':
            continue
        if part not in obj:
            raise KeyError('Missing key %s in %s' % (part, obj))
        obj = obj[part]

    return obj


def walk_up(tree, path, ignore=[]):
    results = {}
    parts = re.split('\\.|/', path)
    for i in range(len(parts), 0, -1):
        subpath = ('/').join(parts[0:i])
        object = nested_element(tree, subpath)
        for key in object:
            if key not in results and key not in ignore:
                results[key] = object[key]

    return results


class FilterModule(object):
    """ Walks up an object tree from the lowest level collecting all attributes not available at lower levels"""

    def filters(self):
        return {'walk_up': walk_up}