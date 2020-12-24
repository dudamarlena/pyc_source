# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/tmp/Projects/ControllProxy/seed/mrpackage/api.py
# Compiled at: 2018-05-20 09:26:02
# Size of source mod 2**32: 366 bytes


class API:

    def __init__(self, from_id, op, msg, handle):
        self.op = op
        self.handle = handle
        self.from_id = from_id
        self.msg = msg
        self.res = 'Not handle '
        if self.op == self.__class__.__name__.lower():
            self.res = self.handle()

    def handle(self):
        raise NotImplementedError('must implemment ')