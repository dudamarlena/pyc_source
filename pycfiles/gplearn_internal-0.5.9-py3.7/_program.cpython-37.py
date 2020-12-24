# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/gplearn/_program.py
# Compiled at: 2020-04-02 03:45:04
# Size of source mod 2**32: 24230 bytes
"""The underlying data structure used in gplearn.

The :mod:`gplearn._program` module contains the underlying representation of a
computer program. It is used for creating and evolving programs used in the
:mod:`gplearn.genetic` module.
"""
from copy import deepcopy as copy
import numpy as np
from sklearn.utils.random import sample_without_replacement
from .functions import _Function
from .utils import check_random_state

class _Program(object):
    __doc__ = "A program-like representation of the evolved program.\n\n    This is the underlying data-structure used by the public classes in this\n    module. It should not be used directly by the user.\n\n    Parameters\n    ----------\n    function_set : list\n        A list of valid functions to use in the program.\n\n    arities : dict\n        A dictionary of the form `{arity: [functions]}`. The arity is the\n        number of arguments that the function takes, the functions must match\n        those in the `function_set` parameter.\n\n    init_depth : tuple of two ints\n        The range of tree depths for the initial population of naive formulas.\n        Individual trees will randomly choose a maximum depth from this range.\n        When combined with `init_method='half and half'` this yields the well-\n        known 'ramped half and half' initialization method.\n\n    init_method : str\n        - 'grow' : Nodes are chosen at random from both functions and\n          terminals, allowing for smaller trees than `init_depth` allows. Tends\n          to grow asymmetrical trees.\n        - 'full' : Functions are chosen until the `init_depth` is reached, and\n          then terminals are selected. Tends to grow 'bushy' trees.\n        - 'half and half' : Trees are grown through a 50/50 mix of 'full' and\n          'grow', making for a mix of tree shapes in the initial population.\n\n    n_features : int\n        The number of features in `X`.\n\n    const_range : tuple of two floats\n        The range of constants to include in the formulas.\n\n    metric : _Fitness object\n        The raw fitness metric.\n\n    p_point_replace : float\n        The probability that any given node will be mutated during point\n        mutation.\n\n    parsimony_coefficient : float\n        This constant penalizes large programs by adjusting their fitness to\n        be less favorable for selection. Larger values penalize the program\n        more which can control the phenomenon known as 'bloat'. Bloat is when\n        evolution is increasing the size of programs without a significant\n        increase in fitness, which is costly for computation time and makes for\n        a less understandable final result. This parameter may need to be tuned\n        over successive runs.\n\n    random_state : RandomState instance\n        The random number generator. Note that ints, or None are not allowed.\n        The reason for this being passed is that during parallel evolution the\n        same program object may be accessed by multiple parallel processes.\n\n    program : list, optional (default=None)\n        The flattened tree representation of the program. If None, a new naive\n        random tree will be grown. If provided, it will be validated.\n\n    Attributes\n    ----------\n    program : list\n        The flattened tree representation of the program.\n\n    raw_fitness_ : float\n        The raw fitness of the individual program.\n\n    fitness_ : float\n        The penalized fitness of the individual program.\n\n    oob_fitness_ : float\n        The out-of-bag raw fitness of the individual program for the held-out\n        samples. Only present when sub-sampling was used in the estimator by\n        specifying `max_samples` < 1.0.\n\n    parents : dict, or None\n        If None, this is a naive random program from the initial population.\n        Otherwise it includes meta-data about the program's parent(s) as well\n        as the genetic operations performed to yield the current program. This\n        is set outside this class by the controlling evolution loops.\n\n    depth_ : int\n        The maximum depth of the program tree.\n\n    length_ : int\n        The number of functions and terminals in the program.\n\n    "

    def __init__(self, function_set, arities, init_depth, init_method, n_features, const_range, metric, p_point_replace, parsimony_coefficient, random_state, transformer=None, feature_names=None, program=None):
        self.function_set = function_set
        self.arities = arities
        self.init_depth = (init_depth[0], init_depth[1] + 1)
        self.init_method = init_method
        self.n_features = n_features
        self.const_range = const_range
        self.metric = metric
        self.p_point_replace = p_point_replace
        self.parsimony_coefficient = parsimony_coefficient
        self.transformer = transformer
        self.feature_names = feature_names
        self.program = program
        if self.program is not None and not self.validate_program():
            raise ValueError('The supplied program is incomplete.')
        else:
            self.program = self.build_program(random_state)
        self.raw_fitness_ = None
        self.fitness_ = None
        self.parents = None
        self._n_samples = None
        self._max_samples = None
        self._indices_state = None

    def build_program(self, random_state):
        """Build a naive random program.

        Parameters
        ----------
        random_state : RandomState instance
            The random number generator.

        Returns
        -------
        program : list
            The flattened tree representation of the program.

        """
        if self.init_method == 'half and half':
            method = 'full' if random_state.randint(2) else 'grow'
        else:
            method = self.init_method
        max_depth = (random_state.randint)(*self.init_depth)
        function = random_state.randint(len(self.function_set))
        function = self.function_set[function]
        program = [function]
        terminal_stack = [function.arity]
        while terminal_stack:
            depth = len(terminal_stack)
            choice = self.n_features + len(self.function_set)
            choice = random_state.randint(choice)
            if not depth < max_depth or method == 'full' or choice <= len(self.function_set):
                function = random_state.randint(len(self.function_set))
                function = self.function_set[function]
                program.append(function)
                terminal_stack.append(function.arity)
            else:
                if self.const_range is not None:
                    terminal = random_state.randint(self.n_features + 1)
                else:
                    terminal = random_state.randint(self.n_features)
                if terminal == self.n_features:
                    terminal = (random_state.uniform)(*self.const_range)
                    if self.const_range is None:
                        raise ValueError('A constant was produced with const_range=None.')
                program.append(terminal)
                terminal_stack[(-1)] -= 1
                while terminal_stack[(-1)] == 0:
                    terminal_stack.pop()
                    if not terminal_stack:
                        return program
                    terminal_stack[(-1)] -= 1

    def validate_program(self):
        """Rough check that the embedded program in the object is valid."""
        terminals = [
         0]
        for node in self.program:
            if isinstance(node, _Function):
                terminals.append(node.arity)
            else:
                terminals[(-1)] -= 1
                while terminals[(-1)] == 0:
                    terminals.pop()
                    terminals[(-1)] -= 1

        return terminals == [-1]

    def __str__(self):
        """Overloads `print` output of the object to resemble a LISP tree."""
        terminals = [
         0]
        output = ''
        for i, node in enumerate(self.program):
            if isinstance(node, _Function):
                terminals.append(node.arity)
                output += node.name + '('
            else:
                if isinstance(node, int):
                    if self.feature_names is None:
                        output += 'X%s' % node
                    else:
                        output += self.feature_names[node]
                else:
                    output += '%.3f' % node
                terminals[(-1)] -= 1
                while terminals[(-1)] == 0:
                    terminals.pop()
                    terminals[(-1)] -= 1
                    output += ')'

            if i != len(self.program) - 1:
                output += ', '

        return output

    def export_graphviz(self, fade_nodes=None):
        """Returns a string, Graphviz script for visualizing the program.

        Parameters
        ----------
        fade_nodes : list, optional
            A list of node indices to fade out for showing which were removed
            during evolution.

        Returns
        -------
        output : string
            The Graphviz script to plot the tree representation of the program.

        """
        terminals = []
        if fade_nodes is None:
            fade_nodes = []
        output = 'digraph program {\nnode [style=filled]\n'
        for i, node in enumerate(self.program):
            fill = '#cecece'
            if isinstance(node, _Function):
                if i not in fade_nodes:
                    fill = '#136ed4'
                terminals.append([node.arity, i])
                output += '%d [label="%s", fillcolor="%s"] ;\n' % (
                 i, node.name, fill)
            else:
                if i not in fade_nodes:
                    fill = '#60a6f6'
                elif isinstance(node, int):
                    if self.feature_names is None:
                        feature_name = 'X%s' % node
                    else:
                        feature_name = self.feature_names[node]
                    output += '%d [label="%s", fillcolor="%s"] ;\n' % (
                     i, feature_name, fill)
                else:
                    output += '%d [label="%.3f", fillcolor="%s"] ;\n' % (
                     i, node, fill)
                if i == 0:
                    return output + '}'
                terminals[(-1)][0] -= 1
                terminals[(-1)].append(i)
                while terminals[(-1)][0] == 0:
                    output += '%d -> %d ;\n' % (terminals[(-1)][1],
                     terminals[(-1)][(-1)])
                    terminals[(-1)].pop()
                    if len(terminals[(-1)]) == 2:
                        parent = terminals[(-1)][(-1)]
                        terminals.pop()
                        if not terminals:
                            return output + '}'
                        terminals[(-1)].append(parent)
                        terminals[(-1)][0] -= 1

    def _depth(self):
        """Calculates the maximum depth of the program tree."""
        terminals = [
         0]
        depth = 1
        for node in self.program:
            if isinstance(node, _Function):
                terminals.append(node.arity)
                depth = max(len(terminals), depth)
            else:
                terminals[(-1)] -= 1
                while terminals[(-1)] == 0:
                    terminals.pop()
                    terminals[(-1)] -= 1

        return depth - 1

    def _length(self):
        """Calculates the number of functions and terminals in the program."""
        return len(self.program)

    def execute(self, X):
        """Execute the program according to X.

        Parameters
        ----------
        X : {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.

        Returns
        -------
        y_hats : array-like, shape = [n_samples]
            The result of executing the program on X.

        """
        node = self.program[0]
        if isinstance(node, float):
            return np.repeat(node, X.shape[0])
        if isinstance(node, int):
            return X[:, node]
        apply_stack = []
        for node in self.program:
            if isinstance(node, _Function):
                apply_stack.append([node])
            else:
                apply_stack[(-1)].append(node)
            while len(apply_stack[(-1)]) == apply_stack[(-1)][0].arity + 1:
                function = apply_stack[(-1)][0]
                terminals = [np.repeat(t, X.shape[0]) if isinstance(t, float) else X[:, t] if isinstance(t, int) else t for t in apply_stack[(-1)][1:]]
                intermediate_result = function(*terminals)
                if len(apply_stack) != 1:
                    apply_stack.pop()
                    apply_stack[(-1)].append(intermediate_result)
                else:
                    return intermediate_result

    def get_all_indices(self, n_samples=None, max_samples=None, random_state=None):
        """Get the indices on which to evaluate the fitness of a program.

        Parameters
        ----------
        n_samples : int
            The number of samples.

        max_samples : int
            The maximum number of samples to use.

        random_state : RandomState instance
            The random number generator.

        Returns
        -------
        indices : array-like, shape = [n_samples]
            The in-sample indices.

        not_indices : array-like, shape = [n_samples]
            The out-of-sample indices.

        """
        if self._indices_state is None:
            if random_state is None:
                raise ValueError('The program has not been evaluated for fitness yet, indices not available.')
        else:
            if n_samples is not None:
                if self._n_samples is None:
                    self._n_samples = n_samples
            if max_samples is not None:
                if self._max_samples is None:
                    self._max_samples = max_samples
            if random_state is not None and self._indices_state is None:
                self._indices_state = random_state.get_state()
        indices_state = check_random_state(None)
        indices_state.set_state(self._indices_state)
        not_indices = sample_without_replacement((self._n_samples),
          (self._n_samples - self._max_samples),
          random_state=indices_state)
        sample_counts = np.bincount(not_indices, minlength=(self._n_samples))
        indices = np.where(sample_counts == 0)[0]
        return (
         indices, not_indices)

    def _indices(self):
        """Get the indices used to measure the program's fitness."""
        return self.get_all_indices()[0]

    def raw_fitness(self, X, y, sample_weight):
        """Evaluate the raw fitness of the program according to X, y.

        Parameters
        ----------
        X : {array-like}, shape = [n_samples, n_features]
            Training vectors, where n_samples is the number of samples and
            n_features is the number of features.

        y : array-like, shape = [n_samples]
            Target values.

        sample_weight : array-like, shape = [n_samples]
            Weights applied to individual samples.

        Returns
        -------
        raw_fitness : float
            The raw fitness of the program.

        """
        y_pred = self.execute(X)
        if self.transformer:
            y_pred = self.transformer(y_pred)
        raw_fitness = self.metric(y, y_pred, sample_weight)
        return raw_fitness

    def fitness(self, parsimony_coefficient=None):
        """Evaluate the penalized fitness of the program according to X, y.

        Parameters
        ----------
        parsimony_coefficient : float, optional
            If automatic parsimony is being used, the computed value according
            to the population. Otherwise the initialized value is used.

        Returns
        -------
        fitness : float
            The penalized fitness of the program.

        """
        if parsimony_coefficient is None:
            parsimony_coefficient = self.parsimony_coefficient
        penalty = parsimony_coefficient * len(self.program) * self.metric.sign
        return self.raw_fitness_ - penalty

    def get_subtree(self, random_state, program=None):
        """Get a random subtree from the program.

        Parameters
        ----------
        random_state : RandomState instance
            The random number generator.

        program : list, optional (default=None)
            The flattened tree representation of the program. If None, the
            embedded tree in the object will be used.

        Returns
        -------
        start, end : tuple of two ints
            The indices of the start and end of the random subtree.

        """
        if program is None:
            program = self.program
        probs = np.array([0.9 if isinstance(node, _Function) else 0.1 for node in program])
        probs = np.cumsum(probs / probs.sum())
        start = np.searchsorted(probs, random_state.uniform())
        stack = 1
        end = start
        while stack > end - start:
            node = program[end]
            if isinstance(node, _Function):
                stack += node.arity
            end += 1

        return (start, end)

    def reproduce(self):
        """Return a copy of the embedded program."""
        return copy(self.program)

    def crossover(self, donor, random_state):
        """Perform the crossover genetic operation on the program.

        Crossover selects a random subtree from the embedded program to be
        replaced. A donor also has a subtree selected at random and this is
        inserted into the original parent to form an offspring.

        Parameters
        ----------
        donor : list
            The flattened tree representation of the donor program.

        random_state : RandomState instance
            The random number generator.

        Returns
        -------
        program : list
            The flattened tree representation of the program.

        """
        start, end = self.get_subtree(random_state)
        removed = range(start, end)
        donor_start, donor_end = self.get_subtree(random_state, donor)
        donor_removed = list(set(range(len(donor))) - set(range(donor_start, donor_end)))
        return (
         self.program[:start] + donor[donor_start:donor_end] + self.program[end:], removed, donor_removed)

    def subtree_mutation(self, random_state):
        """Perform the subtree mutation operation on the program.

        Subtree mutation selects a random subtree from the embedded program to
        be replaced. A donor subtree is generated at random and this is
        inserted into the original parent to form an offspring. This
        implementation uses the "headless chicken" method where the donor
        subtree is grown using the initialization methods and a subtree of it
        is selected to be donated to the parent.

        Parameters
        ----------
        random_state : RandomState instance
            The random number generator.

        Returns
        -------
        program : list
            The flattened tree representation of the program.

        """
        chicken = self.build_program(random_state)
        return self.crossover(chicken, random_state)

    def hoist_mutation(self, random_state):
        """Perform the hoist mutation operation on the program.

        Hoist mutation selects a random subtree from the embedded program to
        be replaced. A random subtree of that subtree is then selected and this
        is 'hoisted' into the original subtrees location to form an offspring.
        This method helps to control bloat.

        Parameters
        ----------
        random_state : RandomState instance
            The random number generator.

        Returns
        -------
        program : list
            The flattened tree representation of the program.

        """
        start, end = self.get_subtree(random_state)
        subtree = self.program[start:end]
        sub_start, sub_end = self.get_subtree(random_state, subtree)
        hoist = subtree[sub_start:sub_end]
        removed = list(set(range(start, end)) - set(range(start + sub_start, start + sub_end)))
        return (self.program[:start] + hoist + self.program[end:], removed)

    def point_mutation(self, random_state):
        """Perform the point mutation operation on the program.

        Point mutation selects random nodes from the embedded program to be
        replaced. Terminals are replaced by other terminals and functions are
        replaced by other functions that require the same number of arguments
        as the original node. The resulting tree forms an offspring.

        Parameters
        ----------
        random_state : RandomState instance
            The random number generator.

        Returns
        -------
        program : list
            The flattened tree representation of the program.

        """
        program = copy(self.program)
        mutate = np.where(random_state.uniform(size=(len(program))) < self.p_point_replace)[0]
        for node in mutate:
            if isinstance(program[node], _Function):
                arity = program[node].arity
                replacement = len(self.arities[arity])
                replacement = random_state.randint(replacement)
                replacement = self.arities[arity][replacement]
                program[node] = replacement
            else:
                if self.const_range is not None:
                    terminal = random_state.randint(self.n_features + 1)
                else:
                    terminal = random_state.randint(self.n_features)
                if terminal == self.n_features:
                    terminal = (random_state.uniform)(*self.const_range)
                    if self.const_range is None:
                        raise ValueError('A constant was produced with const_range=None.')
                program[node] = terminal

        return (
         program, list(mutate))

    depth_ = property(_depth)
    length_ = property(_length)
    indices_ = property(_indices)