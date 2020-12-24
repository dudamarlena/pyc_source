# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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