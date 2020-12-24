# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mapy\model\loads\subcases.py
# Compiled at: 2017-04-12 19:32:03
# Size of source mod 2**32: 318 bytes


class Subcase(object):

    def __init__(self, subid, loadid, consid):
        self.id = subid
        self.loadid = loadid
        self.consid = consid

    def rebuild(self):
        for load in self.model.loaddict.values():
            if load.id == self.loadid:
                load.set_subcase(self)