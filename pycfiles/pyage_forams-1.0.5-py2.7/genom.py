# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/genom.py
# Compiled at: 2014-05-20 16:36:48


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