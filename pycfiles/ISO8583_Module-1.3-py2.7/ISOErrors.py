# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ISO8583/ISOErrors.py
# Compiled at: 2009-01-21 16:07:28
"""

(C) Copyright 2009 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

class ValueToLarge(Exception):
    """Exeption that indicate that a value that want to set inside the bit is large than the "ISO" limit.
                This can happen when you have a different specification of mine.
                If this is the case, you should use "ISO8583.redefineBit()" method and redefine the limit.
        """

    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class BitInexistent(Exception):
    """Exeption that indicate that a bit that you try to manage dosen't exist!
                Try to check your "setBit". Remember that ISO8583 1993 has only bits from 1 to 128!
        """

    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class InvalidValueType(Exception):
    """Exeption that indicate that a value that you try to insert is out of especification.
                For example: You try to insert a value "ABC" in a bit of type "N" (Number) , this is invalid!
                This can happen when you have a different specification of mine.
                If this is the case, you should use "ISO8583.redefineBit()" method and redefine the type.
        """

    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class InvalidBitType(Exception):
    """Exception that indicate that the type that you try to set is invalid.
                For example: You try to set type "X", that dosen't exist.
                Valid type are: B, N, A, AN, ANS, LL, LLL
        """

    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class InvalidIso8583(Exception):
    """Exception that indicate a invalid ASCII message, for example, without a piece... Error size etc.
        """

    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class InvalidMTI(Exception):
    """Exception that indicate a invalid MTI
        """

    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)


class BitNotSet(Exception):
    """Exception that indicate that you try to access a bit not present in the bitmap.
        """

    def __init__(self, value):
        self.str = value

    def __str__(self):
        return repr(self.str)