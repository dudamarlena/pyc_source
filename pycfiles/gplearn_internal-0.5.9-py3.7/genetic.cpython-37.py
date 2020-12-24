# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/gplearn/genetic.py
# Compiled at: 2020-04-02 03:45:04
# Size of source mod 2**32: 65915 bytes
"""Genetic Programming in Python, with a scikit-learn inspired API

The :mod:`gplearn.genetic` module implements Genetic Programming. These
are supervised learning methods based on applying evolutionary operations on
computer programs.
"""
import itertools
from abc import ABCMeta, abstractmethod
from time import time
from warnings import warn
import numpy as np
from joblib import Parallel, delayed
from scipy.stats import rankdata
from sklearn.base import BaseEstimator
from sklearn.base import RegressorMixin, TransformerMixin, ClassifierMixin
from sklearn.exceptions import NotFittedError
from sklearn.utils import compute_sample_weight
from sklearn.utils.validation import check_X_y, check_array
from sklearn.utils.multiclass import check_classification_targets
from ._program import _Program
from .fitness import _fitness_map, _Fitness
from .functions import _function_map, _Function, sig1 as sigmoid
from .utils import _partition_estimators
from .utils import check_random_state
__all__ = [
 'SymbolicRegressor', 'SymbolicClassifier', 'SymbolicTransformer']
MAX_INT = np.iinfo(np.int32).max

def _parallel_evolve(n_programs, parents, X, y, sample_weight, seeds, params):
    """Private function used to build a batch of programs within a job."""
    n_samples, n_features = X.shape
    tournament_size = params['tournament_size']
    function_set = params['function_set']
    arities = params['arities']
    init_depth = params['init_depth']
    init_method = params['init_method']
    const_range = params['const_range']
    metric = params['_metric']
    transformer = params['_transformer']
    parsimony_coefficient = params['parsimony_coefficient']
    method_probs = params['method_probs']
    p_point_replace = params['p_point_replace']
    max_samples = params['max_samples']
    feature_names = params['feature_names']
    max_samples = int(max_samples * n_samples)

    def _tournament():
        contenders = random_state.randint(0, len(parents), tournament_size)
        fitness = [parents[p].fitness_ for p in contenders]
        if metric.greater_is_better:
            parent_index = contenders[np.argmax(fitness)]
        else:
            parent_index = contenders[np.argmin(fitness)]
        return (
         parents[parent_index], parent_index)

    programs = []
    for i in range(n_programs):
        random_state = check_random_state(seeds[i])
        if parents is None:
            program = None
            genome = None
        else:
            method = random_state.uniform()
            parent, parent_index = _tournament()
            if method < method_probs[0]:
                donor, donor_index = _tournament()
                program, removed, remains = parent.crossover(donor.program, random_state)
                genome = {'method':'Crossover',  'parent_idx':parent_index, 
                 'parent_nodes':removed, 
                 'donor_idx':donor_index, 
                 'donor_nodes':remains}
            else:
                if method < method_probs[1]:
                    program, removed, _ = parent.subtree_mutation(random_state)
                    genome = {'method':'Subtree Mutation',  'parent_idx':parent_index, 
                     'parent_nodes':removed}
                else:
                    if method < method_probs[2]:
                        program, removed = parent.hoist_mutation(random_state)
                        genome = {'method':'Hoist Mutation',  'parent_idx':parent_index, 
                         'parent_nodes':removed}
                    else:
                        if method < method_probs[3]:
                            program, mutated = parent.point_mutation(random_state)
                            genome = {'method':'Point Mutation',  'parent_idx':parent_index, 
                             'parent_nodes':mutated}
                        else:
                            program = parent.reproduce()
                            genome = {'method':'Reproduction',  'parent_idx':parent_index, 
                             'parent_nodes':[]}
        program = _Program(function_set=function_set, arities=arities,
          init_depth=init_depth,
          init_method=init_method,
          n_features=n_features,
          metric=metric,
          transformer=transformer,
          const_range=const_range,
          p_point_replace=p_point_replace,
          parsimony_coefficient=parsimony_coefficient,
          feature_names=feature_names,
          random_state=random_state,
          program=program)
        program.parents = genome
        if sample_weight is None:
            curr_sample_weight = np.ones((n_samples,))
        else:
            curr_sample_weight = sample_weight.copy()
        oob_sample_weight = curr_sample_weight.copy()
        indices, not_indices = program.get_all_indices(n_samples, max_samples, random_state)
        curr_sample_weight[not_indices] = 0
        oob_sample_weight[indices] = 0
        program.raw_fitness_ = program.raw_fitness(X, y, curr_sample_weight)
        if max_samples < n_samples:
            program.oob_fitness_ = program.raw_fitness(X, y, oob_sample_weight)
        programs.append(program)

    return programs


