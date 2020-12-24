# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/handlers/input.py
# Compiled at: 2020-01-15 14:18:24
# Size of source mod 2**32: 280 bytes
try:
    input = raw_input
except NameError:
    pass

raw_input = input
try:
    range = xrange
except NameError:
    pass

xrange = range