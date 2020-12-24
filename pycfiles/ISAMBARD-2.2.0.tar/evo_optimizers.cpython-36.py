# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cw12401/code/work/isambard/src/isambard/optimisation/evo_optimizers.py
# Compiled at: 2018-04-18 05:33:18
# Size of source mod 2**32: 25303 bytes
"""Bio-inspired optimizers."""
import operator, random
from deap import creator, tools
import numpy
from .base_evo_opt import BaseOptimizer, Parameter, default_build

class DE(BaseOptimizer):
    __doc__ = 'Differential evolution optimisation algorithm.\n\n    Notes\n    -----\n    Can use neighbourhood model to reduce chance of getting stuck\n    in local optima. This is a very versatile algorithm, and its use\n    is recommended.\n\n    Parameters\n    ----------\n    specification : ampal.specification.assembly_specification\n        An `Assembly` level specification to be optimised.\n    sequences : [str]\n        A list of sequences, one for each polymer.\n    parameters : [base_ev_opt.Parameter]\n        A list of `Parameter` objects in the same order as the\n        function signature expects.\n    build_fn : function((spec, seq, params)) -> ampal\n        A function for building a model using parameters supplied\n        by the optimizer.\n    eval_fn : function(ampal) -> float\n        An evaluation function that assesses an AMPAL object and\n        returns a float. This float will be used to compare models.\n        The optimizer uses the thermodynamic convention that lower\n        numbers are better.\n    cxpb : float\n        The probability of crossing two individuals.\n    diff_weight : float\n        A scaling factor for crossing.\n    neighbours : int or None\n        If not `None`, uses a neighbourhood model to reduce the\n        likelihood of the optimisation getting stuck in a local\n        optima. The number of particles to use as neighbours can\n        be provided as an int.\n    '

    def __init__(self, specification, sequences, parameters, eval_fn, build_fn=default_build, cxpb=0.75, diff_weight=1, neighbours=None, **kwargs):
        (super().__init__)(
 specification, sequences, parameters, build_fn=build_fn, 
         eval_fn=eval_fn, **kwargs)
        self.cxpb = cxpb
        self.diff_weight = diff_weight
        self.neighbours = neighbours
        creator.create('Individual', list, fitness=(creator.FitnessMin))

    def _generate(self):
        """Generates a particle using the creator function.

        Notes
        -----
        Position and speed are uniformly randomly seeded within
        allowed bounds. The particle also has speed limit settings
        taken from global values.

        Returns
        -------
        particle object
        """
        ind = creator.Individual([random.uniform(-1, 1) for _ in range(len(self.value_means))])
        ind.ident = None
        ind.neighbours = None
        return ind

    def _initialize_pop(self, pop_size):
        """Assigns indices to individuals in population."""
        self.toolbox.register('individual', self._generate)
        self.toolbox.register('population', tools.initRepeat, list, self.toolbox.individual)
        self.population = self.toolbox.population(n=pop_size)
        if self.neighbours:
            for i in range(len(self.population)):
                self.population[i].ident = i
                self.population[i].neighbours = list(set([(i - x) % len(self.population) for x in range(1, self.neighbours + 1)] + [(i + x) % len(self.population) for x in range(1, self.neighbours + 1)]))

        self.assign_fitnesses(self.population)

    def _crossover(self, ind):
        """Used by the evolution process to generate a new individual.

        Notes
        -----
        This is a tweaked version of the classical DE crossover
        algorithm, the main difference that candidate parameters are
        generated using a lognormal distribution. Bound handling is
        achieved by resampling where the candidate solution exceeds +/-1

        Parameters
        ----------
        ind : deap individual

        Returns
        -------
        y : deap individual
            An individual representing a candidate solution, to be
            assigned a fitness.
        """
        if self.neighbours:
            a, b, c = random.sample([self.population[i] for i in ind.neighbours], 3)
        else:
            a, b, c = random.sample(self.population, 3)
        y = self.toolbox.clone(a)
        y.ident = ind.ident
        y.neighbours = ind.neighbours
        del y.fitness.values
        ident = random.randrange(len(self.value_means))
        for i, value in enumerate(y):
            if i == ident or random.random() < self.cxpb:
                entry = a[i] + random.lognormvariate(-1.2, 0.5) * self.diff_weight * (b[i] - c[i])
                tries = 0
                while abs(entry) > 1.0:
                    tries += 1
                    entry = a[i] + random.lognormvariate(-1.2, 0.5) * self.diff_weight * (b[i] - c[i])
                    if tries > 10000:
                        entry = a[i]

                y[i] = entry

        return y

    def _update_pop(self, pop_size):
        """Updates population according to crossover and fitness criteria."""
        candidates = []
        for ind in self.population:
            candidates.append(self._crossover(ind))

        self._model_count += len(candidates)
        self.assign_fitnesses(candidates)
        for i in range(len(self.population)):
            if candidates[i].fitness > self.population[i].fitness:
                self.population[i] = candidates[i]