class BaseSymbolic(BaseEstimator, metaclass=ABCMeta):
    __doc__ = 'Base class for symbolic regression / classification estimators.\n\n    Warning: This class should not be used directly.\n    Use derived classes instead.\n\n    '

    @abstractmethod
    def __init__(self, population_size=1000, hall_of_fame=None, n_components=None, generations=20, tournament_size=20, stopping_criteria=0.0, const_range=(-1.0, 1.0), init_depth=(2, 6), init_method='half and half', function_set=('add', 'sub', 'mul', 'div'), transformer=None, metric='mean absolute error', parsimony_coefficient=0.001, p_crossover=0.9, p_subtree_mutation=0.01, p_hoist_mutation=0.01, p_point_mutation=0.01, p_point_replace=0.05, max_samples=1.0, class_weight=None, feature_names=None, warm_start=False, low_memory=False, n_jobs=1, verbose=0, random_state=None):
        self.population_size = population_size
        self.hall_of_fame = hall_of_fame
        self.n_components = n_components
        self.generations = generations
        self.tournament_size = tournament_size
        self.stopping_criteria = stopping_criteria
        self.const_range = const_range
        self.init_depth = init_depth
        self.init_method = init_method
        self.function_set = function_set
        self.transformer = transformer
        self.metric = metric
        self.parsimony_coefficient = parsimony_coefficient
        self.p_crossover = p_crossover
        self.p_subtree_mutation = p_subtree_mutation
        self.p_hoist_mutation = p_hoist_mutation
        self.p_point_mutation = p_point_mutation
        self.p_point_replace = p_point_replace
        self.max_samples = max_samples
        self.class_weight = class_weight
        self.feature_names = feature_names
        self.warm_start = warm_start
        self.low_memory = low_memory
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.random_state = random_state

    def _verbose_reporter(self, run_details=None):
        """A report of the progress of the evolution process.

        Parameters
        ----------
        run_details : dict
            Information about the evolution.

        """
        if run_details is None:
            print('    |{:^25}|{:^42}|'.format('Population Average', 'Best Individual'))
            print('---- ------------------------- ------------------------------------------ ----------')
            line_format = '{:>4} {:>8} {:>16} {:>8} {:>16} {:>16} {:>10}'
            print(line_format.format('Gen', 'Length', 'Fitness', 'Length', 'Fitness', 'OOB Fitness', 'Time Left'))
        else:
            gen = run_details['generation'][(-1)]
            generation_time = run_details['generation_time'][(-1)]
            remaining_time = (self.generations - gen - 1) * generation_time
            if remaining_time > 60:
                remaining_time = '{0:.2f}m'.format(remaining_time / 60.0)
            else:
                remaining_time = '{0:.2f}s'.format(remaining_time)
            oob_fitness = 'N/A'
            line_format = '{:4d} {:8.2f} {:16g} {:8d} {:16g} {:>16} {:>10}'
            if self.max_samples < 1.0:
                oob_fitness = run_details['best_oob_fitness'][(-1)]
                line_format = '{:4d} {:8.2f} {:16g} {:8d} {:16g} {:16g} {:>10}'
            print(line_format.format(run_details['generation'][(-1)], run_details['average_length'][(-1)], run_details['average_fitness'][(-1)], run_details['best_length'][(-1)], run_details['best_fitness'][(-1)], oob_fitness, remaining_time))

    def fit(self, X, y, sample_weight=None):
        """Fit the Genetic Program according to X, y.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.

        y : array-like, shape = [n_samples]
            Target values.

        sample_weight : array-like, shape = [n_samples], optional
            Weights applied to individual samples.

        Returns
        -------
        self : object
            Returns self.

        """
        random_state = check_random_state(self.random_state)
        if sample_weight is not None:
            sample_weight = check_array(sample_weight, ensure_2d=False)
        elif isinstance(self, ClassifierMixin):
            X, y = check_X_y(X, y, y_numeric=False)
            check_classification_targets(y)
            if self.class_weight:
                if sample_weight is None:
                    sample_weight = 1.0
                sample_weight = sample_weight * compute_sample_weight(self.class_weight, y)
            self.classes_, y = np.unique(y, return_inverse=True)
            n_trim_classes = np.count_nonzero(np.bincount(y, sample_weight))
            if n_trim_classes != 2:
                raise ValueError('y contains %d class after sample_weight trimmed classes with zero weights, while 2 classes are required.' % n_trim_classes)
            self.n_classes_ = len(self.classes_)
        else:
            X, y = check_X_y(X, y, y_numeric=True)
        _, self.n_features_ = X.shape
        hall_of_fame = self.hall_of_fame
        if hall_of_fame is None:
            hall_of_fame = self.population_size
        if hall_of_fame > self.population_size or hall_of_fame < 1:
            raise ValueError('hall_of_fame (%d) must be less than or equal to population_size (%d).' % (
             self.hall_of_fame,
             self.population_size))
        n_components = self.n_components
        if n_components is None:
            n_components = hall_of_fame
        if n_components > hall_of_fame or n_components < 1:
            raise ValueError('n_components (%d) must be less than or equal to hall_of_fame (%d).' % (
             self.n_components,
             self.hall_of_fame))
        self._function_set = []
        for function in self.function_set:
            if isinstance(function, str):
                if function not in _function_map:
                    raise ValueError('invalid function name %s found in `function_set`.' % function)
                self._function_set.append(_function_map[function])
            elif isinstance(function, _Function):
                self._function_set.append(function)
            else:
                raise ValueError('invalid type %s found in `function_set`.' % type(function))

        if not self._function_set:
            raise ValueError('No valid functions found in `function_set`.')
        self._arities = {}
        for function in self._function_set:
            arity = function.arity
            self._arities[arity] = self._arities.get(arity, [])
            self._arities[arity].append(function)

        if isinstance(self.metric, _Fitness):
            self._metric = self.metric
        else:
            if isinstance(self, RegressorMixin):
                if self.metric not in ('mean absolute error', 'mse', 'rmse', 'pearson',
                                       'spearman'):
                    raise ValueError('Unsupported metric: %s' % self.metric)
                self._metric = _fitness_map[self.metric]
            else:
                if isinstance(self, ClassifierMixin):
                    if self.metric != 'log loss':
                        raise ValueError('Unsupported metric: %s' % self.metric)
                    self._metric = _fitness_map[self.metric]
                else:
                    if isinstance(self, TransformerMixin):
                        if self.metric not in ('pearson', 'spearman'):
                            raise ValueError('Unsupported metric: %s' % self.metric)
                        self._metric = _fitness_map[self.metric]
                    else:
                        self._method_probs = np.array([self.p_crossover,
                         self.p_subtree_mutation,
                         self.p_hoist_mutation,
                         self.p_point_mutation])
                        self._method_probs = np.cumsum(self._method_probs)
                        if self._method_probs[(-1)] > 1:
                            raise ValueError('The sum of p_crossover, p_subtree_mutation, p_hoist_mutation and p_point_mutation should total to 1.0 or less.')
                        if self.init_method not in ('half and half', 'grow', 'full'):
                            raise ValueError('Valid program initializations methods include "grow", "full" and "half and half". Given %s.' % self.init_method)
                        if not (isinstance(self.const_range, tuple) and len(self.const_range) == 2):
                            if not self.const_range is None:
                                raise ValueError('const_range should be a tuple with length two, or None.')
                            if not isinstance(self.init_depth, tuple) or len(self.init_depth) != 2:
                                raise ValueError('init_depth should be a tuple with length two.')
                            if self.init_depth[0] > self.init_depth[1]:
                                raise ValueError('init_depth should be in increasing numerical order: (min_depth, max_depth).')
                        if self.feature_names is not None:
                            if self.n_features_ != len(self.feature_names):
                                raise ValueError('The supplied `feature_names` has different length to n_features. Expected %d, got %d.' % (
                                 self.n_features_, len(self.feature_names)))
                            for feature_name in self.feature_names:
                                if not isinstance(feature_name, str):
                                    raise ValueError('invalid type %s found in `feature_names`.' % type(feature_name))

                        elif self.transformer is not None:
                            if isinstance(self.transformer, _Function):
                                self._transformer = self.transformer
                            else:
                                if self.transformer == 'sigmoid':
                                    self._transformer = sigmoid
                                else:
                                    raise ValueError('Invalid `transformer`. Expected either "sigmoid" or _Function object, got %s' % type(self.transformer))
                            if self._transformer.arity != 1:
                                raise ValueError('Invalid arity for `transformer`. Expected 1, got %d.' % self._transformer.arity)
                            params = self.get_params()
                            params['_metric'] = self._metric
                            if hasattr(self, '_transformer'):
                                params['_transformer'] = self._transformer
                        else:
                            params['_transformer'] = None
                        params['function_set'] = self._function_set
                        params['arities'] = self._arities
                        params['method_probs'] = self._method_probs
                        self._programs = self.warm_start and hasattr(self, '_programs') or []
                        self.run_details_ = {'generation':[],  'average_length':[],  'average_fitness':[],  'best_length':[],  'best_fitness':[],  'best_oob_fitness':[],  'generation_time':[]}
                    prior_generations = len(self._programs)
                    n_more_generations = self.generations - prior_generations
        if n_more_generations < 0:
            raise ValueError('generations=%d must be larger or equal to len(_programs)=%d when warm_start==True' % (
             self.generations, len(self._programs)))
        else:
            if n_more_generations == 0:
                fitness = [program.raw_fitness_ for program in self._programs[(-1)]]
                warn('Warm-start fitting without increasing n_estimators does not fit new programs.')
            elif self.warm_start:
                for i in range(len(self._programs)):
                    _ = random_state.randint(MAX_INT, size=(self.population_size))

            else:
                if self.verbose:
                    self._verbose_reporter()
                for gen in range(prior_generations, self.generations):
                    start_time = time()
                    if gen == 0:
                        parents = None
                    else:
                        parents = self._programs[(gen - 1)]
                    n_jobs, n_programs, starts = _partition_estimators(self.population_size, self.n_jobs)
                    seeds = random_state.randint(MAX_INT, size=(self.population_size))
                    population = Parallel(n_jobs=n_jobs, verbose=(int(self.verbose > 1)))((delayed(_parallel_evolve)(n_programs[i], parents, X, y, sample_weight, seeds[starts[i]:starts[(i + 1)]], params) for i in range(n_jobs)))
                    population = list(itertools.chain.from_iterable(population))
                    fitness = [program.raw_fitness_ for program in population]
                    length = [program.length_ for program in population]
                    parsimony_coefficient = None
                    if self.parsimony_coefficient == 'auto':
                        parsimony_coefficient = np.cov(length, fitness)[(1, 0)] / np.var(length)
                    else:
                        for program in population:
                            program.fitness_ = program.fitness(parsimony_coefficient)

                        self._programs.append(population)
                        if not self.low_memory:
                            for old_gen in np.arange(gen, 0, -1):
                                indices = []
                                for program in self._programs[old_gen]:
                                    if program is not None:
                                        for idx in program.parents:
                                            if 'idx' in idx:
                                                indices.append(program.parents[idx])

                                indices = set(indices)
                                for idx in range(self.population_size):
                                    if idx not in indices:
                                        self._programs[(old_gen - 1)][idx] = None

                        else:
                            if gen > 0:
                                self._programs[gen - 1] = None
                        if self._metric.greater_is_better:
                            best_program = population[np.argmax(fitness)]
                        else:
                            best_program = population[np.argmin(fitness)]
                    self.run_details_['generation'].append(gen)
                    self.run_details_['average_length'].append(np.mean(length))
                    self.run_details_['average_fitness'].append(np.mean(fitness))
                    self.run_details_['best_length'].append(best_program.length_)
                    self.run_details_['best_fitness'].append(best_program.raw_fitness_)
                    oob_fitness = np.nan
                    if self.max_samples < 1.0:
                        oob_fitness = best_program.oob_fitness_
                    self.run_details_['best_oob_fitness'].append(oob_fitness)
                    generation_time = time() - start_time
                    self.run_details_['generation_time'].append(generation_time)
                    if self.verbose:
                        self._verbose_reporter(self.run_details_)
                    if self._metric.greater_is_better:
                        best_fitness = fitness[np.argmax(fitness)]
                        if best_fitness >= self.stopping_criteria:
                            break
                        else:
                            best_fitness = fitness[np.argmin(fitness)]
                            if best_fitness <= self.stopping_criteria:
                                break

                if isinstance(self, TransformerMixin):
                    fitness = np.array(fitness)
                    if self._metric.greater_is_better:
                        hall_of_fame = fitness.argsort()[::-1][:self.hall_of_fame]
                    else:
                        hall_of_fame = fitness.argsort()[:self.hall_of_fame]
                    evaluation = np.array([gp.execute(X) for gp in [self._programs[(-1)][i] for i in hall_of_fame]])
                    if self.metric == 'spearman':
                        evaluation = np.apply_along_axis(rankdata, 1, evaluation)
                    with np.errstate(divide='ignore', invalid='ignore'):
                        correlations = np.abs(np.corrcoef(evaluation))
                    np.fill_diagonal(correlations, 0.0)
                    components = list(range(self.hall_of_fame))
                    indices = list(range(self.hall_of_fame))
                    while len(components) > self.n_components:
                        most_correlated = np.unravel_index(np.argmax(correlations), correlations.shape)
                        worst = max(most_correlated)
                        components.pop(worst)
                        indices.remove(worst)
                        correlations = correlations[:, indices][indices, :]
                        indices = list(range(len(components)))

                    self._best_programs = [self._programs[(-1)][i] for i in hall_of_fame[components]]
                else:
                    if self._metric.greater_is_better:
                        self._program = self._programs[(-1)][np.argmax(fitness)]
                    else:
                        self._program = self._programs[(-1)][np.argmin(fitness)]
            return self


