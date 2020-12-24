# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/map_to_entries.py
# Compiled at: 2018-10-03 10:45:55
from ansible import errors

def map_to_entries(_map, key, value):
    _list = []
    for k in _map:
        _list.append({key: k, 
           value: _map[k]})

    return _list


class FilterModule(object):
    """ A filter to convert a map into a list of entries"""

    def filters(self):
        return {'map_to_entries': map_to_entries}


if __name__ == '__main__':
    print map_to_entries({'key1': 'value1', 
       'key2': 'value2'}, 'k', 'v')