class PSO(BaseOptimizer):
    __doc__ = 'A particle swarm optimization algorithm.\n\n    Notes\n    -----\n    This is good for avoiding bias and premature minimization, though\n    it may struggle to find the ultimate optimum solution. Supports\n    the neighbourhood model. Bound handling is achieved by allowing\n    particles to exceed permitted bounds, but not assigning them a\n    fitness in this case.\n\n    Parameters\n    ----------\n    specification : ampal.specification.assembly_specification\n        An `Assembly` level specification to be optimised.\n    sequences : [str]\n        A list of sequences, one for each polymer.\n    parameters : [base_ev_opt.Parameter]\n        A list of `Parameter` objects in the same order as the\n        function signature expects.\n    build_fn : function((spec, seq, params)) -> ampal\n        A function for building a model using parameters supplied\n        by the optimizer.\n    eval_fn : function(ampal) -> float\n        An evaluation function that assesses an AMPAL object and\n        returns a float. This float will be used to compare models.\n        The optimizer uses the thermodynamic convention that lower\n        numbers are better.\n    max_speed : float\n        The maximum speed that a particle can have in the swarm.\n    neighbours : int or None\n        If not `None`, uses a neighbourhood model to reduce the\n        likelihood of the optimisation getting stuck in a local\n        optima. The number of particles to use as neighbours can\n        be provided as an int.\n    '

    def __init__(self, specification, sequences, parameters, eval_fn, build_fn=default_build, max_speed=0.75, neighbours=None, **kwargs):
        (super().__init__)(
 specification, sequences, parameters, build_fn=build_fn, 
         eval_fn=eval_fn, **kwargs)
        self.max_speed = 0.75
        self.neighbours = None
        creator.create('Particle', list, fitness=(creator.FitnessMin), speed=list,
          smin=None,
          smax=None,
          best=None)
        self.toolbox.register('particle', self._generate)
        creator.create('Swarm', list, gbest=None, gbestfit=(creator.FitnessMin))
        self.toolbox.register('swarm', tools.initRepeat, creator.Swarm, self.toolbox.particle)

    def _initialize_pop(self, pop_size):
        """Generates initial population with random positions and speeds."""
        self.population = self.toolbox.swarm(n=pop_size)
        if self.neighbours:
            for i in range(len(self.population)):
                self.population[i].ident = i
                self.population[i].neighbours = list(set([(i - x) % len(self.population) for x in range(1, self.neighbours + 1)] + [i] + [(i + x) % len(self.population) for x in range(1, self.neighbours + 1)]))

        else:
            for i in range(len(self.population)):
                self.population[i].ident = i
                self.population[i].neighbours = [x for x in range(len(self.population))]

        self.assign_fitnesses(self.population)
        for part in self.population:
            part.best = creator.Particle(part)
            part.best.fitness.values = part.fitness.values

    def _generate(self):
        """Generates a particle using the creator function.

        Notes
        -----
        Position and speed are uniformly randomly seeded within
        allowed bounds. The particle also has speed limit settings
        taken from global values.

        Returns
        -------
        part : particle object
            A particle used during optimisation.
        """
        part = creator.Particle([random.uniform(-1, 1) for _ in range(len(self.value_means))])
        part.speed = [random.uniform(-self.max_speed, self.max_speed) for _ in range(len(self.value_means))]
        part.smin = -self.max_speed
        part.smax = self.max_speed
        part.ident = None
        part.neighbours = None
        return part

    def update_particle(self, part, chi=0.729843788, c=2.05):
        """Constriction factor update particle method.

        Notes
        -----
        Looks for a list of neighbours attached to a particle and
        uses the particle's best position and that of the best
        neighbour.
        """
        neighbour_pool = [self.population[i] for i in part.neighbours]
        best_neighbour = max(neighbour_pool, key=(lambda x: x.best.fitness))
        ce1 = (c * random.uniform(0, 1) for _ in range(len(part)))
        ce2 = (c * random.uniform(0, 1) for _ in range(len(part)))
        ce1_p = map(operator.mul, ce1, map(operator.sub, part.best, part))
        ce2_g = map(operator.mul, ce2, map(operator.sub, best_neighbour.best, part))
        chi_list = [chi] * len(part)
        chi_list2 = [1 - chi] * len(part)
        a = map(operator.sub, map(operator.mul, chi_list, map(operator.add, ce1_p, ce2_g)), map(operator.mul, chi_list2, part.speed))
        part.speed = list(map(operator.add, part.speed, a))
        for i, speed in enumerate(part.speed):
            if speed < part.smin:
                part.speed[i] = part.smin
            else:
                if speed > part.smax:
                    part.speed[i] = part.smax

        part[:] = list(map(operator.add, part, part.speed))

    def _update_pop(self, pop_size):
        """Assigns fitnesses to particles that are within bounds."""
        valid_particles = []
        invalid_particles = []
        for part in self.population:
            if any(x > 1 or x < -1 for x in part):
                invalid_particles.append(part)
            else:
                valid_particles.append(part)

        self._model_count += len(valid_particles)
        for part in valid_particles:
            self.update_particle(part)

        self.assign_fitnesses(valid_particles)
        for part in valid_particles:
            if part.fitness > part.best.fitness:
                part.best = creator.Particle(part)
                part.best.fitness = part.fitness

        for part in invalid_particles:
            self.update_particle(part)

        self.population[:] = valid_particles + invalid_particles
        self.population.sort(key=(lambda x: x.ident))


