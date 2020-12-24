# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/Boolean.py
# Compiled at: 2008-05-10 01:55:08
import types
__all__ = [
 'boolean']

class boolean:
    """A flag type, such as on/off, true/false, etc.  The following
     values are considered true (case is always ignored):
       - t (T)
       - true (True, TRUE, TrUe)
       - yes (Yes, YES, YeS)
       - on (ON, On, oN)
       - any integer other than 0
  """

    def __init__(self, *args, **kargs):
        """Creates a new boolean object"""
        if len(args) >= 1 and isinstance(args[0], types.StringTypes) and args[0].lower() in ('t',
                                                                                             'true',
                                                                                             'yes',
                                                                                             'on'):
            self._value = True
        elif len(args) >= 1 and isinstance(args[0], types.BooleanType):
            self._value = args[0]
        elif len(args) >= 1 and isinstance(args[0], (types.IntType, types.LongType, types.FloatType)):
            self._value = args[0] != 0
        elif len(args) >= 1 and isinstance(args[0], boolean):
            self._value = args[0]._value
        else:
            self._value = False

    def __eq__(self, other):
        """Returns whether this boolean value matches the other one"""
        if isinstance(other, boolean):
            return self._value == other._value
        else:
            if isinstance(other, types.BooleanType):
                return self._value == other
            return self._value == boolean(other)._value

    def __repr__(self):
        return self._value and 'True' or 'False'