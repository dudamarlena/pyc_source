# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pgpu/compatibility.py
# Compiled at: 2016-03-15 01:17:49
"""
Module to make it easier to write code compatible with both 2.x and 3.x.

AUTHORS:
v0.2.0+             --> pydsigner
v1.0.1+             --> pydsigner
"""
__all__ = [
 'input', 'range', 'chr', 'str', 'Print']
try:
    input = raw_input
    range = xrange
    chr = unichr
    str = unicode
except NameError:
    input = input
    range = range
    chr = chr
    str = str

Print = __builtins__.get('print')