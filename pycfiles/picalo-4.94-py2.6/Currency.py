# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/Currency.py
# Compiled at: 2009-12-17 15:49:10
import types, re
from Number import number
__all__ = [
 'currency']
RE_IMPORT = re.compile('^.*?(\\d+\\.\\d+|\\d+).*?$')

class currency(number):
    """A simple extension to number to deliniate a currency type.  In future versions,
     we'll make this class support the currencies from around the world."""

    def __new__(self, value=0.0):
        if value and isinstance(value, types.StringTypes):
            match = RE_IMPORT.search(value)
            if match:
                value = match.group(1)
        return number(value)