# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\numberdata\__init__.py
# Compiled at: 2018-11-12 07:45:13
# Size of source mod 2**32: 295 bytes
import math

def calculateSquareRoot(num):
    return math.sqrt(num)


def calculateSquare(num):
    square = num * num
    return square


def calculateCube(num):
    cube = num * num * num
    return cube


def calculatePower(num1, num2):
    return num1 ** num2