class SymbolicRegressor(BaseSymbolic, RegressorMixin):
    __doc__ = 'A Genetic Programming symbolic regressor.\n\n    A symbolic regressor is an estimator that begins by building a population\n    of naive random formulas to represent a relationship. The formulas are\n    represented as tree-like structures with mathematical functions being\n    recursively applied to variables and constants. Each successive generation\n    of programs is then evolved from the one that came before it by selecting\n    the fittest individuals from the population to undergo genetic operations\n    such as crossover, mutation or reproduction.\n\n    Parameters\n    ----------\n    population_size : integer, optional (default=1000)\n        The number of programs in each generation.\n\n    generations : integer, optional (default=20)\n        The number of generations to evolve.\n\n    tournament_size : integer, optional (default=20)\n        The number of programs that will compete to become part of the next\n        generation.\n\n    stopping_criteria : float, optional (default=0.0)\n        The required metric value required in order to stop evolution early.\n\n    const_range : tuple of two floats, or None, optional (default=(-1., 1.))\n        The range of constants to include in the formulas. If None then no\n        constants will be included in the candidate programs.\n\n    init_depth : tuple of two ints, optional (default=(2, 6))\n        The range of tree depths for the initial population of naive formulas.\n        Individual trees will randomly choose a maximum depth from this range.\n        When combined with `init_method=\'half and half\'` this yields the well-\n        known \'ramped half and half\' initialization method.\n\n    init_method : str, optional (default=\'half and half\')\n        - \'grow\' : Nodes are chosen at random from both functions and\n          terminals, allowing for smaller trees than `init_depth` allows. Tends\n          to grow asymmetrical trees.\n        - \'full\' : Functions are chosen until the `init_depth` is reached, and\n          then terminals are selected. Tends to grow \'bushy\' trees.\n        - \'half and half\' : Trees are grown through a 50/50 mix of \'full\' and\n          \'grow\', making for a mix of tree shapes in the initial population.\n\n    function_set : iterable, optional (default=(\'add\', \'sub\', \'mul\', \'div\'))\n        The functions to use when building and evolving programs. This iterable\n        can include strings to indicate either individual functions as outlined\n        below, or you can also include your own functions as built using the\n        ``make_function`` factory from the ``functions`` module.\n\n        Available individual functions are:\n\n        - \'add\' : addition, arity=2.\n        - \'sub\' : subtraction, arity=2.\n        - \'mul\' : multiplication, arity=2.\n        - \'div\' : protected division where a denominator near-zero returns 1.,\n          arity=2.\n        - \'sqrt\' : protected square root where the absolute value of the\n          argument is used, arity=1.\n        - \'log\' : protected log where the absolute value of the argument is\n          used and a near-zero argument returns 0., arity=1.\n        - \'abs\' : absolute value, arity=1.\n        - \'neg\' : negative, arity=1.\n        - \'inv\' : protected inverse where a near-zero argument returns 0.,\n          arity=1.\n        - \'max\' : maximum, arity=2.\n        - \'min\' : minimum, arity=2.\n        - \'sin\' : sine (radians), arity=1.\n        - \'cos\' : cosine (radians), arity=1.\n        - \'tan\' : tangent (radians), arity=1.\n\n    metric : str, optional (default=\'mean absolute error\')\n        The name of the raw fitness metric. Available options include:\n\n        - \'mean absolute error\'.\n        - \'mse\' for mean squared error.\n        - \'rmse\' for root mean squared error.\n        - \'pearson\', for Pearson\'s product-moment correlation coefficient.\n        - \'spearman\' for Spearman\'s rank-order correlation coefficient.\n\n        Note that \'pearson\' and \'spearman\' will not directly predict the target\n        but could be useful as value-added features in a second-step estimator.\n        This would allow the user to generate one engineered feature at a time,\n        using the SymbolicTransformer would allow creation of multiple features\n        at once.\n\n    parsimony_coefficient : float or "auto", optional (default=0.001)\n        This constant penalizes large programs by adjusting their fitness to\n        be less favorable for selection. Larger values penalize the program\n        more which can control the phenomenon known as \'bloat\'. Bloat is when\n        evolution is increasing the size of programs without a significant\n        increase in fitness, which is costly for computation time and makes for\n        a less understandable final result. This parameter may need to be tuned\n        over successive runs.\n\n        If "auto" the parsimony coefficient is recalculated for each generation\n        using c = Cov(l,f)/Var( l), where Cov(l,f) is the covariance between\n        program size l and program fitness f in the population, and Var(l) is\n        the variance of program sizes.\n\n    p_crossover : float, optional (default=0.9)\n        The probability of performing crossover on a tournament winner.\n        Crossover takes the winner of a tournament and selects a random subtree\n        from it to be replaced. A second tournament is performed to find a\n        donor. The donor also has a subtree selected at random and this is\n        inserted into the original parent to form an offspring in the next\n        generation.\n\n    p_subtree_mutation : float, optional (default=0.01)\n        The probability of performing subtree mutation on a tournament winner.\n        Subtree mutation takes the winner of a tournament and selects a random\n        subtree from it to be replaced. A donor subtree is generated at random\n        and this is inserted into the original parent to form an offspring in\n        the next generation.\n\n    p_hoist_mutation : float, optional (default=0.01)\n        The probability of performing hoist mutation on a tournament winner.\n        Hoist mutation takes the winner of a tournament and selects a random\n        subtree from it. A random subtree of that subtree is then selected\n        and this is \'hoisted\' into the original subtrees location to form an\n        offspring in the next generation. This method helps to control bloat.\n\n    p_point_mutation : float, optional (default=0.01)\n        The probability of performing point mutation on a tournament winner.\n        Point mutation takes the winner of a tournament and selects random\n        nodes from it to be replaced. Terminals are replaced by other terminals\n        and functions are replaced by other functions that require the same\n        number of arguments as the original node. The resulting tree forms an\n        offspring in the next generation.\n\n        Note : The above genetic operation probabilities must sum to less than\n        one. The balance of probability is assigned to \'reproduction\', where a\n        tournament winner is cloned and enters the next generation unmodified.\n\n    p_point_replace : float, optional (default=0.05)\n        For point mutation only, the probability that any given node will be\n        mutated.\n\n    max_samples : float, optional (default=1.0)\n        The fraction of samples to draw from X to evaluate each program on.\n\n    feature_names : list, optional (default=None)\n        Optional list of feature names, used purely for representations in\n        the `print` operation or `export_graphviz`. If None, then X0, X1, etc\n        will be used for representations.\n\n    warm_start : bool, optional (default=False)\n        When set to ``True``, reuse the solution of the previous call to fit\n        and add more generations to the evolution, otherwise, just fit a new\n        evolution.\n\n    low_memory : bool, optional (default=False)\n        When set to ``True``, only the current generation is retained. Parent\n        information is discarded. For very large populations or runs with many\n        generations, this can result in substantial memory use reduction.\n\n    n_jobs : integer, optional (default=1)\n        The number of jobs to run in parallel for `fit`. If -1, then the number\n        of jobs is set to the number of cores.\n\n    verbose : int, optional (default=0)\n        Controls the verbosity of the evolution building process.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        If int, random_state is the seed used by the random number generator;\n        If RandomState instance, random_state is the random number generator;\n        If None, the random number generator is the RandomState instance used\n        by `np.random`.\n\n    Attributes\n    ----------\n    run_details_ : dict\n        Details of the evolution process. Includes the following elements:\n\n        - \'generation\' : The generation index.\n        - \'average_length\' : The average program length of the generation.\n        - \'average_fitness\' : The average program fitness of the generation.\n        - \'best_length\' : The length of the best program in the generation.\n        - \'best_fitness\' : The fitness of the best program in the generation.\n        - \'best_oob_fitness\' : The out of bag fitness of the best program in\n          the generation (requires `max_samples` < 1.0).\n        - \'generation_time\' : The time it took for the generation to evolve.\n\n    See Also\n    --------\n    SymbolicTransformer\n\n    References\n    ----------\n    .. [1] J. Koza, "Genetic Programming", 1992.\n\n    .. [2] R. Poli, et al. "A Field Guide to Genetic Programming", 2008.\n\n    '

    def __init__(self, population_size=1000, generations=20, tournament_size=20, stopping_criteria=0.0, const_range=(-1.0, 1.0), init_depth=(2, 6), init_method='half and half', function_set=('add', 'sub', 'mul', 'div'), metric='mean absolute error', parsimony_coefficient=0.001, p_crossover=0.9, p_subtree_mutation=0.01, p_hoist_mutation=0.01, p_point_mutation=0.01, p_point_replace=0.05, max_samples=1.0, feature_names=None, warm_start=False, low_memory=False, n_jobs=1, verbose=0, random_state=None):
        super(SymbolicRegressor, self).__init__(population_size=population_size,
          generations=generations,
          tournament_size=tournament_size,
          stopping_criteria=stopping_criteria,
          const_range=const_range,
          init_depth=init_depth,
          init_method=init_method,
          function_set=function_set,
          metric=metric,
          parsimony_coefficient=parsimony_coefficient,
          p_crossover=p_crossover,
          p_subtree_mutation=p_subtree_mutation,
          p_hoist_mutation=p_hoist_mutation,
          p_point_mutation=p_point_mutation,
          p_point_replace=p_point_replace,
          max_samples=max_samples,
          feature_names=feature_names,
          warm_start=warm_start,
          low_memory=low_memory,
          n_jobs=n_jobs,
          verbose=verbose,
          random_state=random_state)

    def __str__(self):
        """Overloads `print` output of the object to resemble a LISP tree."""
        if not hasattr(self, '_program'):
            return self.__repr__()
        return self._program.__str__()

    def predict(self, X):
        """Perform regression on test vectors X.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Input vectors, where n_samples is the number of samples
            and n_features is the number of features.

        Returns
        -------
        y : array, shape = [n_samples]
            Predicted values for X.

        """
        if not hasattr(self, '_program'):
            raise NotFittedError('SymbolicRegressor not fitted.')
        X = check_array(X)
        _, n_features = X.shape
        if self.n_features_ != n_features:
            raise ValueError('Number of features of the model must match the input. Model n_features is %s and input n_features is %s.' % (
             self.n_features_, n_features))
        y = self._program.execute(X)
        return y


