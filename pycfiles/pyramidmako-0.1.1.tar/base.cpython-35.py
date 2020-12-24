# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/logservice/base.py
# Compiled at: 2016-08-13 23:10:45
# Size of source mod 2**32: 91 bytes


class Base(object):

    def __init__(self, dbsession):
        self.dbsession = dbsession