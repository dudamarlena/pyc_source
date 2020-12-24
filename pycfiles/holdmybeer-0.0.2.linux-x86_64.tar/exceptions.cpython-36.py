# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tmiedema/.pyenv/versions/3.6.0/lib/python3.6/site-packages/holdmybeer/exceptions.py
# Compiled at: 2017-03-28 10:14:56
# Size of source mod 2**32: 310 bytes


class RunDry(Exception):
    __doc__ = 'Attempted to get more out of a bucket than it contains.'


class NegativeSubstance(Exception):
    __doc__ = 'Attempted to initialize or modify a bucket with negative values'


class IncompatibleContainer(Exception):
    __doc__ = 'Attempted to flow to an incompatable container'