class SymbolicClassifier(BaseSymbolic, ClassifierMixin):
    __doc__ = 'A Genetic Programming symbolic classifier.\n\n    A symbolic classifier is an estimator that begins by building a population\n    of naive random formulas to represent a relationship. The formulas are\n    represented as tree-like structures with mathematical functions being\n    recursively applied to variables and constants. Each successive generation\n    of programs is then evolved from the one that came before it by selecting\n    the fittest individuals from the population to undergo genetic operations\n    such as crossover, mutation or reproduction.\n\n    Parameters\n    ----------\n    population_size : integer, optional (default=500)\n        The number of programs in each generation.\n\n    generations : integer, optional (default=10)\n        The number of generations to evolve.\n\n    tournament_size : integer, optional (default=20)\n        The number of programs that will compete to become part of the next\n        generation.\n\n    stopping_criteria : float, optional (default=0.0)\n        The required metric value required in order to stop evolution early.\n\n    const_range : tuple of two floats, or None, optional (default=(-1., 1.))\n        The range of constants to include in the formulas. If None then no\n        constants will be included in the candidate programs.\n\n    init_depth : tuple of two ints, optional (default=(2, 6))\n        The range of tree depths for the initial population of naive formulas.\n        Individual trees will randomly choose a maximum depth from this range.\n        When combined with `init_method=\'half and half\'` this yields the well-\n        known \'ramped half and half\' initialization method.\n\n    init_method : str, optional (default=\'half and half\')\n        - \'grow\' : Nodes are chosen at random from both functions and\n          terminals, allowing for smaller trees than `init_depth` allows. Tends\n          to grow asymmetrical trees.\n        - \'full\' : Functions are chosen until the `init_depth` is reached, and\n          then terminals are selected. Tends to grow \'bushy\' trees.\n        - \'half and half\' : Trees are grown through a 50/50 mix of \'full\' and\n          \'grow\', making for a mix of tree shapes in the initial population.\n\n    function_set : iterable, optional (default=(\'add\', \'sub\', \'mul\', \'div\'))\n        The functions to use when building and evolving programs. This iterable\n        can include strings to indicate either individual functions as outlined\n        below, or you can also include your own functions as built using the\n        ``make_function`` factory from the ``functions`` module.\n\n        Available individual functions are:\n\n        - \'add\' : addition, arity=2.\n        - \'sub\' : subtraction, arity=2.\n        - \'mul\' : multiplication, arity=2.\n        - \'div\' : protected division where a denominator near-zero returns 1.,\n          arity=2.\n        - \'sqrt\' : protected square root where the absolute value of the\n          argument is used, arity=1.\n        - \'log\' : protected log where the absolute value of the argument is\n          used and a near-zero argument returns 0., arity=1.\n        - \'abs\' : absolute value, arity=1.\n        - \'neg\' : negative, arity=1.\n        - \'inv\' : protected inverse where a near-zero argument returns 0.,\n          arity=1.\n        - \'max\' : maximum, arity=2.\n        - \'min\' : minimum, arity=2.\n        - \'sin\' : sine (radians), arity=1.\n        - \'cos\' : cosine (radians), arity=1.\n        - \'tan\' : tangent (radians), arity=1.\n\n    transformer : str, optional (default=\'sigmoid\')\n        The name of the function through which the raw decision function is\n        passed. This function will transform the raw decision function into\n        probabilities of each class.\n\n        This can also be replaced by your own functions as built using the\n        ``make_function`` factory from the ``functions`` module.\n\n    metric : str, optional (default=\'log loss\')\n        The name of the raw fitness metric. Available options include:\n\n        - \'log loss\' aka binary cross-entropy loss.\n\n    parsimony_coefficient : float or "auto", optional (default=0.001)\n        This constant penalizes large programs by adjusting their fitness to\n        be less favorable for selection. Larger values penalize the program\n        more which can control the phenomenon known as \'bloat\'. Bloat is when\n        evolution is increasing the size of programs without a significant\n        increase in fitness, which is costly for computation time and makes for\n        a less understandable final result. This parameter may need to be tuned\n        over successive runs.\n\n        If "auto" the parsimony coefficient is recalculated for each generation\n        using c = Cov(l,f)/Var( l), where Cov(l,f) is the covariance between\n        program size l and program fitness f in the population, and Var(l) is\n        the variance of program sizes.\n\n    p_crossover : float, optional (default=0.9)\n        The probability of performing crossover on a tournament winner.\n        Crossover takes the winner of a tournament and selects a random subtree\n        from it to be replaced. A second tournament is performed to find a\n        donor. The donor also has a subtree selected at random and this is\n        inserted into the original parent to form an offspring in the next\n        generation.\n\n    p_subtree_mutation : float, optional (default=0.01)\n        The probability of performing subtree mutation on a tournament winner.\n        Subtree mutation takes the winner of a tournament and selects a random\n        subtree from it to be replaced. A donor subtree is generated at random\n        and this is inserted into the original parent to form an offspring in\n        the next generation.\n\n    p_hoist_mutation : float, optional (default=0.01)\n        The probability of performing hoist mutation on a tournament winner.\n        Hoist mutation takes the winner of a tournament and selects a random\n        subtree from it. A random subtree of that subtree is then selected\n        and this is \'hoisted\' into the original subtrees location to form an\n        offspring in the next generation. This method helps to control bloat.\n\n    p_point_mutation : float, optional (default=0.01)\n        The probability of performing point mutation on a tournament winner.\n        Point mutation takes the winner of a tournament and selects random\n        nodes from it to be replaced. Terminals are replaced by other terminals\n        and functions are replaced by other functions that require the same\n        number of arguments as the original node. The resulting tree forms an\n        offspring in the next generation.\n\n        Note : The above genetic operation probabilities must sum to less than\n        one. The balance of probability is assigned to \'reproduction\', where a\n        tournament winner is cloned and enters the next generation unmodified.\n\n    p_point_replace : float, optional (default=0.05)\n        For point mutation only, the probability that any given node will be\n        mutated.\n\n    max_samples : float, optional (default=1.0)\n        The fraction of samples to draw from X to evaluate each program on.\n\n    class_weight : dict, \'balanced\' or None, optional (default=None)\n        Weights associated with classes in the form ``{class_label: weight}``.\n        If not given, all classes are supposed to have weight one.\n\n        The "balanced" mode uses the values of y to automatically adjust\n        weights inversely proportional to class frequencies in the input data\n        as ``n_samples / (n_classes * np.bincount(y))``\n\n    feature_names : list, optional (default=None)\n        Optional list of feature names, used purely for representations in\n        the `print` operation or `export_graphviz`. If None, then X0, X1, etc\n        will be used for representations.\n\n    warm_start : bool, optional (default=False)\n        When set to ``True``, reuse the solution of the previous call to fit\n        and add more generations to the evolution, otherwise, just fit a new\n        evolution.\n\n    low_memory : bool, optional (default=False)\n        When set to ``True``, only the current generation is retained. Parent\n        information is discarded. For very large populations or runs with many\n        generations, this can result in substantial memory use reduction.\n\n    n_jobs : integer, optional (default=1)\n        The number of jobs to run in parallel for `fit`. If -1, then the number\n        of jobs is set to the number of cores.\n\n    verbose : int, optional (default=0)\n        Controls the verbosity of the evolution building process.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        If int, random_state is the seed used by the random number generator;\n        If RandomState instance, random_state is the random number generator;\n        If None, the random number generator is the RandomState instance used\n        by `np.random`.\n\n    Attributes\n    ----------\n    run_details_ : dict\n        Details of the evolution process. Includes the following elements:\n\n        - \'generation\' : The generation index.\n        - \'average_length\' : The average program length of the generation.\n        - \'average_fitness\' : The average program fitness of the generation.\n        - \'best_length\' : The length of the best program in the generation.\n        - \'best_fitness\' : The fitness of the best program in the generation.\n        - \'best_oob_fitness\' : The out of bag fitness of the best program in\n          the generation (requires `max_samples` < 1.0).\n        - \'generation_time\' : The time it took for the generation to evolve.\n\n    See Also\n    --------\n    SymbolicTransformer\n\n    References\n    ----------\n    .. [1] J. Koza, "Genetic Programming", 1992.\n\n    .. [2] R. Poli, et al. "A Field Guide to Genetic Programming", 2008.\n\n    '

    def __init__(self, population_size=1000, generations=20, tournament_size=20, stopping_criteria=0.0, const_range=(-1.0, 1.0), init_depth=(2, 6), init_method='half and half', function_set=('add', 'sub', 'mul', 'div'), transformer='sigmoid', metric='log loss', parsimony_coefficient=0.001, p_crossover=0.9, p_subtree_mutation=0.01, p_hoist_mutation=0.01, p_point_mutation=0.01, p_point_replace=0.05, max_samples=1.0, class_weight=None, feature_names=None, warm_start=False, low_memory=False, n_jobs=1, verbose=0, random_state=None):
        super(SymbolicClassifier, self).__init__(population_size=population_size,
          generations=generations,
          tournament_size=tournament_size,
          stopping_criteria=stopping_criteria,
          const_range=const_range,
          init_depth=init_depth,
          init_method=init_method,
          function_set=function_set,
          transformer=transformer,
          metric=metric,
          parsimony_coefficient=parsimony_coefficient,
          p_crossover=p_crossover,
          p_subtree_mutation=p_subtree_mutation,
          p_hoist_mutation=p_hoist_mutation,
          p_point_mutation=p_point_mutation,
          p_point_replace=p_point_replace,
          max_samples=max_samples,
          class_weight=class_weight,
          feature_names=feature_names,
          warm_start=warm_start,
          low_memory=low_memory,
          n_jobs=n_jobs,
          verbose=verbose,
          random_state=random_state)

    def __str__(self):
        """Overloads `print` output of the object to resemble a LISP tree."""
        if not hasattr(self, '_program'):
            return self.__repr__()
        return self._program.__str__()

    def _more_tags(self):
        return {'binary_only': True}

    def predict_proba(self, X):
        """Predict probabilities on test vectors X.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Input vectors, where n_samples is the number of samples
            and n_features is the number of features.

        Returns
        -------
        proba : array, shape = [n_samples, n_classes]
            The class probabilities of the input samples. The order of the
            classes corresponds to that in the attribute `classes_`.

        """
        if not hasattr(self, '_program'):
            raise NotFittedError('SymbolicClassifier not fitted.')
        X = check_array(X)
        _, n_features = X.shape
        if self.n_features_ != n_features:
            raise ValueError('Number of features of the model must match the input. Model n_features is %s and input n_features is %s.' % (
             self.n_features_, n_features))
        scores = self._program.execute(X)
        proba = self._transformer(scores)
        proba = np.vstack([1 - proba, proba]).T
        return proba

    def predict(self, X):
        """Predict classes on test vectors X.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Input vectors, where n_samples is the number of samples
            and n_features is the number of features.

        Returns
        -------
        y : array, shape = [n_samples,]
            The predicted classes of the input samples.

        """
        proba = self.predict_proba(X)
        return self.classes_.take(np.argmax(proba, axis=1), axis=0)


