# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/methods/deap_swarm.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 15781 bytes
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import numpy as np, scipy, itertools, random
from pyxrd.refinement.refine_method import RefineMethod
from pyxrd.refinement.refine_method_option import RefineMethodOption
from pyxrd.refinement.refine_async_helper import RefineAsyncHelper
from deap import base, creator, tools
from .deap_utils import pyxrd_array, PyXRDParetoFront, FitnessMin, result_func
NGEN = 100
NSWARMS = 1
NEXCESS = 3
NPARTICLES = 15
CONV_FACTR = 0.3

class MultiPSOStrategy(object):

    def generate_particle(self, pclass, dim, pmin, pmax, smin, smax):
        """ Generate a particle """
        part = pclass(random.uniform(pmin[i], pmax[i]) for i in range(dim))
        part.speed = np.array([random.uniform(smin[i], smax[i]) for i in range(dim)])
        return part

    def update_particle(self, part, best, chi, c):
        """
            Update a particle's position & speed
            part: the particle
            best: the global best
            chi ~ recombination factor
            c ~ scale factor(s)
        """
        part_pos = np.asarray(part)
        best_pos = np.asarray(best)
        pers_pos = np.asarray(part.best)
        speed = np.asarray(part.speed)
        ce1 = c * np.random.uniform(0, 1, size=(len(part)))
        ce2 = c * np.random.uniform(0, 1, size=(len(part)))
        ce1_p = ce1 * np.array(best_pos - part_pos)
        ce1_g = ce2 * np.array(pers_pos - part_pos)
        f = ce1_p + ce1_g
        a = chi * (f + speed) - speed
        speed = a + speed
        part[:] = part_pos + speed
        part.speed = speed
        del part.fitness.values

    def create_swarm(self, container, iterable):
        """ Returns a swarm container using the iterable """
        return container(iterable)

    def generate_particles(self, func, n):
        """ Returns a particle generator """
        for _ in range(n):
            yield func()

    def update_swarm(self, swarm, part):
        """ Update swarm's attractors personal best and global best """
        if not part.fitness.valid:
            raise RuntimeError('Particles need to have a valid fitness before calling update_swarm!')
        else:
            if part.best == None or part.fitness > part.bestfit:
                part.best = creator.Particle(part)
                part.bestfit.values = part.fitness.values
            if swarm.best == None or part.fitness > swarm.bestfit:
                swarm.best = creator.Particle(part)
                swarm.bestfit.values = part.fitness.values

    def give_reinit_swarms(self, population):
        """ Gives a set of swarm indeces that need to be reinitialized (overlap)"""
        reinit_swarms = set()
        for s1, s2 in itertools.combinations(list(range(len(population))), 2):
            if population[s1].best is not None and population[s2].best is not None and not (s1 in reinit_swarms or s2 in reinit_swarms):
                t, _ = scipy.stats.ttest_ind(population[s1], population[s2])
                if np.all(t < 0.1):
                    if population[s1].bestfit <= population[s2].bestfit:
                        reinit_swarms.add(s1)
                    else:
                        reinit_swarms.add(s2)

        return reinit_swarms

    def give_converged_swarms(self, population, conv_factr, converged_bests=[]):
        """ Returns the number of converged swarms and the worst swarm index """
        not_converged = 0
        worst_swarm_idx = None
        worst_swarm = None
        for i, swarm in enumerate(population):
            std = np.std([ind.fitness.values for ind in swarm])
            if std > conv_factr:
                not_converged += 1
                if worst_swarm is None or swarm.bestfit < worst_swarm.bestfit:
                    worst_swarm_idx = i
                    worst_swarm = swarm
            else:
                converged_bests.append(swarm.best)

        converged_bests.sort(key=(lambda i: i.fitness))
        return (
         not_converged, worst_swarm_idx, converged_bests)


