# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/solutions/forams/genom.py
# Compiled at: 2015-12-21 16:57:02


class Genom(object):

    def __init__(self, chambers_limit):
        super(Genom, self).__init__()
        self.chambers_limit = chambers_limit


class GenomFactory(object):

    def __init__(self, chambers_limit):
        super(GenomFactory, self).__init__()
        self.life_length = chambers_limit

    def generate(self):
        return Genom(self.life_length)