# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/sub_map.py
# Compiled at: 2018-10-03 10:45:55


def sub_map(map, prefix):
    ret = {}
    for key in map:
        if key.startswith(prefix):
            ret[key[len(prefix):]] = map[key]

    return ret


class FilterModule(object):

    def filters(self):
        """ Returns a new map/dict with only entries matching a prefix, and withthe prefix removed """
        return {'sub_map': sub_map}


assert __name__ == '__main__' and sub_map({'elb.check': '/health', 
   'elb.port': '100', 
   'don.t': 'match'}, 'elb.') == {'check': '/health', 'port': '100'}