# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lsga/engine.py
# Compiled at: 2019-02-10 14:34:46
# Size of source mod 2**32: 13994 bytes
""" Genetic Algorithm engine definition
"""
import logging, math
from functools import wraps
import cProfile, pstats, os
from .components import IndividualBase, Population
from .plugin_interfaces.operators import Selection, Crossover, Mutation
from .plugin_interfaces.analysis import OnTheFlyAnalysis
from .mpiutil import MPIUtil
mpi = MPIUtil()

def do_profile(filename, sortby='tottime'):
    """ Constructor for function profiling decorator.
    """

    def _do_profile(func):

        @wraps(func)
        def profiled_func(*args, **kwargs):
            DO_PROF = os.getenv('PROFILING')
            if DO_PROF:
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                ps = pstats.Stats(profile).sort_stats(sortby)
                ps.dump_stats(filename)
            else:
                result = func(*args, **kwargs)
            return result

        return profiled_func

    return _do_profile


class StatVar(object):

    def __init__(self, name):
        """ Descriptor for statistical variables which need to be memoized when
        engine running.
        """
        self.name = '_{}'.format(name)

    def __get__(self, engine, cls):
        """
        Getter.
        """
        stat_var = getattr(engine, self.name)
        if stat_var is None:
            if 'min' in self.name:
                if 'ori' in self.name:
                    stat_var = engine.population.min(engine.ori_fitness)
            else:
                if 'min' in self.name:
                    stat_var = engine.population.min(engine.fitness)
                elif 'max' in self.name and 'ori' in self.name:
                    stat_var = engine.population.max(engine.ori_fitness)
                else:
                    if 'max' in self.name:
                        stat_var = engine.population.max(engine.fitness)
                    else:
                        if 'mean' in self.name and 'ori' in self.name:
                            stat_var = engine.population.mean(engine.ori_fitness)
            if 'mean' in self.name:
                stat_var = engine.population.mean(engine.fitness)
            setattr(engine, self.name, stat_var)
        return stat_var

    def __set__(self, engine, value):
        """
        Setter.
        """
        setattr(engine, self.name, value)


