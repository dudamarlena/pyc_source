# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hexdutils/hexops.py
# Compiled at: 2019-08-02 02:17:36
# Size of source mod 2**32: 2907 bytes
from os import path
import sys
sys.path.insert(0, path.abspath(path.join(path.dirname(__file__), '.')))
from intohex import _intohex as intohex
from hextoint import _hextoint as hextoint

def _hex_add(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if type(first) is not str or type(second) is not str:
        raise TypeError('Values type must be str (are %s). Use intohex(int value)' % [type(first), type(second)])
    result = hextoint(first) + hextoint(second)
    if hex_output:
        return intohex(result, hex_output_prefix, hex_output_upper)
    return result


def _hex_sub(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if type(first) is not str or type(second) is not str:
        raise TypeError('Values type must be str (are %s). Use intohex(int value)' % [type(first), type(second)])
    result = hextoint(first) - hextoint(second)
    if hex_output:
        return intohex(result, hex_output_prefix, hex_output_upper)
    return result


def _hex_mul(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if type(first) is not str or type(second) is not str:
        raise TypeError('Values type must be str (are %s). Use intohex(int value)' % [type(first), type(second)])
    result = hextoint(first) * hextoint(second)
    if hex_output:
        return intohex(result, hex_output_prefix, hex_output_upper)
    return result


def _hex_floordiv(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if type(first) is not str or type(second) is not str:
        raise TypeError('Values type must be str (are %s). Use intohex(int value)' % [type(first), type(second)])
    result = hextoint(first) // hextoint(second)
    if hex_output:
        return intohex(result, hex_output_prefix, hex_output_upper)
    return result


_hex_truediv = _hex_floordiv

def _hex_mod(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if type(first) is not str or type(second) is not str:
        raise TypeError('Values type must be str (are %s). Use intohex(int value)' % [type(first), type(second)])
    result = hextoint(first) % hextoint(second)
    if hex_output:
        return intohex(result, hex_output_prefix, hex_output_upper)
    return result


def _hex_power(first, second, hex_output, hex_output_prefix=False, hex_output_upper=False):
    if type(first) is not str or type(second) is not str:
        raise TypeError('Values type must be str (are %s). Use intohex(int value)' % [type(first), type(second)])
    result = hextoint(first) ** hextoint(second)
    if hex_output:
        return intohex(result, hex_output_prefix, hex_output_upper)
    return result