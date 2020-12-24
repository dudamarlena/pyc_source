# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modipy/namespace.py
# Compiled at: 2009-08-25 18:19:45
"""
The namespace module contains namespace classes that are used for
variable substitution within ModiPy.

Namespaces exist in a hierarchy, and a particular change will
use a namespace at some point in the hierarchy to find the
value to use for a keyword substitution. If the namespace doesn't
have an entry for that key, it will cascade upwards to its parent
namespace(s) all the way up to a global namespace to look for that
keyword, and will use the first one it finds.

In this way, you can define variables for use in your changes,
either globally (including some default keywords in the global
namespace) or specifically within just specific changes, or
for groups of changes.
"""
import logging
log = logging.getLogger('modipy')

class Namespace:
    """
    A cascading namespace object that can refer to items in
    parent namespaces to resolve names if they do not exist
    in the current namespace.
    """

    def __init__(self, name='', namespace=None, parent=None):
        self.name = name
        self.parent = parent
        if namespace is None:
            self.namespace = {}
        else:
            self.namespace = namespace.copy()
        return

    def __getitem__(self, key):
        """
        Implement dictionary interface
        """
        try:
            return self.namespace[key]
        except KeyError:
            if self.parent is not None:
                return self.parent[key]
            else:
                raise

        return

    def __setitem__(self, key, value):
        self.namespace[key] = value

    def keys(self):
        keys = self.namespace.keys()
        if self.parent is not None:
            pkeys = self.parent.keys()
            for pkey in pkeys:
                if pkey not in keys:
                    keys.append(pkey)

        return keys

    def has_key(self, key):
        if self.namespace.has_key(key):
            return True
        elif self.parent is not None:
            return self.parent.has_key(key)
        else:
            return False
        return

    def update(self, dict):
        if dict is not None:
            for key in dict:
                self.namespace[key] = dict[key]

        return

    def __iter__(self):
        if self.parent is not None:
            log.debug('started parent iterator')
            return self.parent.__iter__()
        self.namespace.__iter__()
        return self

    def next(self):
        if self.parent is not None:
            try:
                return self.parent.next()
            except StopIteration:
                return self.namespace.next()

        else:
            try:
                return self.namespace.next()
            except AttributeError:
                raise StopIteration

        return

    def items(self):
        items = []
        if self.parent is not None:
            items.extend(self.parent.items())
        items.extend(self.namespace.items())
        return items

    def copy(self):
        return self.namespace.copy()

    def __repr__(self):
        return '<Namespace [%s]: %s>' % (self.name, self.items())


def create_namespace(node):
    """
    Create a namespace from an element node
    """
    ns = Namespace(node.tag)
    for entry in node.findall('entry'):
        item_name = entry.attrib['name']
        item_value = entry.text
        ns[item_name] = item_value

    return ns