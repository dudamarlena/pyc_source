# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/__init__.py
# Compiled at: 2016-04-14 05:05:30
# Size of source mod 2**32: 16871 bytes
import operator, random
from abc import ABCMeta, abstractmethod
from collections import abc
from pynetics.utils import take_chances, clone_empty
from .exceptions import WrongValueForInterval, NotAProbabilityError, PyneticsError, InvalidSize
__version__ = '0.4.0'

class GeneticAlgorithm(metaclass=ABCMeta):
    """GeneticAlgorithm"""

    class GAListener:
        """GeneticAlgorithm.GAListener"""

        @abstractmethod
        def algorithm_started(self, ga):
            """ Called when the algorithm start.

            This method will be called AFTER initialization but BEFORE the first
            iteration, including the check against the stop condition.

            :param ga: The GeneticAlgorithm instanced that called this method.
            """
            pass

        @abstractmethod
        def algorithm_finished(self, ga):
            """ Called when the algorithm finishes.

            Particularly, this method will be called AFTER the stop condition
            has been met.

            :param ga: The GeneticAlgorithm instanced that called this method.
            """
            pass

        @abstractmethod
        def step_started(self, ga):
            """ Called when a new step of the genetic algorithm starts.

            This method will be called AFTER the stop condition has been checked
            and proved to be false) and BEFORE the new step is computed.

            :param ga: The GeneticAlgorithm instanced that called this method.
            """
            pass

        @abstractmethod
        def step_finished(self, ga):
            """ Called when a new step of the genetic algorithm finishes.

            This method will be called AFTER an step of the algorithm has been
            computed and BEFORE a new check against the stop condition is going
            to be made.

            :param ga: The GeneticAlgorithm instanced that called this method.
            """
            pass

    def __init__(self, stop_condition):
        self.stop_condition = stop_condition
        self.generation = 0
        self.listeners = []

    def run(self):
        """ Runs the simulation.

        The process is as follows: initialize populations and, while the stop
        condition is not met, do a new evolve step. This process relies in the
        abstract method "step".
        """
        self.initialize()
        [l.algorithm_started(self) for l in self.listeners]
        while self.best() is None or not self.stop_condition(self):
            [l.step_started(self) for l in self.listeners]
            self.step()
            self.generation += 1
            [l.step_finished(self) for l in self.listeners]

        self.finish()
        [l.algorithm_finished(self) for l in self.listeners]

    def initialize(self):
        """ Called when starting the genetic algorithm to initialize it. """
        self.generation = 0

    def step(self):
        """ Called on every iteration of the algorithm. """
        pass

    def finish(self):
        """ Called one the algorithm has finished. """
        pass

    @abstractmethod
    def best(self, generation=None):
        """ Returns the best individual obtained until this moment.

        :param generation: The generation of the individual that we want to
            recover. If not set, this will be the one emerged in the last
            generation. Defaults to None (not set, thus last generation).
        :return: The best individual generated in the specified generation.
        """
        pass


class StopCondition(metaclass=ABCMeta):
    """StopCondition"""

    @abstractmethod
    def __call__(self, genetic_algorithm):
        """ Checks if this stop condition is met.

        :param genetic_algorithm: The genetic algorithm where this stop
            condition belongs.
        :return: True if criteria is met, false otherwise.
        """
        pass


