# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynetics/algorithms.py
# Compiled at: 2016-04-13 18:41:07
# Size of source mod 2**32: 11935 bytes
import inspect, math, multiprocessing, random
from pynetics import Population, GeneticAlgorithm, take_chances, PyneticsError, NoMutation

class SimpleGA(GeneticAlgorithm):
    """SimpleGA"""

    def __init__(self, stop_condition, size, spawning_pool, selection, recombination, replacement, mutation=None, p_recombination=0.9, p_mutation=0.1, replacement_rate=1.0):
        """ Initializes this instance.

        :param stop_condition: The condition to be met in order to stop the
            genetic algorithm.
        :param size: The size this population should have.
        :param spawning_pool: The object that generates individuals.
        :param selection: The method to select individuals of the population to
            recombine.
        :param replacement: The method that will add and remove individuals from
            the population given the set of old individuals (i.e. the ones on
            the population before the evolution step) and new individuals (i.e.
            the offspring).
        :param recombination: The method to recombine parents in order to
            generate an offspring with characteristics of the parents. If none,
            no recombination will be applied.
        :param mutation: The method to mutate an individual. If none, no
            mutation over the individual will be applied. If not provided, no
            mutation is performed.
        :param p_recombination: The odds for recombination method to be
            performed over a set of selected individuals to generate progeny. If
            not performed, progeny will be the parents. Must be a value between
            0 and 1 (both included). If not provided, defaults to 1.0.
        :param p_mutation: The odds for mutation method to be performed over a
            progeny. It's applied once for each individual. If not performed the
            individuals will not be modified. Must be a value between 0 and 1
            (both included). If not provided, it defaults to 0.0 (no mutation is
            performed).
        :param replacement_rate: The rate of individuals to be replaced in each
            step of the algorithm. Must be a float value in the (0, 1] interval.
        :raises WrongValueForIntervalError: If any of the bounded values fall
            out of their respective intervals.
        :raises NotAProbabilityError: If a value was expected to be a
            probability and it wasn't.
        :raises UnexpectedClassError: If any of the input variables doesn't
            follow the contract required (i.e. doesn't inherit from a predefined
            class).
        """
        super().__init__(stop_condition=stop_condition)
        self.population_size = size
        self.spawning_pool = spawning_pool
        self.offspring_size = int(math.ceil(size * replacement_rate))
        self.selection = selection
        self.recombination = recombination
        self.mutation = mutation or NoMutation()
        self.replacement = replacement
        self.replacement_rate = replacement_rate
        self.p_recombination = p_recombination
        self.p_mutation = p_mutation
        self.selection_size = len(inspect.signature(recombination.__call__).parameters)
        self.population = None
        self.best_individuals = []

    def initialize(self):
        self.population = Population(size=self.population_size, spawning_pool=self.spawning_pool)

    def step(self):
        offspring = []
        while len(offspring) < self.offspring_size:
            parents = self.selection(self.population, self.selection_size)
            if take_chances(self.p_recombination):
                progeny = self.recombination(*parents)
            else:
                progeny = [i.clone() for i in parents]
            individuals_who_fit = min(len(progeny), self.offspring_size - len(offspring))
            progeny = [self.mutation(individual, self.p_mutation) for individual in random.sample(progeny, individuals_who_fit)]
            offspring.extend(progeny)

        self.replacement(self.population, offspring)
        if self.generation < len(self.best_individuals):
            self.best_individuals[self.generation] = self.population.best()
        else:
            self.best_individuals.append(self.population.best())

    def best(self, generation=None):
        if self.best_individuals:
            generation = generation or -1
            if generation > len(self.best_individuals) - 1:
                raise PyneticsError()
            else:
                return self.best_individuals[generation]
        else:
            return


