# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/golem/db/conceptlist.py
# Compiled at: 2008-08-22 15:02:55


class conceptlist(list):
    __module__ = __name__

    def __init__(self, *args):
        list.__init__(self, list(args))

    def setpredicate(self, predicate):
        self.predicate = predicate

    def getpredicate(self):
        try:
            return self.predicate
        except AttributeError:
            return

        return