# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_vendor/resolvelib/reporters.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 1094 bytes


class BaseReporter(object):
    __doc__ = 'Delegate class to provider progress reporting for the resolver.\n    '

    def starting(self):
        """Called before the resolution actually starts.
        """
        pass

    def starting_round(self, index):
        """Called before each round of resolution starts.

        The index is zero-based.
        """
        pass

    def ending_round(self, index, state):
        """Called before each round of resolution ends.

        This is NOT called if the resolution ends at this round. Use `ending`
        if you want to report finalization. The index is zero-based.
        """
        pass

    def ending(self, state):
        """Called before the resolution ends successfully.
        """
        pass

    def adding_requirement(self, requirement):
        """Called when the resolver adds a new requirement into the resolve criteria.
        """
        pass

    def backtracking(self, candidate):
        """Called when the resolver rejects a candidate during backtracking.
        """
        pass

    def pinning(self, candidate):
        """Called when adding a candidate to the potential solution.
        """
        pass