# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/boduch/type/type.py
# Compiled at: 2009-08-14 17:29:30
"""This module defines the base type class.  This class defines some
operator-overloading functionality."""
import types, uuid
from zope.interface import implements
from boduch.interface import IType

class Type(object):
    """The base type class that defines various comparison operators."""
    implements(IType)

    def __init__(self, *args, **kw):
        """Constructor.  Initialize the keyword data.  The data attribute
        is used when computing the length of type instances."""
        self.data = kw
        self.uuid = uuid.uuid1()

    def __len__(self):
        """Compute the length of this instance.  We iterate through the 
        values in the data attribute.  We then return the total of all
        integers found in the data attribute."""
        length = 0
        for i in self.data.values():
            try:
                if type(i) is types.IntType:
                    length += i
                    continue
                length += len(i)
            except (TypeError, AttributeError):
                continue

        return length

    def __eq__(self, other):
        """Compare the equality of this instance to another.  We return true
        if the length of the two instances match"""
        return len(self) == len(other)

    def __lt__(self, other):
        """Return true if this instance is less than the other instance."""
        return len(self) < len(other)

    def __gt__(self, other):
        """Return true if this instance is greater than the other instance."""
        return len(self) > len(other)

    def __cmp__(self, other):
        """Return -1 if both instances have a priority attribute and this
        one is less than the other; 1 if both instances have a priority
        attribute and this one is greater than the other; 0 in all other
        cases."""
        if hasattr(self, 'priority') and hasattr(other, 'priority'):
            return cmp(self.priority, other.priority)
        return 0


__all__ = [
 'Type']