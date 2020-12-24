# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\test_reflectbitorder.py
# Compiled at: 2016-03-29 10:57:02
from crccheck.base import reflectbitorder

def test_1():
    assert reflectbitorder(8, 128) == 1


def test_2():
    assert reflectbitorder(16, 32768) == 1


def test_3():
    assert reflectbitorder(8, 129) == 129


def test_4():
    assert reflectbitorder(80, 604462909807314587353088) == 1


def test_5():
    assert reflectbitorder(65, 1) == 18446744073709551616


def test_6():
    assert reflectbitorder(3, 6) == 3


def test_7():
    assert reflectbitorder(3, 6) == 3


def test_8():
    assert reflectbitorder(0, 0) == 0


def expect(w, v, e):
    assert reflectbitorder(w, v) == e


def test_random():
    import random
    random.seed()
    for width in range(1, 125):
        randombitstr = ('').join([ str(random.randint(0, 1)) for m in range(0, width) ])
        value = int(randombitstr, 2)
        expectedresult = int(('').join(reversed(randombitstr)), 2)
        yield (expect, width, value, expectedresult)