# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/typecheck/typeclasses.py
# Compiled at: 2006-05-27 18:37:16
from typecheck import Typeclass
_numbers = [
 int, float, complex, long, bool]
try:
    from decimal import Decimal
    _numbers.append(Decimal)
    del Decimal
except ImportError:
    pass

Number = Typeclass(*_numbers)
del _numbers
String = Typeclass(str, unicode)
ImSequence = Typeclass(tuple, xrange, String)
MSequence = Typeclass(list)
Mapping = Typeclass(dict)