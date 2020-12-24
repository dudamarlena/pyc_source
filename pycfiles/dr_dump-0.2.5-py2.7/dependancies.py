# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drdump/dependancies.py
# Compiled at: 2015-02-04 12:28:23
"""
Dependancies manager
"""
from collections import OrderedDict

class DependanciesManager(OrderedDict):
    """
    Object to store a catalog of available dump dependancies with some methods
    to get a clean dump map with their required dependancies.
    """
    deps_index = {}

    def __init__(self, *args, **kwargs):
        self.silent_key_error = kwargs.pop('silent_key_error', False)
        super(DependanciesManager, self).__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        """
        Perform string to list translation and dependancies indexing when
        setting an item
        """
        if isinstance(value['models'], basestring):
            value['models'] = value['models'].split()
        if 'dependancies' in value:
            if isinstance(value['dependancies'], basestring):
                value['dependancies'] = value['dependancies'].split()
            for k in value['dependancies']:
                if k not in self.deps_index:
                    self.deps_index[k] = set([])
                self.deps_index[k].add(key)

        OrderedDict.__setitem__(self, key, value)

    def get_dump_names(self, names, dumps=None):
        """
        Find and return all dump names required (by dependancies) for a given
        dump names list

        Beware, the returned name list does not respect order, you should only
        use it when walking throught the "original" dict builded by OrderedDict
        """
        if dumps is None:
            dumps = set([])
        for item in names:
            if item not in self:
                if not self.silent_key_error:
                    raise KeyError(("Dump name '{0}' is unknowed").format(item))
                else:
                    continue
            dumps.add(item)
            deps = self.__getitem__(item).get('dependancies', [])
            dumps.update(deps)

        if names == dumps:
            return dumps
        else:
            return self.get_dump_names(dumps.copy(), dumps)

    def get_dump_order(self, names):
        """
        Return ordered dump names required for a given dump names list
        """
        finded_names = self.get_dump_names(names)
        return [ item for item in self if item in finded_names ]


if __name__ == '__main__':
    import json
    AVAILABLE_DUMPS = json.load(open('maps/djangocms-3.json', 'r'))
    dump_manager = DependanciesManager(AVAILABLE_DUMPS, silent_key_error=True)
    print dump_manager.get_dump_order(['django-cms', 'porticus'])
    print