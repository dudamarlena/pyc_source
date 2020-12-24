# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: numphy/hep.py
# Compiled at: 2018-04-30 09:40:59
"""
High-energy physics objects.
"""
__all__ = [
 'LorentVector']
from numphy.core import Wrapper

class LorentVector(Wrapper):

    def __init__(self, *args, **kwargs):
        super(LorentVector, self).__init__(*args, **kwargs)