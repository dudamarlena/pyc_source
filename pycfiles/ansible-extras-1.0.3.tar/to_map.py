# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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