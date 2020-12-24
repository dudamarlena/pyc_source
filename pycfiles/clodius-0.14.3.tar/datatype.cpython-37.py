# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/datatype.py
# Compiled at: 2019-12-10 06:35:02
# Size of source mod 2**32: 2194 bytes
import copy, types
from clocwalk.libs.core.exception import DataException

class AttribDict(dict):
    """AttribDict"""

    def __init__(self, indict=None, attribute=None):
        if indict is None:
            indict = {}
        self.attribute = attribute
        dict.__init__(self, indict)
        self._AttribDict__initialised = True

    def __getattr__(self, item):
        """
        Maps values to attributes
        Only called if there *is NOT* an attribute with this name
        """
        try:
            return self.__getitem__(item)
        except KeyError:
            raise DataException("unable to access item '%s'" % item)

    def __setattr__(self, item, value):
        """
        Maps attributes to values
        Only if we are initialised
        """
        if '_AttribDict__initialised' not in self.__dict__:
            return dict.__setattr__(self, item, value)
        elif item in self.__dict__:
            dict.__setattr__(self, item, value)
        else:
            self.__setitem__(item, value)

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, dict):
        self.__dict__ = dict

    def __deepcopy__(self, memo):
        retVal = self.__class__()
        memo[id(self)] = retVal
        for attr in dir(self):
            if not attr.startswith('_'):
                value = getattr(self, attr)
                isinstance(value, (types.BuiltinFunctionType, types.FunctionType, types.MethodType)) or setattr(retVal, attr, copy.deepcopy(value, memo))

        for key, value in self.items():
            retVal.__setitem__(key, copy.deepcopy(value, memo))

        return retVal