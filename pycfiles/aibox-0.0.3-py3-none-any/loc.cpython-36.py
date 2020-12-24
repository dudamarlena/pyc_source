# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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