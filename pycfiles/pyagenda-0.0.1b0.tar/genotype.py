# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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