class SymbolicTransformer(BaseSymbolic, TransformerMixin):
    __doc__ = 'A Genetic Programming symbolic transformer.\n\n    A symbolic transformer is a supervised transformer that begins by building\n    a population of naive random formulas to represent a relationship. The\n    formulas are represented as tree-like structures with mathematical\n    functions being recursively applied to variables and constants. Each\n    successive generation of programs is then evolved from the one that came\n    before it by selecting the fittest individuals from the population to\n    undergo genetic operations such as crossover, mutation or reproduction.\n    The final population is searched for the fittest individuals with the least\n    correlation to one another.\n\n    Parameters\n    ----------\n    population_size : integer, optional (default=1000)\n        The number of programs in each generation.\n\n    hall_of_fame : integer, or None, optional (default=100)\n        The number of fittest programs to compare from when finding the\n        least-correlated individuals for the n_components. If `None`, the\n        entire final generation will be used.\n\n    n_components : integer, or None, optional (default=10)\n        The number of best programs to return after searching the hall_of_fame\n        for the least-correlated individuals. If `None`, the entire\n        hall_of_fame will be used.\n\n    generations : integer, optional (default=20)\n        The number of generations to evolve.\n\n    tournament_size : integer, optional (default=20)\n        The number of programs that will compete to become part of the next\n        generation.\n\n    stopping_criteria : float, optional (default=1.0)\n        The required metric value required in order to stop evolution early.\n\n    const_range : tuple of two floats, or None, optional (default=(-1., 1.))\n        The range of constants to include in the formulas. If None then no\n        constants will be included in the candidate programs.\n\n    init_depth : tuple of two ints, optional (default=(2, 6))\n        The range of tree depths for the initial population of naive formulas.\n        Individual trees will randomly choose a maximum depth from this range.\n        When combined with `init_method=\'half and half\'` this yields the well-\n        known \'ramped half and half\' initialization method.\n\n    init_method : str, optional (default=\'half and half\')\n        - \'grow\' : Nodes are chosen at random from both functions and\n          terminals, allowing for smaller trees than `init_depth` allows. Tends\n          to grow asymmetrical trees.\n        - \'full\' : Functions are chosen until the `init_depth` is reached, and\n          then terminals are selected. Tends to grow \'bushy\' trees.\n        - \'half and half\' : Trees are grown through a 50/50 mix of \'full\' and\n          \'grow\', making for a mix of tree shapes in the initial population.\n\n    function_set : iterable, optional (default=(\'add\', \'sub\', \'mul\', \'div\'))\n        The functions to use when building and evolving programs. This iterable\n        can include strings to indicate either individual functions as outlined\n        below, or you can also include your own functions as built using the\n        ``make_function`` factory from the ``functions`` module.\n\n        Available individual functions are:\n\n        - \'add\' : addition, arity=2.\n        - \'sub\' : subtraction, arity=2.\n        - \'mul\' : multiplication, arity=2.\n        - \'div\' : protected division where a denominator near-zero returns 1.,\n          arity=2.\n        - \'sqrt\' : protected square root where the absolute value of the\n          argument is used, arity=1.\n        - \'log\' : protected log where the absolute value of the argument is\n          used and a near-zero argument returns 0., arity=1.\n        - \'abs\' : absolute value, arity=1.\n        - \'neg\' : negative, arity=1.\n        - \'inv\' : protected inverse where a near-zero argument returns 0.,\n          arity=1.\n        - \'max\' : maximum, arity=2.\n        - \'min\' : minimum, arity=2.\n        - \'sin\' : sine (radians), arity=1.\n        - \'cos\' : cosine (radians), arity=1.\n        - \'tan\' : tangent (radians), arity=1.\n\n    metric : str, optional (default=\'pearson\')\n        The name of the raw fitness metric. Available options include:\n\n        - \'pearson\', for Pearson\'s product-moment correlation coefficient.\n        - \'spearman\' for Spearman\'s rank-order correlation coefficient.\n\n    parsimony_coefficient : float or "auto", optional (default=0.001)\n        This constant penalizes large programs by adjusting their fitness to\n        be less favorable for selection. Larger values penalize the program\n        more which can control the phenomenon known as \'bloat\'. Bloat is when\n        evolution is increasing the size of programs without a significant\n        increase in fitness, which is costly for computation time and makes for\n        a less understandable final result. This parameter may need to be tuned\n        over successive runs.\n\n        If "auto" the parsimony coefficient is recalculated for each generation\n        using c = Cov(l,f)/Var( l), where Cov(l,f) is the covariance between\n        program size l and program fitness f in the population, and Var(l) is\n        the variance of program sizes.\n\n    p_crossover : float, optional (default=0.9)\n        The probability of performing crossover on a tournament winner.\n        Crossover takes the winner of a tournament and selects a random subtree\n        from it to be replaced. A second tournament is performed to find a\n        donor. The donor also has a subtree selected at random and this is\n        inserted into the original parent to form an offspring in the next\n        generation.\n\n    p_subtree_mutation : float, optional (default=0.01)\n        The probability of performing subtree mutation on a tournament winner.\n        Subtree mutation takes the winner of a tournament and selects a random\n        subtree from it to be replaced. A donor subtree is generated at random\n        and this is inserted into the original parent to form an offspring in\n        the next generation.\n\n    p_hoist_mutation : float, optional (default=0.01)\n        The probability of performing hoist mutation on a tournament winner.\n        Hoist mutation takes the winner of a tournament and selects a random\n        subtree from it. A random subtree of that subtree is then selected\n        and this is \'hoisted\' into the original subtrees location to form an\n        offspring in the next generation. This method helps to control bloat.\n\n    p_point_mutation : float, optional (default=0.01)\n        The probability of performing point mutation on a tournament winner.\n        Point mutation takes the winner of a tournament and selects random\n        nodes from it to be replaced. Terminals are replaced by other terminals\n        and functions are replaced by other functions that require the same\n        number of arguments as the original node. The resulting tree forms an\n        offspring in the next generation.\n\n        Note : The above genetic operation probabilities must sum to less than\n        one. The balance of probability is assigned to \'reproduction\', where a\n        tournament winner is cloned and enters the next generation unmodified.\n\n    p_point_replace : float, optional (default=0.05)\n        For point mutation only, the probability that any given node will be\n        mutated.\n\n    max_samples : float, optional (default=1.0)\n        The fraction of samples to draw from X to evaluate each program on.\n\n    feature_names : list, optional (default=None)\n        Optional list of feature names, used purely for representations in\n        the `print` operation or `export_graphviz`. If None, then X0, X1, etc\n        will be used for representations.\n\n    warm_start : bool, optional (default=False)\n        When set to ``True``, reuse the solution of the previous call to fit\n        and add more generations to the evolution, otherwise, just fit a new\n        evolution.\n\n    low_memory : bool, optional (default=False)\n        When set to ``True``, only the current generation is retained. Parent\n        information is discarded. For very large populations or runs with many\n        generations, this can result in substantial memory use reduction.\n\n    n_jobs : integer, optional (default=1)\n        The number of jobs to run in parallel for `fit`. If -1, then the number\n        of jobs is set to the number of cores.\n\n    verbose : int, optional (default=0)\n        Controls the verbosity of the evolution building process.\n\n    random_state : int, RandomState instance or None, optional (default=None)\n        If int, random_state is the seed used by the random number generator;\n        If RandomState instance, random_state is the random number generator;\n        If None, the random number generator is the RandomState instance used\n        by `np.random`.\n\n    Attributes\n    ----------\n    run_details_ : dict\n        Details of the evolution process. Includes the following elements:\n\n        - \'generation\' : The generation index.\n        - \'average_length\' : The average program length of the generation.\n        - \'average_fitness\' : The average program fitness of the generation.\n        - \'best_length\' : The length of the best program in the generation.\n        - \'best_fitness\' : The fitness of the best program in the generation.\n        - \'best_oob_fitness\' : The out of bag fitness of the best program in\n          the generation (requires `max_samples` < 1.0).\n        - \'generation_time\' : The time it took for the generation to evolve.\n\n    See Also\n    --------\n    SymbolicRegressor\n\n    References\n    ----------\n    .. [1] J. Koza, "Genetic Programming", 1992.\n\n    .. [2] R. Poli, et al. "A Field Guide to Genetic Programming", 2008.\n\n    '

    def __init__(self, population_size=1000, hall_of_fame=100, n_components=10, generations=20, tournament_size=20, stopping_criteria=1.0, const_range=(-1.0, 1.0), init_depth=(2, 6), init_method='half and half', function_set=('add', 'sub', 'mul', 'div'), metric='pearson', parsimony_coefficient=0.001, p_crossover=0.9, p_subtree_mutation=0.01, p_hoist_mutation=0.01, p_point_mutation=0.01, p_point_replace=0.05, max_samples=1.0, feature_names=None, warm_start=False, low_memory=False, n_jobs=1, verbose=0, random_state=None):
        super(SymbolicTransformer, self).__init__(population_size=population_size,
          hall_of_fame=hall_of_fame,
          n_components=n_components,
          generations=generations,
          tournament_size=tournament_size,
          stopping_criteria=stopping_criteria,
          const_range=const_range,
          init_depth=init_depth,
          init_method=init_method,
          function_set=function_set,
          metric=metric,
          parsimony_coefficient=parsimony_coefficient,
          p_crossover=p_crossover,
          p_subtree_mutation=p_subtree_mutation,
          p_hoist_mutation=p_hoist_mutation,
          p_point_mutation=p_point_mutation,
          p_point_replace=p_point_replace,
          max_samples=max_samples,
          feature_names=feature_names,
          warm_start=warm_start,
          low_memory=low_memory,
          n_jobs=n_jobs,
          verbose=verbose,
          random_state=random_state)

    def __len__(self):
        """Overloads `len` output to be the number of fitted components."""
        if not hasattr(self, '_best_programs'):
            return 0
        return self.n_components

    def __getitem__(self, item):
        """Return the ith item of the fitted components."""
        if item >= len(self):
            raise IndexError
        return self._best_programs[item]

    def __str__(self):
        """Overloads `print` output of the object to resemble LISP trees."""
        if not hasattr(self, '_best_programs'):
            return self.__repr__()
        output = str([gp.__str__() for gp in self])
        return output.replace("',", ',\n').replace("'", '')

    def transform(self, X):
        """Transform X according to the fitted transformer.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Input vectors, where n_samples is the number of samples
            and n_features is the number of features.

        Returns
        -------
        X_new : array-like, shape = [n_samples, n_components]
            Transformed array.

        """
        if not hasattr(self, '_best_programs'):
            raise NotFittedError('SymbolicTransformer not fitted.')
        X = check_array(X)
        _, n_features = X.shape
        if self.n_features_ != n_features:
            raise ValueError('Number of features of the model must match the input. Model n_features is %s and input n_features is %s.' % (
             self.n_features_, n_features))
        X_new = np.array([gp.execute(X) for gp in self._best_programs]).T
        return X_new

    def fit_transform(self, X, y, sample_weight=None):
        """Fit to data, then transform it.

        Parameters
        ----------
        X : array-like, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.

        y : array-like, shape = [n_samples]
            Target values.

        sample_weight : array-like, shape = [n_samples], optional
            Weights applied to individual samples.

        Returns
        -------
        X_new : array-like, shape = [n_samples, n_components]
            Transformed array.

        """
        return self.fit(X, y, sample_weight).transform(X)