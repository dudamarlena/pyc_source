# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/easyshop/core/interfaces/utilities.py
# Compiled at: 2008-06-20 09:35:25
from zope.interface import Interface

class INumberConverter(Interface):
    """Provides several converter methods for numbers.
    """
    __module__ = __name__

    def floatToString(float):
        """Formats a float to "0,00"
        """
        pass

    def floatToTaxString(myfloat, unit):
        """Formats given float to a tax string like "19,0 %"
        """
        pass

    def formatString(string):
        """Formats a float like string to "0,00"
        """
        pass

    def stringToFloat(string):
        """Converts a string to a float
        """
        pass