class MPSOAlgorithm(RefineAsyncHelper):
    __doc__ = '\n        Multi-particle-swarm optimization method adapted from the examples found\n        in the DEAP project. Employs a T-test (two independent sample lists) to\n        differentiate between swarms instead of the diameter and average of the\n        swarms. Seemed to work better for scaled parameters (YMMV).\n        \n        Implementation of the Multiswarm Particle Swarm Optimization algorithm as\n        presented in *Blackwell, Branke, and Li, 2008, Particle Swarms for Dynamic\n        Optimization Problems.*\n    '
    gen = -1
    converged_bests = None

    def __init__(self, toolbox, bounds, norms, ngen=NGEN, nswarms=NSWARMS, nexcess=NEXCESS, nparticles=NPARTICLES, conv_factr=CONV_FACTR, stats=None, halloffame=None, verbose=True, refiner=None, stop=None):
        """
            TODO
        """
        self.converged_bests = []
        self.toolbox = toolbox
        self.bounds = bounds
        self.norms = norms
        self.ngen = ngen
        self.nswarms = nswarms
        self.nexcess = nexcess
        self.nparticles = nparticles
        self.conv_factr = conv_factr
        self.stats = stats
        self.halloffame = halloffame
        self.verbose = verbose
        self.refiner = refiner
        self._stop = stop

    def _evaluate_swarms(self, population):

        def give_unevaluated_particles():
            for p in (itertools.chain)(*population):
                if p.fitness.valid:
                    continue
                else:
                    yield p

        self.do_async_evaluation(iter_func=give_unevaluated_particles, result_func=result_func)
        for swarm in population:
            for part in swarm:
                self.toolbox.update_swarm(swarm, part)

        return population

    def _create_and_evaluate_swarm(self):
        """ Helper function that creates, evaluates and returns a new swarm """
        particles = self.do_async_evaluation(iter_func=(self.toolbox.generate_particles), result_func=result_func)
        return self.toolbox.swarm(particles)

    def _create_and_evaluate_population(self):
        """ Helper function that creates, evaluates and returns a population of swarms """
        population = [self._create_and_evaluate_swarm() for _ in range(self.nswarms)]
        if self.halloffame is not None:
            self.halloffame.update((itertools.chain)(*population))
        return population

    def run(self):
        """Will run this algorithm"""
        self._setup_logging()
        population = []
        for _ in range(self.ngen):
            if self._user_cancelled():
                logger.info('User cancelled execution of PCMA-ES, stopping ...')
                break
            population = self._ask(population)
            self._record(population)
            if self._is_stagnating():
                break
            self._tell(population)

        return (
         self.refiner.history.best_solution,
         list((itertools.chain)(*population)),
         self.converged_bests)

    def _ask(self, population):
        """
            Calculates how many swarms have converged, and keeps track of the
            worst swarm. If all swarms have converged, it will add a new swarm.
            If too many swarms are roaming, it will remove the worst.
        """
        self.gen += 1
        self.refiner.status.message = 'Creating generation #%d' % (self.gen + 1)
        if not population:
            population = self._create_and_evaluate_population()
        else:
            reinit_swarms = self.toolbox.give_reinit_swarms(population)
            for sindex in reinit_swarms:
                population[sindex] = self._create_and_evaluate_swarm()

        not_converged, worst_swarm_idx, self.converged_bests = self.toolbox.give_converged_swarms(population, self.conv_factr, self.converged_bests)
        if not_converged == 0:
            population.append(self._create_and_evaluate_swarm())
        else:
            if not_converged > self.nexcess:
                population.pop(worst_swarm_idx)
        return population

    def _tell(self, population):
        for swarm in population:
            for part in swarm:
                if swarm.best is not None and part.best is not None:
                    self.toolbox.update_particle(part, swarm.best)

        self._evaluate_swarms(population)
        self.halloffame.update((itertools.chain)(*population))

    def _is_stagnating(self):
        return False

    def _setup_logging(self):
        if self.verbose:
            column_names = [
             'gen', 'nswarm', 'indiv']
            if self.stats is not None:
                column_names += list(self.stats.functions.keys())
            self.logbook = tools.Logbook()
            self.logbook.header = column_names

    def _record(self, population):
        pop_size = len(population)
        best = self.halloffame.get_best()
        best_f = best.fitness.values[0]
        pop = list((itertools.chain)(*population))
        record = self.stats.compile(pop)
        if self.verbose:
            (self.logbook.record)(gen=self.gen, nswarm=pop_size, indiv=len(pop), **record)
            print(self.logbook.stream)
        self.refiner.update(best, iteration=(self.gen), residual=best_f)