class GAEngine(object):
    __doc__ = ' Class for representing a Genetic Algorithm engine. The class is the \n    central object in GAFT framework for running a genetic algorithm optimization.\n    Once the population with individuals,  a set of genetic operators and fitness \n    function are setup, the engine object unites these informations and provide \n    means for running a genetic algorthm optimization.\n\n    :param population: The Population to be reproduced in evolution iteration.\n    :type population: :obj:`lsga.components.Population`\n\n    :param selection: The Selection to be used for individual seleciton.\n    :type selection: :obj:`lsga.plugin_interfaces.operators.Selection`\n\n    :param crossover: The Crossover to be used for individual crossover.\n    :type crossover: :obj:`lsga.plugin_interfaces.operators.Crossover`\n\n    :param mutation: The Mutation to be used for individual mutation.\n    :type mutation: :obj:`lsga.plugin_interfaces.operators.Mutation`\n\n    :param fitness: The fitness calculation function for an individual in population.\n    :type fitness: function\n\n    :param analysis: All analysis class for on-the-fly analysis.\n    :type analysis: :obj:`OnTheFlyAnalysis` list\n    '
    fmax, fmin, fmean = StatVar('fmax'), StatVar('fmin'), StatVar('fmean')
    ori_fmax, ori_fmin, ori_fmean = StatVar('ori_fmax'), StatVar('ori_fmin'), StatVar('ori_fmean')

    def __init__(self, population, selection, crossover, mutation, fitness=None, analysis=None):
        logger_name = 'lsga.{}'.format(self.__class__.__name__)
        self.logger = logging.getLogger(logger_name)
        self.population = population
        self.fitness = fitness
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.analysis = [] if analysis is None else [a() for a in analysis]
        self._fmax, self._fmin, self._fmean = (None, None, None)
        self._ori_fmax, self._ori_fmin, self._ori_fmean = (None, None, None)
        self.ori_fitness = None if self.fitness is None else self.fitness
        self.current_generation = -1
        self._check_parameters()

    @do_profile(filename='gaft_run.prof')
    def run(self, ng=10):
        """ Run the Genetic Algorithm optimization iteration with specified parameters.

        :param ng: Evolution iteration steps (generation number)
        :type ng: int
        """
        if self.fitness is None:
            raise AttributeError('No fitness function in GA engine')
        self._update_statvars()
        for a in self.analysis:
            a.setup(ng=ng, engine=self)

        try:
            try:
                for g in range(ng):
                    self.current_generation = g
                    if mpi.is_master:
                        best_indv = self.population.best_indv(self.fitness)
                    else:
                        best_indv = None
                    best_indv = mpi.bcast(best_indv)
                    local_indvs = []
                    local_size = mpi.split_size(self.population.size // 2)
                    for _ in range(local_size):
                        parents = self.selection.select((self.population), fitness=(self.fitness))
                        children = (self.crossover.cross)(*parents)
                        children = [self.mutation.mutate(child, self) for child in children]
                        local_indvs.extend(children)

                    indvs = mpi.merge_seq(local_indvs)
                    indvs[0] = best_indv
                    self.population.individuals = indvs
                    self._update_statvars()
                    for a in self.analysis:
                        if g % a.interval == 0:
                            a.register_step(g=g, population=(self.population), engine=self)

            except Exception as e:
                if mpi.is_master:
                    msg = '{} exception is catched'.format(type(e).__name__)
                    self.logger.exception(msg)
                raise e

        finally:
            self.current_generation = -1
            for a in self.analysis:
                a.finalize(population=(self.population), engine=self)

    def _update_statvars(self):
        """
        Private helper function to update statistic variables in GA engine, like
        maximum, minimum and mean values.
        """
        self.ori_fmax = self.population.max(self.ori_fitness)
        self.ori_fmin = self.population.min(self.ori_fitness)
        self.ori_fmean = self.population.mean(self.ori_fitness)
        self.fmax = self.population.max(self.fitness)
        self.fmin = self.population.min(self.fitness)
        self.fmean = self.population.mean(self.fitness)

    def _check_parameters(self):
        """
        Helper function to check parameters of engine.
        """
        if not isinstance(self.population, Population):
            raise TypeError('population must be a Population object')
        else:
            if not isinstance(self.selection, Selection):
                raise TypeError('selection operator must be a Selection instance')
            if not isinstance(self.crossover, Crossover):
                raise TypeError('crossover operator must be a Crossover instance')
            raise isinstance(self.mutation, Mutation) or TypeError('mutation operator must be a Mutation instance')
        for ap in self.analysis:
            if not isinstance(ap, OnTheFlyAnalysis):
                msg = '{} is not subclass of OnTheFlyAnalysis'.format(ap.__name__)
                raise TypeError(msg)

    def fitness_register(self, fn):
        """ A decorator for fitness function register.

        :param fn: Fitness function to be registered
        :type fn: function
        """

        @wraps(fn)
        def _fn_with_fitness_check(indv):
            if not isinstance(indv, IndividualBase):
                raise TypeError("indv's class must be subclass of IndividualBase")
            fitness = fn(indv)
            is_invalid = type(fitness) is not float or math.isnan(fitness)
            if is_invalid:
                msg = 'Fitness value(value: {}, type: {}) is invalid'
                msg = msg.format(fitness, type(fitness))
                raise ValueError(msg)
            return fitness

        self.fitness = _fn_with_fitness_check
        if self.ori_fitness is None:
            self.ori_fitness = _fn_with_fitness_check

    def analysis_register(self, analysis_cls):
        """ A decorator for analysis regsiter.

        :param analysis_cls: The analysis to be registered
        :type analysis_cls: :obj:`lsga.plugin_interfaces.OnTheFlyAnalysis`
        """
        if not issubclass(analysis_cls, OnTheFlyAnalysis):
            raise TypeError('analysis class must be subclass of OnTheFlyAnalysis')
        analysis = analysis_cls()
        self.analysis.append(analysis)

    def linear_scaling(self, target='max', ksi=0.5):
        r"""
        A decorator constructor for fitness function linear scaling.

        :param target: The optimization target, maximization or minimization,
                       possible value: 'max', 'min'
        :type target: str

        :param ksi: Selective pressure adjustment value.
        :type ksi: float

        .. Note::

            Linear Scaling:
                1. :math:`arg \max f(x)`, then the scaled fitness would be :math:`f - \min f(x) + {\xi}`
                2. :math:`arg \min f(x)`, then the scaled fitness would be :math:`\max f(x) - f(x) + {\xi}`

        """

        def _linear_scaling(fn):
            self.ori_fitness = fn

            @wraps(fn)
            def _fn_with_linear_scaling(indv):
                f = fn(indv)
                if target == 'max':
                    f_prime = f - self.ori_fmin + ksi
                else:
                    if target == 'min':
                        f_prime = self.ori_fmax - f + ksi
                    else:
                        raise ValueError('Invalid target type({})'.format(target))
                return f_prime

            return _fn_with_linear_scaling

        return _linear_scaling

    def dynamic_linear_scaling(self, target='max', ksi0=2, r=0.9):
        r"""
        A decorator constructor for fitness dynamic linear scaling.

        :param target: The optimization target, maximization or minimization
                       possible value: 'min' or 'max'
        :type target: str

        :param ksi0: Initial selective pressure adjustment value, default value is 2
        :type ksi0: float

        :param r: The reduction factor for selective pressure adjustment value,
                  ksi^(k-1)*r is the adjustment value for generation k, default
                  value is 0.9
        :type r: float in range [0.9, 0.999]

        .. Note::
            Dynamic Linear Scaling:

            For maximizaiton, :math:`f' = f(x) - \min f(x) + {\xi}^{k}`, :math:`k` is generation number.
        """

        def _dynamic_linear_scaling(fn):
            self.ori_fitness = fn

            @wraps(fn)
            def _fn_with_dynamic_linear_scaling(indv):
                f = fn(indv)
                k = self.current_generation + 1
                if target == 'max':
                    f_prime = f - self.ori_fmin + ksi0 * r ** k
                else:
                    if target == 'min':
                        f_prime = self.ori_fmax - f + ksi0 * r ** k
                    else:
                        raise ValueError('Invalid target type({})'.format(target))
                return f_prime

            return _fn_with_dynamic_linear_scaling

        return _dynamic_linear_scaling

    def minimize(self, fn):
        """ A decorator for minimizing the fitness function.

        :param fn: Original fitness function
        :type fn: function
        """

        @wraps(fn)
        def _minimize(indv):
            return -fn(indv)

        return _minimize