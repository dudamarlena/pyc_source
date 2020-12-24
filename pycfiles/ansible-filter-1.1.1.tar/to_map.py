# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/to_map.py
# Compiled at: 2018-10-03 10:45:55


def to_map(_map, key, value):
    ret = {}
    for row in _map:
        ret[row[key].lower()] = row[value]

    return ret


class FilterModule(object):

    def filters(self):
        return {'to_map': to_map}