class GA(BaseOptimizer):
    __doc__ = 'A classic genetic algorithm optimization algorithm.\n\n    Notes\n    -----\n    Very good for eliminating unfavourable regions of the search space.\n    Can be heavily customized in terms of mutation and crossover operators\n    etc. Bound handling is achieved simply by amending any out of\n    bounds parameters to the boundary value.\n\n    Parameters\n    ----------\n    specification : ampal.specification.assembly_specification\n        An `Assembly` level specification to be optimised.\n    sequences : [str]\n        A list of sequences, one for each polymer.\n    parameters : [base_ev_opt.Parameter]\n        A list of `Parameter` objects in the same order as the\n        function signature expects.\n    build_fn : function((spec, seq, params)) -> ampal\n        A function for building a model using parameters supplied\n        by the optimizer.\n    eval_fn : function(ampal) -> float\n        An evaluation function that assesses an AMPAL object and\n        returns a float. This float will be used to compare models.\n        The optimizer uses the thermodynamic convention that lower\n        numbers are better.\n    cxpb : float\n        The probability of crossing two individuals.\n    mutpb : float\n        Probability of mutating an individual.\n    '

    def __init__(self, specification, sequences, parameters, eval_fn, build_fn=default_build, cxpb=0.5, mutpb=0.2, **kwargs):
        (super().__init__)(
 specification, sequences, parameters, build_fn=build_fn, 
         eval_fn=eval_fn, **kwargs)
        self.cxpb = cxpb
        self.mutpb = mutpb
        creator.create('Individual', list, fitness=(creator.FitnessMin))
        self.toolbox.register('mate', (tools.cxBlend), alpha=0.2)
        self.toolbox.register('mutate', (tools.mutGaussian), mu=0,
          sigma=0.2,
          indpb=0.4)
        self.toolbox.register('select', tools.selTournament)

    def _generate(self):
        """Generates a particle using the creator function."""
        ind = creator.Individual([random.uniform(-1, 1) for _ in range(len(self.value_means))])
        return ind

    def _initialize_pop(self, pop_size):
        """Assigns indices to individuals in population."""
        self.toolbox.register('individual', self._generate)
        self.toolbox.register('population', tools.initRepeat, list, self.toolbox.individual)
        self.population = self.toolbox.population(n=pop_size)
        self.assign_fitnesses(self.population)
        self._model_count += len(self.population)

    def _update_pop(self, pop_size):
        """Updates population according to crossover and fitness criteria."""
        offspring = list(map(self.toolbox.clone, self.population))
        for _ in range(pop_size // 2):
            if random.random() < self.cxpb:
                child1, child2 = self.toolbox.select(self.population, 2, 6)
                temp1 = self.toolbox.clone(child1)
                temp2 = self.toolbox.clone(child2)
                self.toolbox.mate(temp1, temp2)
                del temp1.fitness.values
                del temp2.fitness.values
                offspring.append(temp1)
                offspring.append(temp2)

        for mutant in offspring:
            if random.random() < self.mutpb:
                self.toolbox.mutate(mutant)
                del mutant.fitness.values

        for i in range(len(offspring)):
            for j in range(len(offspring[i])):
                if offspring[i][j] > 1:
                    offspring[i][j] = 1
                if offspring[i][j] < -1:
                    offspring[i][j] = -1

        self._model_count += len([ind for ind in offspring if not ind.fitness.values])
        self.assign_fitnesses([ind for ind in offspring if not ind.fitness.valid])
        offspring.sort(reverse=True, key=(lambda x: x.fitness))
        if len(self.halloffame) != 0:
            if offspring[0].fitness < self.halloffame[0].fitness:
                offspring.insert(0, self.halloffame[0])
        self.population[:] = offspring[:pop_size]


class CMAES(BaseOptimizer):
    __doc__ = "Covariance matrix adaptation evolutionary strategy optimizer.\n\n    Notes\n    -----\n    Basically uses a covariance matrix at each step to identify the\n    'direction' of the optimal solution in the search space, and\n    generates new individuals accordingly. Bound handling is achieved\n    by moving any out of bounds parameters to the boundary condition.\n    Other than that the implementation used here is as in the\n    originating code from the deap module.\n\n    Parameters\n    ----------\n    specification : ampal.specification.assembly_specification\n        An `Assembly` level specification to be optimised.\n    sequences : [str]\n        A list of sequences, one for each polymer.\n    parameters : [base_ev_opt.Parameter]\n        A list of `Parameter` objects in the same order as the\n        function signature expects.\n    build_fn : function((spec, seq, params)) -> ampal\n        A function for building a model using parameters supplied\n        by the optimizer.\n    eval_fn : function(ampal) -> float\n        An evaluation function that assesses an AMPAL object and\n        returns a float. This float will be used to compare models.\n        The optimizer uses the thermodynamic convention that lower\n        numbers are better.\n    sigma : float\n        Initial standard deviation of the distribution.\n    weight_type : str\n        Can be 'linear', 'superlinear' or 'equal'. Used to decrease\n        speed of particles.\n    "

    def __init__(self, specification, sequences, parameters, eval_fn, build_fn=default_build, sigma=0.3, weight_type='superlinear', **kwargs):
        (super().__init__)(
 specification, sequences, parameters, build_fn=build_fn, 
         eval_fn=eval_fn, **kwargs)
        self.sigma = sigma
        self.weight_type = weight_type
        creator.create('Individual', list, fitness=(creator.FitnessMin))

    def _initialize_pop(self, pop_size):
        """Generates the initial population and assigns fitnesses."""
        self.initialize_cma_es(pop_size)
        self.toolbox.register('individual', self._make_individual)
        self.toolbox.register('generate', self._generate, self.toolbox.individual)
        self.toolbox.register('population', tools.initRepeat, list, self._initial_individual)
        self.toolbox.register('update', self.update)
        self.population = self.toolbox.population(n=pop_size)
        self.assign_fitnesses(self.population)
        self._model_count += len(self.population)

    def _initial_individual(self):
        """Generates an individual with random parameters within bounds."""
        ind = creator.Individual([random.uniform(-1, 1) for _ in range(len(self.value_means))])
        return ind

    def _update_pop(self, pop_size):
        """Updates population according to crossover and fitness criteria."""
        self.toolbox.generate()
        for i in range(len(self.population)):
            for j in range(len(self.population[i])):
                if self.population[i][j] > 1:
                    self.population[i][j] = 1
                if self.population[i][j] < -1:
                    self.population[i][j] = -1

        self.assign_fitnesses(self.population)
        self.toolbox.update(self.population)
        self._model_count += len(self.population)

    def _make_individual(self, paramlist):
        """Makes an individual particle."""
        part = creator.Individual(paramlist)
        part.ident = None
        return part

    def initialize_cma_es(self, lambda_):
        """A strategy that will keep track of the basic parameters.

        Parameters
        ----------
        centroid:
            An iterable object that indicates where to start the
            evolution.
        parameter:
            One or more parameter to pass to the strategy as
            described in the following table, optional.
        """
        self.centroid = numpy.array([0] * len(self.value_means))
        self.dim = len(self.centroid)
        self.pc = numpy.zeros(self.dim)
        self.ps = numpy.zeros(self.dim)
        self.chiN = numpy.sqrt(self.dim) * (1 - 1.0 / (4.0 * self.dim) + 1.0 / (21.0 * self.dim ** 2))
        self.C = numpy.identity(self.dim)
        self.diagD, self.B = numpy.linalg.eigh(self.C)
        indx = numpy.argsort(self.diagD)
        self.diagD = self.diagD[indx] ** 0.5
        self.B = self.B[:, indx]
        self.BD = self.B * self.diagD
        self.cond = self.diagD[indx[(-1)]] / self.diagD[indx[0]]
        self.lambda_ = lambda_
        self.update_count = 0
        self.compute_params()

    def _generate(self, func):
        r"""Generate a population of :math:`\lambda` individuals.

        Notes
        -----
        Individuals are of type *ind_init* from the current strategy.

        Parameters
        ----------
        ind_init:
            A function object that is able to initialize an
            individual from a list.
        """
        arz = numpy.random.standard_normal((self.lambda_, self.dim))
        arz = self.centroid + self.sigma * numpy.dot(arz, self.BD.T)
        self.population = list(map(func, arz))

    def update(self, population):
        """Update the covariance matrix strategy from the *population*.

        Parameters
        ----------
        population:
            A list of individuals from which to update the
            parameters.
        """
        population.sort(key=(lambda ind: ind.fitness), reverse=True)
        old_centroid = self.centroid
        self.centroid = numpy.dot(self.weights, population[0:self.mu])
        c_diff = self.centroid - old_centroid
        self.ps = (1 - self.cs) * self.ps + numpy.sqrt(self.cs * (2 - self.cs) * self.mueff) / self.sigma * numpy.dot(self.B, 1.0 / self.diagD * numpy.dot(self.B.T, c_diff))
        hsig = float(numpy.linalg.norm(self.ps) / numpy.sqrt(1.0 - (1.0 - self.cs) ** (2.0 * (self.update_count + 1.0))) / self.chiN < 1.4 + 2.0 / (self.dim + 1.0))
        self.update_count += 1
        self.pc = (1 - self.cc) * self.pc + hsig * numpy.sqrt(self.cc * (2 - self.cc) * self.mueff) / self.sigma * c_diff
        artmp = population[0:self.mu] - old_centroid
        self.C = (1 - self.ccov1 - self.ccovmu + (1 - hsig) * self.ccov1 * self.cc * (2 - self.cc)) * self.C + self.ccov1 * numpy.outer(self.pc, self.pc) + self.ccovmu * numpy.dot(self.weights * artmp.T, artmp) / self.sigma ** 2
        self.sigma *= numpy.exp((numpy.linalg.norm(self.ps) / self.chiN - 1.0) * self.cs / self.damps)
        self.diagD, self.B = numpy.linalg.eigh(self.C)
        indx = numpy.argsort(self.diagD)
        self.cond = self.diagD[indx[(-1)]] / self.diagD[indx[0]]
        self.diagD = self.diagD[indx] ** 0.5
        self.B = self.B[:, indx]
        self.BD = self.B * self.diagD

    def compute_params(self):
        r"""Computes the parameters depending on :math:`\lambda`.

        Notes
        -----
        It needs to be called again if :math:`\lambda` changes during
        evolution.
        """
        self.mu = int(self.lambda_ / 2)
        if self.weight_type == 'superlinear':
            self.weights = numpy.log(self.mu + 0.5) - numpy.log(numpy.arange(1, self.mu + 1))
        else:
            if self.weight_type == 'linear':
                self.weights = self.mu + 0.5 - numpy.arange(1, self.mu + 1)
            else:
                if self.weight_type == 'equal':
                    self.weights = numpy.ones(self.mu)
                else:
                    raise RuntimeError('Unknown weight type: {}'.format(self.weight_type))
        self.weights /= sum(self.weights)
        self.mueff = 1.0 / sum(self.weights ** 2)
        self.cc = 4.0 / (self.dim + 4.0)
        self.cs = (self.mueff + 2.0) / (self.dim + self.mueff + 3.0)
        self.ccov1 = 2.0 / ((self.dim + 1.3) ** 2 + self.mueff)
        self.ccovmu = 2.0 * (self.mueff - 2.0 + 1.0 / self.mueff) / ((self.dim + 2.0) ** 2 + self.mueff)
        self.ccovmu = min(1 - self.ccov1, self.ccovmu)
        self.damps = 1.0 + 2.0 * max(0, numpy.sqrt((self.mueff - 1.0) / (self.dim + 1.0)) - 1.0) + self.cs


__author__ = 'Andrew R. Thomson, Christopher W. Wood, Gail J. Bartlett'
__status__ = 'Development'