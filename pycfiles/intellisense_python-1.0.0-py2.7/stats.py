# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/intellisense/stats.py
# Compiled at: 2013-10-21 14:15:37


class Statistics(object):

    def __init__(self):
        self.submitted = 0
        self.identifies = 0
        self.describes = 0
        self.measures = 0
        self.tracks = 0
        self.aliases = 0
        self.successful = 0
        self.failed = 0
        self.flushes = 0