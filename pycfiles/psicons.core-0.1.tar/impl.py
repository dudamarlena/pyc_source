# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/f0/paul/Projects/Tools/Psicons/psicons.core/psicons/core/impl.py
# Compiled at: 2011-08-01 12:48:18
"""
Internal implementation utilities and details.

This module contains various odds and ends to make development easier. None of
the code within should be relied upon as it is subject to change at a whim.
"""
__docformat__ = 'restructuredtext en'
import types
__all__ = [
 'make_list']

def make_list(x):
    """
        If this isn't a list, make it one.
        
        :Parameters:
                x : list, tuple, other
                        a sequence, or a single element to be placed in a sequence
                        
        :Returns:
                Either the original a parameter if a sequence, or the parameter placed in
                a list.
        
        Syntactic sugar for allowing method calls to be single elements or lists of
        elements.
        
        For example::
        
                >>> make_list (1)
                [1]
                >>> make_list ('1')
                ['1']
                >>> make_list ([1, 2])
                [1, 2]
                >>> make_list ((1, 2))
                (1, 2)
                
        """
    if type(x) not in (types.ListType, types.TupleType):
        x = [
         x]
    return x


if __name__ == '__main__':
    import doctest
    doctest.testmod()