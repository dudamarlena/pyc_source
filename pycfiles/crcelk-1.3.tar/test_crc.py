# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_crc.py
# Compiled at: 2016-03-31 03:49:51
__doc__ = ' Unit tests for checksum module.\n\n  License::\n  \n    Copyright (C) 2015-2016 by Martin Scharrer <martin@scharrer-online.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import sys
from nose.plugins.skip import SkipTest
from crccheck.base import CrccheckError
from crccheck.crc import ALLCRCCLASSES, Crc32

def test_allcrc():
    """Test if expected 'check' result is calulated with standard test vector."""
    for crcclass in ALLCRCCLASSES:
        yield (
         lambda x: x.selftest(), crcclass)


def test_allcrcfail():
    """Test if 'check' result is not reached with different input."""

    def fail(cls):
        try:
            cls.selftest(bytearray('wrongtestinput'), cls._check_result)
        except CrccheckError:
            pass
        else:
            raise Exception('Selftest passed with incorrect input!')

    for crcclass in ALLCRCCLASSES:
        yield (
         fail, crcclass)


def test_generator():
    Crc32.calc(n for n in range(0, 255))


def test_list1():
    Crc32.calc([ n for n in range(0, 255) ])


def test_list2():
    Crc32.calc([ n for n in range(0, 255) ], 123)


def test_bytearray():
    Crc32.calc(bytearray.fromhex('12345678909876543210'))


def test_bytes():
    if sys.version_info < (3, 3, 0):
        raise SkipTest
    Crc32.calc(bytes.fromhex('12345678909876543210'))


def test_string1():
    if sys.version_info < (3, 3, 0):
        raise SkipTest
    Crc32.calc('Teststring')


def test_string2():
    if sys.version_info < (3, 3, 0):
        raise SkipTest
    Crc32.calc(('Teststring').encode())