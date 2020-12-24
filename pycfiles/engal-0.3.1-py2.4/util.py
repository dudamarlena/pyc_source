# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/engal/util.py
# Compiled at: 2006-09-18 06:17:43
import os, os.path, random

def sample(population, number):
    population = SQLObjectSequence(population)
    population_size = len(population)
    if number > population_size:
        number = population_size
    return random.sample(population, number)


def choice(population):
    population = SQLObjectSequence(population)
    try:
        return random.choice(population)
    except:
        return

    return


class SQLObjectSequence(object):
    __module__ = __name__
    cached_length = None

    def __init__(self, resultset):
        self.resultset = resultset

    def __len__(self):
        if not self.cached_length:
            self.cached_length = self.resultset.count()
        return self.cached_length

    def __getattr__(self, name):
        return getattr(self.resultset, name)

    def __iter__(self):
        return self.resultset.__iter__()

    def __getitem__(self, n):
        return self.resultset.__getitem__(n)


def getTagIconDirectory():
    import turbogears
    path = os.environ.get('ENGAL_PATH')
    if not path:
        path = os.getcwd()
    base = turbogears.config.get('engal.tagicons_directory', 'tagicons/')
    return os.path.join(path, base)