class RefineMPSORun(RefineMethod):
    __doc__ = '\n        The DEAP MPSO algorithm implementation\n    '
    name = 'MPSO refinement'
    description = 'This algorithm uses the MPSO refinement strategy'
    index = 2
    disabled = False
    ngen = RefineMethodOption('Maximum # of generations', NGEN, [1, 1000], int)
    nswarms = RefineMethodOption('Start # of swarms', NSWARMS, [1, 50], int)
    nexcess = RefineMethodOption('Max # of unconverged swarms', NEXCESS, [1, 50], int)
    nparticles = RefineMethodOption('Swarm size', NPARTICLES, [1, 50], int)
    conv_factr = RefineMethodOption('Convergence tolerance', CONV_FACTR, [0.0, 10.0], float)

    def _individual_creator(self, context, bounds):
        creator.create('Particle',
          pyxrd_array, fitness=FitnessMin,
          speed=list,
          best=None,
          bestfit=FitnessMin,
          context=context,
          min_bounds=(bounds[:, 0]),
          max_bounds=(bounds[:, 1]))
        creator.create('Swarm', list, best=None, bestfit=FitnessMin)

    def _create_stats(self):
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register('avg', (np.mean), axis=0)
        stats.register('std', (np.std), axis=0)
        stats.register('min', (np.min), axis=0)
        stats.register('max', (np.max), axis=0)
        return stats

    def run(self, refiner, ngen=NGEN, nswarms=NSWARMS, nexcess=NEXCESS, conv_factr=CONV_FACTR, nparticles=NPARTICLES, **kwargs):
        logger.info('Setting up the DEAP MPSO refinement algorithm')
        ndim = len(refiner.refinables)
        bounds = np.array(refiner.ranges)
        norms = np.abs(bounds[:, 1] - bounds[:, 0])
        self._individual_creator(refiner, bounds)
        strategy = MultiPSOStrategy()
        logger.info('Creating hall-off-fame and statistics')
        halloffame = PyXRDParetoFront(similar=(lambda a1, a2: np.all(a1 == a2)))
        stats = self._create_stats()
        toolbox = base.Toolbox()
        toolbox.register('particle',
          (strategy.generate_particle), (creator.Particle), dim=ndim,
          pmin=(bounds[:, 0]),
          pmax=(bounds[:, 1]),
          smin=(-norms / 2.0),
          smax=(norms / 2.0))
        toolbox.register('update_particle', (strategy.update_particle), chi=0.729843788, c=(norms / np.amax(norms)))
        toolbox.register('generate_particles', (strategy.generate_particles), (toolbox.particle), n=NPARTICLES)
        toolbox.register('swarm', strategy.create_swarm, creator.Swarm)
        toolbox.register('update_swarm', strategy.update_swarm)
        toolbox.register('give_reinit_swarms', strategy.give_reinit_swarms)
        toolbox.register('give_converged_swarms', strategy.give_converged_swarms)
        algorithm = MPSOAlgorithm(
 toolbox, bounds, norms,
 ngen, nswarms, nexcess, nparticles, conv_factr, stats=stats, 
         halloffame=halloffame, refiner=refiner, 
         stop=self._stop, **kwargs)
        logger.info('Running the MPSO algorithm...')
        best, population, converged_bests = algorithm.run()
        return (
         best, population, converged_bests)