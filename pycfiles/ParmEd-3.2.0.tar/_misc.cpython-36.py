# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/fortranformat/_misc.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 1303 bytes
"""
Miscellaneous functions, classes etc
"""

class has_next_iterator(object):
    __doc__ = '\n    A wrapper class for iterators so that the .has_next() method is implemented\n\n    See - http://stackoverflow.com/questions/1966591/hasnext-in-python-iterators\n    '

    def __init__(self, it):
        self.it = iter(it)
        self._has_next = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._has_next:
            result = self._the_next
        else:
            result = next(self.it)
        self._has_next = None
        return result

    def next(self):
        if self._has_next:
            result = self._the_next
        else:
            result = next(self.it)
        self._has_next = None
        return result

    def has_next(self):
        if self._has_next is None:
            try:
                self._the_next = next(self.it)
            except StopIteration:
                self._has_next = False
            else:
                self._has_next = True
        return self._has_next


def expand_edit_descriptors(eds):
    expanded_eds = []
    for ed in eds:
        if hasattr(ed, 'repeat') and ed.repeat is not None:
            expanded_eds.extend(ed.repeat * [ed])
        else:
            expanded_eds.append(ed)

    return expanded_eds