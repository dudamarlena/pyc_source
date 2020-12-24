# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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