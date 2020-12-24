# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/parsec/parsec.py
# Compiled at: 2015-12-14 04:43:06
# Size of source mod 2**32: 618 bytes


class Parsec(object):

    def __init__(self, parsec):
        self.parsec = parsec

    def __call__(self, st):
        return self.parsec(st)

    def bind(self, continuation):

        def bind(st):
            binder = continuation(self.parsec(st))
            return binder(st)

        return Parsec(bind)

    def then(self, p):

        def then(st):
            self.parsec(st)
            return p(st)

        return Parsec(then)

    def over(self, p):

        def over(st):
            re = self.parsec(st)
            p(st)
            return re

        return Parsec(over)