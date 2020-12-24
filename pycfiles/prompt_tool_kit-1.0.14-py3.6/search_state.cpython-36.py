# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/search_state.py
# Compiled at: 2019-08-15 23:31:02
# Size of source mod 2**32: 1099 bytes
from .enums import IncrementalSearchDirection
from .filters import to_simple_filter
__all__ = ('SearchState', )

class SearchState(object):
    __doc__ = "\n    A search 'query'.\n    "
    __slots__ = ('text', 'direction', 'ignore_case')

    def __init__(self, text='', direction=IncrementalSearchDirection.FORWARD, ignore_case=False):
        ignore_case = to_simple_filter(ignore_case)
        self.text = text
        self.direction = direction
        self.ignore_case = ignore_case

    def __repr__(self):
        return '%s(%r, direction=%r, ignore_case=%r)' % (
         self.__class__.__name__, self.text, self.direction, self.ignore_case)

    def __invert__(self):
        """
        Create a new SearchState where backwards becomes forwards and the other
        way around.
        """
        if self.direction == IncrementalSearchDirection.BACKWARD:
            direction = IncrementalSearchDirection.FORWARD
        else:
            direction = IncrementalSearchDirection.BACKWARD
        return SearchState(text=(self.text), direction=direction, ignore_case=(self.ignore_case))