class ConcurrentGA(GeneticAlgorithm):

    def __init__(self, stop_condition, size, spawning_pool, selection, recombination, replacement, mutation=None, p_recombination=0.9, p_mutation=0.1, replacement_rate=1.0, processes=None):
        super().__init__(stop_condition=stop_condition)
        self.spawning_pool = spawning_pool
        self.offspring_size = int(math.ceil(size * replacement_rate))
        self.selection = selection
        self.recombination = recombination
        self.mutation = mutation or NoMutation()
        self.replacement = replacement
        self.replacement_rate = replacement_rate
        self.p_recombination = p_recombination
        self.p_mutation = p_mutation
        self.nproc = processes or multiprocessing.cpu_count()
        print('Entrenando en {} procesos'.format(self.nproc))
        self.psize = int((size + self.nproc - 1) // self.nproc * self.nproc)
        if size != self.psize:
            print('Ajustada población a {} para los {} procesos'.format(self.psize, self.nproc))
        self.csize = int(self.psize / self.nproc)
        self.selection_size = len(inspect.signature(recombination.__call__).parameters)
        self.population = None
        self.best_individuals = []
        self.evolver_processes = []

    class EvolverProcess:

        def __init__(self, steps, selection, recombination, mutation, replacement, replacement_rate, p_recombination, p_mutation):
            self.steps = steps
            self.selection = selection
            self.recombination = recombination
            self.mutation = mutation
            self.replacement = replacement
            self.replacement_rate = replacement_rate
            self.p_recombination = p_recombination
            self.p_mutation = p_mutation
            self.selection_size = len(inspect.signature(recombination.__call__).parameters)
            self.input = multiprocessing.Queue()
            self.output = multiprocessing.Queue()
            self.stop = False

        def run(self):
            while not self.stop:
                population = self.input.get()
                offspring_size = int(math.ceil(len(population) * self.replacement_rate))
                for _ in range(self.steps):
                    self.step(population, offspring_size)

                offspring = []
                for individual in population:
                    individual.population = None
                    offspring.append(individual)

                self.output.put(offspring)

        def step(self, population, offspring_size):
            offspring = []
            while len(offspring) < offspring_size:
                parents = self.selection(population, self.selection_size)
                if take_chances(self.p_recombination):
                    progeny = self.recombination(*parents)
                else:
                    progeny = parents
                individuals_who_fit = min(len(progeny), offspring_size - len(offspring))
                progeny = [self.mutation(individual, self.p_mutation) for individual in random.sample(progeny, individuals_who_fit)]
                offspring.extend(progeny)

            self.replacement(population, offspring)

    def initialize(self):
        self.population = Population(size=self.psize, spawning_pool=self.spawning_pool)
        self.best_individuals = [
         self.population.best()]
        for i in range(self.nproc):
            self.evolver_processes.append(ConcurrentGA.EvolverProcess(steps=10, selection=self.selection, recombination=self.recombination, mutation=self.mutation, replacement=self.replacement, replacement_rate=self.replacement_rate, p_recombination=self.p_recombination, p_mutation=self.p_mutation))
            proc = multiprocessing.Process(target=self.evolver_processes[i].run)
            proc.daemon = True
            proc.start()

    def step(self):
        random.shuffle(self.population)
        for i, evolver_process in enumerate(self.evolver_processes):
            evolver_process.input.put(Population(size=self.psize, spawning_pool=self.spawning_pool, individuals=self.population[self.csize * i:self.csize * (i + 1)]), False)

        offspring = []
        for evolver_process in self.evolver_processes:
            offspring += evolver_process.output.get()

        if len(offspring) > self.offspring_size:
            offspring = random.sample(offspring, self.offspring_size)
        self.replacement(self.population, offspring)
        if self.generation < len(self.best_individuals):
            self.best_individuals[self.generation] = self.population.best()
        else:
            self.best_individuals.append(self.population.best())

    def finish(self):
        for evolver_process in self.evolver_processes:
            evolver_process.stop = True

        multiprocessing.active_children()

    def best(self, generation=None):
        generation = generation or -1
        if generation > len(self.best_individuals) - 1:
            raise PyneticsError()
        else:
            return self.best_individuals[generation]