class Individual(metaclass=ABCMeta):
    """Individual"""

    def __init__(self):
        """ Initializes the individual.

        An individual contains a cache for the fitness method that prevents to
        compute it over and over again. However, as well as it is possible to
        clear this cache, also it is possible to disable it.

        :param disable_cache: Disables the fitness cache. Defaults to True,
            which means the cache is enabled.
        """
        self.population = None
        self.fitness_method = None

    def fitness(self):
        """ Computes the fitness of this individual.

        It will use the fitness method defined on its spawning pool.

        :param init: If this call to fitness is in initialization time. It
            defaults to False.
        :return: A float value.
        """
        return self.fitness_method(self)

    @abstractmethod
    def phenotype(self):
        """ The expression of this particular individual in the environment.

        :return: An object representing this individual in the environment
        """
        pass

    @abstractmethod
    def clone(self):
        """ Creates an instance as an exact copy of this individual

        If the implementing subclass has internal attributes to be cloned, the
        attributes copy should be implemented in an overriden version of this
        method.

        :return: A brand new individual like this one.
        """
        individual = clone_empty(self)
        individual.population = self.population
        individual.fitness_method = self.fitness_method
        return individual


class Diversity:
    """Diversity"""

    @abstractmethod
    def __call__(self, individuals):
        """ It returns a value that symbolizes how diverse is the population.

        The expected value will rely completely over the Individual
        implementation.

        :param individuals: A sequence of individuals from which obtain the
            diversity.
        :return: A value representing the diversity.
        """
        pass


class SpawningPool(metaclass=ABCMeta):
    """SpawningPool"""

    def __init__(self, fitness, diversity):
        """ Initializes this spawning pool.

        :param fitness: The method to evaluate individuals. It's expected to be
            a callable that returns a float value where the higher the value,
            the better the individual. Instances of subclasses of class Fitness
            can be used for this purpose.
        :param diversity: The method to compute the diversity of a sequence of
            individuals generated by this SpawningPool instance. Is expected to
            be a function that generates a diversity representation given a
            subset of individuals. Instances of subclasses of class Diversity
            can be used for this purpose.
        """
        self.population = None
        self.fitness = fitness
        self.diversity = diversity

    def spawn(self):
        """ Returns a new random individual.

        It uses the abstract method "create" to be implemented with the logic
        of individual creation. The purpose of this method is to add the
        parameters the base individual needs.

        :return: An individual instance.
        """
        individual = self.create()
        individual.population = self.population
        individual.fitness_method = self.fitness
        return individual

    @abstractmethod
    def create(self):
        """ Creates a new individual randomly.

        :return: A new Individual object.
        """
        pass


class Population(abc.MutableSequence):
    """Population"""

    def __init__(self, size=None, spawning_pool=None, individuals=None):
        """ Initializes the population, filling it with individuals.

        :param size: The size this population should have.
        :param spawning_pool: The object that generates individuals.
        :param individuals: The list of starting individuals. If none or if its
            length is lower than the population size, the rest of individuals
            will be generated randomly. If the length of initial individuals is
            greater than the population size, a random sample of the individuals
            is selected as members of population.
        :raises InvalidSize: If the provided size for the population is invalid.
        :raises UnexpectedClassError: If any of the instances provided wasn't
            of the required class.
        """
        if size is None or size < 1:
            raise InvalidSize('> 0', size)
        self.size = size
        self.spawning_pool = spawning_pool
        self.spawning_pool.population = self
        if individuals is not None:
            self.individuals = [i.clone() for i in individuals]
        else:
            self.individuals = []
        while len(self.individuals) > self.size:
            self.individuals.remove(random.choice(self.individuals))

        while len(self.individuals) < self.size:
            self.individuals.append(self.spawning_pool.spawn())

        self._Population__sorted = False
        self._Population__diversity = None

    def diversity(self):
        if self._Population__diversity is None:
            self._Population__diversity = self.spawning_pool.diversity(self.individuals)
        return self._Population__diversity

    def sort(self):
        """ Sorts this population from best to worst individual. """
        if self._Population__sorted is False:
            self.individuals.sort(key=operator.methodcaller('fitness'), reverse=True)
            self._Population__sorted = True

    def __len__(self):
        """ Returns the number fo individuals this population has. """
        return len(self.individuals)

    def __delitem__(self, i):
        """ Removes the ith individual from the population.

        The population will be sorted by its fitness before deleting.

        :param i: The ith individual to delete.
        """
        del self.individuals[i]
        self._Population__diversity = None

    def __setitem__(self, i, individual):
        """ Puts the named individual in the ith position.

        This call will cause a new sorting of the individuals the next time an
        access is required. This means that is preferable to make all the
        inserts in the population at once instead doing interleaved readings and
        inserts.

        :param i: The position where to insert the individual.
        :param individual: The individual to be inserted.
        """
        individual.population = self
        self.individuals.__setitem__(i, individual)
        self._Population__sorted = False
        self._Population__diversity = None

    def insert(self, i, individual):
        """ Ads a new element to the ith position of the population population.

        This call will cause a new sorting of the individuals the next time an
        access is required. This means that is preferable to make all the
        inserts in the population at once instead doing interleaved readings and
        inserts.

        :param i: The position where insert the individual.
        :param individual: The individual to be inserted in the population
        """
        individual.population = self
        self.individuals.insert(i, individual)
        self._Population__sorted = False
        self._Population__diversity = None

    def __getitem__(self, i):
        """ Returns the individual located on the ith position.

        The population will be sorted before accessing to the element so it's
        correct to assume that the individuals are arranged from fittest (i = 0)
        to least fit (n  len(populaton)).

        :param i: The index of the individual to retrieve.
        :return: The individual.
        """
        return self.individuals.__getitem__(i)

    def best(self):
        """ Returns the best individual for the gth.

        :return: The best individual for that generation.
        """
        self.sort()
        return self[0]


