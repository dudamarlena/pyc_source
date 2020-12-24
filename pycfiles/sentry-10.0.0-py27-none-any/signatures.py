# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/similarity/signatures.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import mmh3

class MinHashSignatureBuilder(object):

    def __init__(self, columns, rows):
        self.columns = columns
        self.rows = rows

    def __call__(self, features):
        return map(lambda column: min(map(lambda feature: mmh3.hash(feature, column) % self.rows, features)), range(self.columns))