# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\grammar\list.py
# Compiled at: 2009-04-03 11:21:16
"""
    This file implements List and DictList classes which behave
    as built-in Python lists and dicts, but can be used within
    Dragonfly grammars.
"""

class ListBase(object):
    _valid_types = (
     str, unicode)

    def __init__(self, name):
        self._name = name
        self._grammar = None
        return

    valid_types = property(lambda self: self._valid_types, doc='The types of object at a Dragonfly list can contain.')
    name = property(lambda self: self._name, doc="Read-only access to a list's name.")

    def _get_grammar(self):
        return self._grammar

    def _set_grammar(self, grammar):
        if self._grammar is None:
            self._grammar = grammar
        else:
            raise TypeError('The grammar object a Dragonfly list is bound to cannot be changed after it has been set.')
        return

    grammar = property(_get_grammar, _set_grammar, doc="Set-once access to a list's grammar object.")

    def _update(self):
        invalid = [ i for i in self if not isinstance(i, self._valid_types) ]
        if invalid:
            raise TypeError('Dragonfly lists can only contain string objects; received: %r' % invalid)
        if self._grammar:
            self._grammar.update_list(self)

    def get_list_items(self):
        raise NotImplementedError('Call to virtual method list_items()')


class List(ListBase, list):
    """
        Wrapper for Python's built-in list that supports automatic
        Natlink notification of changes.
    """

    def __init__(self, name, *args, **kwargs):
        ListBase.__init__(self, name)
        list.__init__(self, *args, **kwargs)

    def get_list_items(self):
        return self

    def set(self, other):
        """Set the contents of this list to the contents of another."""
        self[:] = other
        self._update()

    def __add__(self, *args, **kwargs):
        result = list.__add__(self, *args, **kwargs)
        self._update()
        return result

    def __delitem__(self, *args, **kwargs):
        result = list.__delitem__(self, *args, **kwargs)
        self._update()
        return result

    def __delslice__(self, *args, **kwargs):
        result = list.__delslice__(self, *args, **kwargs)
        self._update()
        return result

    def __iadd__(self, *args, **kwargs):
        result = list.__iadd__(self, *args, **kwargs)
        self._update()
        return result

    def __imul__(self, *args, **kwargs):
        result = list.__imul__(self, *args, **kwargs)
        self._update()
        return result

    def __mul__(self, *args, **kwargs):
        result = list.__mul__(self, *args, **kwargs)
        self._update()
        return result

    def __reduce__(self, *args, **kwargs):
        result = list.__reduce__(self, *args, **kwargs)
        self._update()
        return result

    def __reduce_ex__(self, *args, **kwargs):
        result = list.__reduce_ex__(self, *args, **kwargs)
        self._update()
        return result

    def __rmul__(self, *args, **kwargs):
        result = list.__rmul__(self, *args, **kwargs)
        self._update()
        return result

    def __setitem__(self, *args, **kwargs):
        result = list.__setitem__(self, *args, **kwargs)
        self._update()
        return result

    def __setslice__(self, *args, **kwargs):
        result = list.__setslice__(self, *args, **kwargs)
        self._update()
        return result

    def append(self, *args, **kwargs):
        result = list.append(self, *args, **kwargs)
        self._update()
        return result

    def extend(self, *args, **kwargs):
        result = list.extend(self, *args, **kwargs)
        self._update()
        return result

    def insert(self, *args, **kwargs):
        result = list.insert(self, *args, **kwargs)
        self._update()
        return result

    def pop(self, *args, **kwargs):
        result = list.pop(self, *args, **kwargs)
        self._update()
        return result

    def remove(self, *args, **kwargs):
        result = list.remove(self, *args, **kwargs)
        self._update()
        return result

    def reverse(self, *args, **kwargs):
        result = list.reverse(self, *args, **kwargs)
        self._update()
        return result

    def sort(self, *args, **kwargs):
        result = list.sort(self, *args, **kwargs)
        self._update()
        return result


class DictList(ListBase, dict):
    """
        Wrapper for Python's built-in dict that supports automatic
        Natlink notification of changes.  The object's keys are used
        as the elements of the Natlink list, while use of the associated
        values is left to the user.
    """

    def __init__(self, name, *args, **kwargs):
        ListBase.__init__(self, name)
        dict.__init__(self, *args, **kwargs)

    def get_list_items(self):
        return self.keys()

    def set(self, other):
        """Set the contents of this dict to the contents of another."""
        self.clear()
        self.update(other)
        self._update()

    def __delitem__(self, *args, **kwargs):
        result = dict.__delitem__(self, *args, **kwargs)
        self._update()
        return result

    def __reduce__(self, *args, **kwargs):
        result = dict.__reduce__(self, *args, **kwargs)
        self._update()
        return result

    def __reduce_ex__(self, *args, **kwargs):
        result = dict.__reduce_ex__(self, *args, **kwargs)
        self._update()
        return result

    def __setitem__(self, *args, **kwargs):
        result = dict.__setitem__(self, *args, **kwargs)
        self._update()
        return result

    def clear(self, *args, **kwargs):
        result = dict.clear(self, *args, **kwargs)
        self._update()
        return result

    def fromkeys(self, *args, **kwargs):
        result = dict.fromkeys(self, *args, **kwargs)
        self._update()
        return result

    def pop(self, *args, **kwargs):
        result = dict.pop(self, *args, **kwargs)
        self._update()
        return result

    def popitem(self, *args, **kwargs):
        result = dict.popitem(self, *args, **kwargs)
        self._update()
        return result

    def setdefault(self, *args, **kwargs):
        result = dict.setdefault(self, *args, **kwargs)
        self._update()
        return result

    def update(self, *args, **kwargs):
        result = dict.update(self, *args, **kwargs)
        self._update()
        return result