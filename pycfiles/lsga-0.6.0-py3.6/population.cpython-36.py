# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/components/population.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 7926 bytes
from .individual import IndividualBase
from joblib import Parallel, delayed

class Memoized(object):
    __doc__ = ' Descriptor for population statistical varibles caching.\n    '

    def __init__(self, func):
        self.func = func
        self.result = None
        self.fitness = None

    def __get__(self, instance, cls):
        self.instance = instance
        return self

    def __call__(self, fitness):
        if not self.instance.updated:
            if self.result is not None:
                if fitness == self.fitness:
                    return self.result
        self.fitness = fitness
        self.result = self.func(self.instance, fitness)
        self.instance._updated = False
        return self.result


class Individuals(object):
    __doc__ = ' Descriptor for all individuals in population.\n\n    .. Note::\n        Use this descriptor to ensure the individual related flags can be updated\n        when the population indivduals are changed.\n    '

    def __init__(self, name):
        self.name = '_{}'.format(name)

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        instance.__dict__[self.name] = value
        instance.update_flag()


class Population(object):
    __doc__ = ' Class for representing population in genetic algorithm.\n\n    :param indv_template: A template individual to clone all the other\n                          individuals in current population.\n    :type indv_template: :obj:`lsga.components.IndividualBase`\n\n    :param size: The size of population, number of individuals in population.\n    :type size: int\n    '
    individuals = Individuals('individuals')

    def __init__(self, indv_template, n_jobs=1, size=100):
        self.n_jobs = n_jobs
        if size % 2 != 0:
            raise ValueError('Population size must be an even number')
        self.size = size
        self.indv_template = indv_template
        self._updated = False

        class IndvList(list):
            __doc__ = ' A proxy class inherited from built-in list to contain all\n            individuals which can update the population._updated flag\n            automatically when its content is changed.\n            '

            def __init__(this, *args):
                (super(this.__class__, this).__init__)(*args)

            def __setitem__(this, key, value):
                old_value = this[key]
                if old_value == value:
                    return
                super(this.__class__, self).__setitem__(key, value)
                self.update_flag()

            def append(this, item):
                super(this.__class__, this).append(item)
                self.update_flag()

            def extend(this, iterable_item):
                if not iterable_item:
                    return
                super(this.__class__, this).extend(iterable_item)
                self.update_flag()

        self._individuals = IndvList()

    def init(self, indvs=None):
        """ Initialize current population with individuals.

        :param indvs: Initial individuals in population, randomly initialized
                      individuals are created if not provided.
        :type indvs: list of Individual object
        """
        IndvType = self.indv_template.__class__
        if indvs is None:
            for _ in range(self.size):
                indv = IndvType(ranges=(self.indv_template.ranges), eps=(self.indv_template.eps))
                self.individuals.append(indv)

        else:
            if len(indvs) != self.size:
                raise ValueError('Invalid individuals number')
            for indv in indvs:
                if not isinstance(indv, IndividualBase):
                    raise ValueError('individual class must be subclass of IndividualBase')

            self.individuals = indvs
        self._updated = True
        return self

    def update_flag(self):
        """ Interface for updating individual update flag to True.
        """
        self._updated = True

    @property
    def updated(self):
        """ Query function for population updating flag.
        """
        return self._updated

    def new(self):
        """ Create a new emtpy population.
        """
        return self.__class__(indv_template=(self.indv_template), size=(self.size))

    def __getitem__(self, key):
        """
        Get individual by index.
        """
        if key < 0 or key >= self.size:
            raise IndexError('Individual index({}) out of range'.format(key))
        return self.individuals[key]

    def __len__(self):
        """
        Get length of population.
        """
        return len(self.individuals)

    def best_indv(self, fitness):
        """ The individual with the best fitness.

        :param fitness: Fitness function to calculate fitness value
        :type fitness: function

        :return: the best individual in current population
        :rtype: :obj:`lsga.components.IndividualBase`
        """
        all_fits = self.all_fits(fitness)
        return max((self.individuals), key=(lambda indv: all_fits[self.individuals.index(indv)]))

    def worst_indv(self, fitness):
        """ The individual with the worst fitness.

        :param fitness: Fitness function to calculate fitness value
        :type fitness: function

        :return: the worst individual in current population
        :rtype: :obj:`lsga.components.IndividualBase`
        """
        all_fits = self.all_fits(fitness)
        return min((self.individuals), key=(lambda indv: all_fits[self.individuals.index(indv)]))

    def max(self, fitness):
        """ Get the maximum fitness value in population.

        :param fitness: Fitness function to calculate fitness value
        :type fitness: function

        :return: The maximum fitness value
        :rtype: float
        """
        return max(self.all_fits(fitness))

    def min(self, fitness):
        """ Get the minimum value of fitness in population.

        :param fitness: Fitness function to calculate fitness value
        :type fitness: function

        :return: The minimum fitness value
        :rtype: float
        """
        return min(self.all_fits(fitness))

    def mean(self, fitness):
        """ Get the average fitness value in population.

        :param fitness: Fitness function to calculate fitness value
        :type fitness: function

        :return: The average fitness value
        :rtype: float
        """
        all_fits = self.all_fits(fitness)
        return sum(all_fits) / len(all_fits)

    @Memoized
    def all_fits(self, fitness):
        """ Get all fitness values in population.

        :param fitness: Fitness function to calculate fitness value
        :type fitness: function
        """
        return Parallel(n_jobs=(self.n_jobs), verbose=10)(delayed(fitness)(indv) for indv in self.individuals)