# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/solutions/evolution/genotype.py
# Compiled at: 2015-12-21 17:12:57


class PointGenotype(object):

    def __init__(self, x, y):
        super(PointGenotype, self).__init__()
        self.x = x
        self.y = y
        self.fitness = None
        return

    def __str__(self):
        return '(%s, %s), f:%s' % (self.x, self.y, self.fitness)

    def __repr__(self):
        return self.__str__()


class FloatGenotype(object):

    def __init__(self, genes):
        super(FloatGenotype, self).__init__()
        self.fitness = None
        self.genes = genes
        return

    def __str__(self):
        return '%s, f:%s' % (self.genes, self.fitness)

    def __repr__(self):
        return self.__str__()