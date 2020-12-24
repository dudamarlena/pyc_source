# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/r/repo/aibolit/metrics/loc/loc.py
# Compiled at: 2020-04-10 11:54:00
# Size of source mod 2**32: 1322 bytes


class Loc:

    def __init__(self, path):
        self.path = path

    def value(self):
        with open(self.path) as (f):
            for i, l in enumerate(f):
                pass

            return i + 1