class Fitness(metaclass=ABCMeta):
    """Fitness"""

    @abstractmethod
    def __call__(self, individual):
        """ Estimates how adapted is the individual.

        Must return a float value where the higher the value, the better the
        adaption of the individual to the environment.

        :param individual: The individual to which estimate the adaptation.
        :return: A float value pointing the adation to the environment.
        """
        pass


class Mutation(metaclass=ABCMeta):
    """Mutation"""

    @abstractmethod
    def __call__(self, individual, p):
        """ Applies the mutation method to the individual.

        :param individual: an individual to mutate.
        :param p: The probability of mutation.
        :return: A cloned individual of the one passed as parameter but with a
            slightly (or not, X-MEN!!!!) mutation.
        """
        pass


class NoMutation(Mutation):

    def __call__(self, individual, p):
        return individual


class Recombination(metaclass=ABCMeta):
    """Recombination"""

    @abstractmethod
    def __call__(self, *args):
        """ Implementation of the recombine method.

        :param args: One or more Individual instances to use as parents in the
            recombination.
        :return: A sequence of individuals with characteristics of the parents.
        """
        pass


class Replacement(metaclass=ABCMeta):
    """Replacement"""

    @abstractmethod
    def __call__(self, population, individuals):
        """ It makes the replacement according to the subclass implementation.

        :param population: The population where make the replacement.
        :param individuals: The new population to use as replacement.
        """
        pass


class Selection(metaclass=ABCMeta):
    """Selection"""

    def __call__(self, population, n):
        """ Makes some checks to the configuration before delegating selection.

        After checking the parameters, the selection is performed by perform
        method.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return.
        :return: A sequence of individuals.
        :raises PyneticsError: If length of the population is smaller than the
            number of individuals to select and the repetition parameter is set
            to False (i.e. the same Individual cannot be selected twice or more
            times).
        """
        if len(population) < n:
            raise PyneticsError()
        else:
            return self.perform(population, n)

    @abstractmethod
    def perform(self, population, n):
        """ It makes the selection according to the subclass implementation.

        :param population: The population from which select the individuals.
        :param n: The number of individuals to return.
        :return: A sequence of n individuals.
        """
        pass


class Catastrophe(metaclass=ABCMeta):
    """Catastrophe"""

    @abstractmethod
    def __call__(self, population):
        """ Applies the catastrophe to the specified population.

        :param population: The population where apply the catastrophic method.
        """
        pass