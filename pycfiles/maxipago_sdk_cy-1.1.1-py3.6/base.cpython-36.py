# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/maxipago/resources/base.py
# Compiled at: 2018-07-08 23:37:16
# Size of source mod 2**32: 267 bytes


class Resource(object):

    def __init__(self, data, requester, manager):
        self.data = data
        self.requester = requester
        self.manager = manager
        self.process()

    def process(self):
        raise NotImplementedError()