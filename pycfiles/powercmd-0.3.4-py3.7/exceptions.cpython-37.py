# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/powercmd/exceptions.py
# Compiled at: 2019-01-13 18:05:41
# Size of source mod 2**32: 159 bytes
"""
Exception types used by powercmd module.
"""

class InvalidInput(ValueError):
    __doc__ = 'An error raised if the input cannot be parsed as a valid command.'