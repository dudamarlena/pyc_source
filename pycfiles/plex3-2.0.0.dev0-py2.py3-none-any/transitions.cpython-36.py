# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\geoffrey\workspace\python-plex\build\lib\plex\transitions.py
# Compiled at: 2018-02-04 13:40:13
# Size of source mod 2**32: 7414 bytes
"""
Plex - Transition Maps

This version represents state sets direcly as dicts
for speed.
"""
from copy import copy
import string

class TransitionMap:
    __doc__ = '\n    A TransitionMap maps an input event to a set of states.\n    An input event is one of: a range of character codes,\n    the empty string (representing an epsilon move), or one\n    of the special symbols BOL, EOL, EOF.\n\n    For characters, this implementation compactly represents\n    the map by means of a list:\n\n        [code_0, states_0, code_1, states_1, code_2, states_2,\n        ..., code_n-1, states_n-1, code_n]\n\n    where |code_i| is a character code, and |states_i| is a\n    set of states corresponding to characters with codes |c|\n    in the range |code_i| <= |c| <= |code_i+1|.\n\n    The following invariants hold:\n        n >= 1\n        code_0 == -float("inf")\n        code_n == float("inf")\n        code_i < code_i+1 for i in 0..n-1\n        states_0 == states_n-1\n\n    Mappings for the special events \'\', BOL, EOL, EOF are\n    kept separately in a dictionary.\n    '
    map = None
    special = None

    def __init__(self, map=None, special=None):
        if not map:
            map = [
             -float('inf'), {}, float('inf')]
        if not special:
            special = {}
        self.map = map
        self.special = special

    def add(self, event, new_state, tuple_type=tuple):
        """
        Add transition to |new_state| on |event|.
        """
        if isinstance(event, tuple_type):
            code0, code1 = event
            i = self.split(code0)
            j = self.split(code1)
            map = self.map
            while i < j:
                map[(i + 1)][new_state] = 1
                i = i + 2

        else:
            self.get_special(event)[new_state] = 1

    def add_set(self, event, new_set, tuple_type=tuple):
        """
        Add transitions to the states in |new_set| on |event|.
        """
        if isinstance(event, tuple_type):
            code0, code1 = event
            i = self.split(code0)
            j = self.split(code1)
            map = self.map
            while i < j:
                map[(i + 1)].update(new_set)
                i = i + 2

        else:
            self.get_special(event).update(new_set)

    def get_epsilon(self):
        """
        Return the mapping for epsilon, or None.
        """
        return self.special.get('')

    def items(self, len=len):
        """
        Return the mapping as a list of ((code1, code2), state_set) and
        (special_event, state_set) pairs.
        """
        result = []
        map = self.map
        else_set = map[1]
        i = 0
        n = len(map) - 1
        code0 = map[0]
        while i < n:
            set = map[(i + 1)]
            code1 = map[(i + 2)]
            if set or else_set:
                result.append(((code0, code1), set))
            code0 = code1
            i = i + 2

        for event, set in list(self.special.items()):
            if set:
                result.append((event, set))

        return result

    def split(self, code, len=len, maxint=float('inf')):
        """
        Search the list for the position of the split point for |code|,
        inserting a new split point if necessary. Returns index |i| such
        that |code| == |map[i]|.
        """
        map = self.map
        hi = len(map) - 1
        if code == maxint:
            return hi
        else:
            lo = 0
            while hi - lo >= 4:
                mid = int((lo + hi) / 2) & -2
                if code < map[mid]:
                    hi = mid
                else:
                    lo = mid

            if map[lo] == code:
                return lo
            map[hi:hi] = [code, map[(hi - 1)].copy()]
            return hi

    def get_special(self, event):
        """
        Get state set for special event, adding a new entry if necessary.
        """
        special = self.special
        set = special.get(event, None)
        if not set:
            set = {}
            special[event] = set
        return set

    def __str__(self):
        map_strs = []
        map = self.map
        n = len(map)
        i = 0
        while i < n:
            code = map[i]
            if code == -float('inf'):
                code_str = '-inf'
            else:
                if code == float('inf'):
                    code_str = 'inf'
                else:
                    code_str = str(code)
            map_strs.append(code_str)
            i = i + 1
            if i < n:
                map_strs.append(state_set_str(map[i]))
            i = i + 1

        special_strs = {}
        for event, set in list(self.special.items()):
            special_strs[event] = state_set_str(set)

        return '[%s]+%s' % (
         string.join(map_strs, ','),
         special_strs)

    def check(self):
        """Check data structure integrity."""
        if not self.map[(-3)] < self.map[(-1)]:
            print(self)
            if not 0:
                raise AssertionError

    def dump(self, file):
        map = self.map
        i = 0
        n = len(map) - 1
        while i < n:
            self.dump_range(map[i], map[(i + 2)], map[(i + 1)], file)
            i = i + 2

        for event, set in list(self.special.items()):
            if set:
                if not event:
                    event = 'empty'
                self.dump_trans(event, set, file)

    def dump_range(self, code0, code1, set, file):
        if set:
            if code0 == -float('inf'):
                if code1 == float('inf'):
                    k = 'any'
                else:
                    k = '< %s' % self.dump_char(code1)
            else:
                if code1 == float('inf'):
                    k = '> %s' % self.dump_char(code0 - 1)
                else:
                    if code0 == code1 - 1:
                        k = self.dump_char(code0)
                    else:
                        k = '%s..%s' % (self.dump_char(code0),
                         self.dump_char(code1 - 1))
            self.dump_trans(k, set, file)

    def dump_char(self, code):
        if 0 <= code <= 255:
            return repr(chr(code))
        else:
            return 'chr(%d)' % code

    def dump_trans(self, key, set, file):
        file.write('      %s --> %s\n' % (key, self.dump_set(set)))

    def dump_set(self, set):
        return state_set_str(set)


def state_set_str(set):
    state_list = list(set.keys())
    str_list = []
    for state in state_list:
        str_list.append('S%d' % state.number)

    return '[%s]' % string.join(str_list, ',')