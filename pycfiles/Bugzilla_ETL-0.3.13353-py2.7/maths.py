# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bzETL\util\maths.py
# Compiled at: 2013-12-18 14:05:11
import math
from . import struct
from .struct import Null, nvl
from .logs import Log
from .strings import find_first

class Math(object):

    @staticmethod
    def bayesian_add(a, b):
        if a >= 1 or b >= 1 or a <= 0 or b <= 0:
            Log.error('Only allowed values *between* zero and one')
        return a * b / (a * b + (1 - a) * (1 - b))

    @staticmethod
    def sign(v):
        if v < 0:
            return -1
        if v > 0:
            return +1
        return 0

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except Exception:
            return False

    @staticmethod
    def is_integer(s):
        try:
            if float(s) == round(float(s), 0):
                return True
            else:
                return False

        except Exception:
            return False

    @staticmethod
    def round_sci(value, decimal=None, digits=None):
        if digits != None:
            m = pow(10, math.floor(math.log10(digits)))
            return round(value / m, digits) * m
        else:
            return round(value, decimal)

    @staticmethod
    def floor(value, mod=None):
        """
        x == floor(x, a) + mod(x, a)  FOR ALL a
        """
        mod = nvl(mod, 1)
        v = int(math.floor(value))
        return v - v % mod

    @staticmethod
    def approx_str(value):
        v = unicode(value)
        d = v.find('.')
        if d == -1:
            return value
        i = find_first(v, ['9999', '0000'], d)
        if i == -1:
            return value
        return Math.round_sci(value, decimal=i - d - 1)

    @staticmethod
    def min(values):
        output = Null
        for v in values:
            if v == None:
                continue
            if math.isnan(v):
                continue
            if output == None:
                output = v
                continue
            output = min(output, v)

        return output

    @staticmethod
    def max(values):
        output = Null
        for v in values:
            if v == None:
                continue
            if math.isnan(v):
                continue
            if output == None:
                output = v
                continue
            output = max(output, v)

        return output

    @staticmethod
    def ceiling(value):
        return math.ceil(value)