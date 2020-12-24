# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage/operators.py
# Compiled at: 2015-12-21 16:57:03
import random
from pyage.events import EventHook
from pyage.genotype import PointGenotype
from pyage.inject import Inject

def points_population_generator():
    return [ PointGenotype(random.random(), random.random()) for _ in range(100) ]


def points_population_generator_factory():
    return points_population_generator


def rosenbrock(point):
    x, y = point.x, point.y
    point.fitness = -(1 - x) ** 2 - 100 * (y - x ** 2) ** 2
    return point


def rosenbrock_evaluation(population):
    map(lambda point: rosenbrock(point), population)


def random_selection(population):
    for point in population:
        if random.random() < 0.001:
            population.remove(point)


def random_mutation(population):
    for point in population:
        point.x += random.random() * 10 - 5
        point.y += random.random() * 10 - 5


class RandomStopCondition(object):

    @Inject('event_manager')
    def __init__(self):
        pass

    def should_stop(self, population):
        stop = random.random() > 0.99
        if stop:
            self.event_manager.fire(population)
        return stop


event = EventHook()

def end(population):
    print 'end: ',
    print population
    print 'best: ',
    print reduce(lambda x, y: x.fitness > y.fitness and x or y, population)


event += lambda population: end(population)