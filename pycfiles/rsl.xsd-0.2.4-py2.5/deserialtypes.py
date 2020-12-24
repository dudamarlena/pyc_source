# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/rsl/xsd/deserialtypes.py
# Compiled at: 2009-01-12 07:29:42
"""
this module defines data types to be used by xml-deserialisers. those data 
types are derived from the standard python builtin data types, and are able to
store xml-attributes as object-attributes.
"""

class ValueType(object):
    """
    base type for deserialtypes.
    """

    def __eq__(self, other):
        """
        override equality test. this method allows to compare the bultin
        data types with the derived ones as usual. it consideres an 
        eventually available __dict__ attribute in its comparison.
        """
        if other is None:
            return False
        supcls = super(ValueType, self)
        if hasattr(supcls, '__eq__'):
            ret = supcls.__eq__(other)
        else:
            ret = supcls.__cmp__(other) == 0
        if ret:
            if hasattr(other, '__dict__'):
                ret = self.__dict__ == other.__dict__
            else:
                ret = not bool(self.__dict__)
        return ret

    def __ne__(self, other):
        """
        override non equality test. this method allows to compare the 
        bultin data types with the derived ones as usual. it consideres an 
        eventually available __dict__ attribute in its comparison.
        """
        if other is None:
            return True
        supcls = super(ValueType, self)
        if hasattr(supcls, '__ne__'):
            ret = supcls.__ne__(other)
        else:
            ret = supcls.__cmp__(other) != 0
        if not ret:
            if hasattr(other, '__dict__'):
                ret = self.__dict__ != other.__dict__
            else:
                ret = bool(self.__dict__)
        return ret

    def __repr__(self):
        """
        show an eventually available __dict__ attribute in repr output.
        """
        if self.__dict__:
            return super(ValueType, self).__repr__() + ',' + repr(self.__dict__)
        else:
            return super(ValueType, self).__repr__()


class Dict(ValueType, dict):
    """
    the builtin compatible dict type with additional meta infos (xml-attributes).
    """
    pass


class List(ValueType, list):
    """
    the builtin compatible list type with additional meta infos (xml-attributes).
    """
    pass


class String(ValueType, str):
    """
    the builtin compatible string type with additional meta infos (xml-attributes).
    """
    pass


class Unicode(ValueType, unicode):
    """
    the builtin compatible unicde type with additional meta infos (xml-attributes).
    """
    pass