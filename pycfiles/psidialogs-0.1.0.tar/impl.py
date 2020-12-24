# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/f0/paul/Projects/Tools/Psicons/psicons.core/psicons/core/impl.py
# Compiled at: 2011-08-01 12:48:18
__doc__ = '\nInternal implementation utilities and details.\n\nThis module contains various odds and ends to make development easier. None of\nthe code within should be relied upon as it is subject to change at a whim.\n'
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