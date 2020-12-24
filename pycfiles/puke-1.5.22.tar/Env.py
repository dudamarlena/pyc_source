# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: puke/Env.py
# Compiled at: 2011-12-05 13:52:37
import os

class Env:

    @staticmethod
    def get(name, default):
        v = os.environ.get(name)
        if not v:
            return default
        return v