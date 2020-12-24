# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/joekavalieri/git/conversionman/conversionman/lib/python2.7/site-packages/redisengine/core/common.py
# Compiled at: 2016-03-29 10:39:10
from redisengine.exceptions import NotRegistered
__all__ = ('ALLOW_INHERITANCE', 'get_tree', '_tree_registry')
ALLOW_INHERITANCE = False
_tree_registry = {}

def get_tree(name):
    doc = _tree_registry.get(name, None)
    if not doc:
        single_end = name.split('.')[(-1)]
        compound_end = '.%s' % single_end
        possible_match = [ k for k in _tree_registry.keys() if k.endswith(compound_end) or k == single_end
                         ]
        if len(possible_match) == 1:
            doc = _tree_registry.get(possible_match.pop(), None)
    if not doc:
        raise NotRegistered(('\n            `%s` has not been registered in the tree registry.\n            Importing the tree class automatically registers it, has it\n            been imported?\n        ').strip() % name)
    return doc