# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/code/oss/hyperopt/hyperopt/algobase.py
# Compiled at: 2019-10-17 07:38:06
# Size of source mod 2**32: 10723 bytes
""" Support code for new-style search algorithms.
"""
from __future__ import print_function
from builtins import object
import copy
from collections import deque
import numpy as np
from . import pyll
from .base import miscs_update_idxs_vals
__authors__ = 'James Bergstra'
__license__ = '3-clause BSD License'
__contact__ = 'github.com/hyperopt/hyperopt'

class ExprEvaluator(object):

    def __init__(self, expr, deepcopy_inputs=False, max_program_len=None, memo_gc=True):
        """
        Parameters
        ----------

        expr - pyll Apply instance to be evaluated

        deepcopy_inputs - deepcopy inputs to every node prior to calling that
            node's function on those inputs. If this leads to a different
            return value, then some function (XXX add more complete DebugMode
            functionality) in your graph is modifying its inputs and causing
            mis-calculation. XXX: This is not a fully-functional DebugMode
            because if the offender happens on account of the toposort order
            to be the last user of said input, then it will not be detected as
            a potential problem.

        max_program_len : int (default pyll.base.DEFAULT_MAX_PROGRAM_LEN)
            If more than this many nodes are evaluated in the course of
            evaluating `expr`, then evaluation is aborted under the assumption
            that an infinite recursion is underway.

        memo_gc : bool
            If True, values computed for apply nodes within `expr` may be
            cleared during computation. The bookkeeping required to do this
            takes a bit of extra time, but usually no big deal.

        """
        self.expr = pyll.as_apply(expr)
        if deepcopy_inputs not in (0, 1, False, True):
            raise ValueError('deepcopy_inputs should be bool', deepcopy_inputs)
        self.deepcopy_inputs = deepcopy_inputs
        if max_program_len is None:
            self.max_program_len = pyll.base.DEFAULT_MAX_PROGRAM_LEN
        else:
            self.max_program_len = max_program_len
        self.memo_gc = memo_gc

    def eval_nodes(self, memo=None):
        if memo is None:
            memo = {}
        else:
            memo = dict(memo)
        if self.memo_gc:
            clients = self.clients = {}
            for aa in pyll.dfs(self.expr):
                clients.setdefault(aa, set())
                for ii in aa.inputs():
                    clients.setdefault(ii, set()).add(aa)

        todo = deque([self.expr])
        while todo:
            if len(todo) > self.max_program_len:
                raise RuntimeError('Probably infinite loop in document')
            node = todo.pop()
            if node in memo:
                continue
            if node.name == 'switch':
                waiting_on = self.on_switch(memo, node)
                if waiting_on is None:
                    continue
                else:
                    if isinstance(node, pyll.Literal):
                        self.set_in_memo(memo, node, node.obj)
                        continue
                    else:
                        waiting_on = [v for v in node.inputs() if v not in memo]
                if waiting_on:
                    todo.append(node)
                    todo.extend(waiting_on)
                else:
                    rval = self.on_node(memo, node)
                    if isinstance(rval, pyll.Apply):
                        evaluator = self.__class__(rval, self.deep_copy_inputs, self.max_program_len, self.memo_gc)
                        foo = evaluator(memo)
                        self.set_in_memo(memo, node, foo)
                    else:
                        self.set_in_memo(memo, node, rval)

        return memo

    def set_in_memo(self, memo, k, v):
        """Assign memo[k] = v

        This is implementation optionally drops references to the arguments
        "clients" required to compute apply-node `k`, which allows those
        objects to be garbage-collected. This feature is enabled by
        `self.memo_gc`.

        """
        if self.memo_gc:
            assert v is not pyll.base.GarbageCollected
            memo[k] = v
            for ii in k.inputs():
                if all(iic in memo for iic in self.clients[ii]):
                    memo[ii] = pyll.base.GarbageCollected

        else:
            memo[k] = v

    def on_switch(self, memo, node):
        switch_i_var = node.pos_args[0]
        if switch_i_var in memo:
            switch_i = memo[switch_i_var]
            try:
                int(switch_i)
            except:
                raise TypeError('switch argument was', switch_i)

            if switch_i != int(switch_i) or switch_i < 0:
                raise ValueError('switch pos must be positive int', switch_i)
            rval_var = node.pos_args[(switch_i + 1)]
            if rval_var in memo:
                self.set_in_memo(memo, node, memo[rval_var])
                return
            else:
                return [
                 rval_var]
        else:
            return [
             switch_i_var]

    def on_node(self, memo, node):
        args = _args = [memo[v] for v in node.pos_args]
        kwargs = _kwargs = dict([(k, memo[v]) for k, v in node.named_args])
        if self.memo_gc:
            for aa in args + list(kwargs.values()):
                if not aa is not pyll.base.GarbageCollected:
                    raise AssertionError

        if self.deepcopy_inputs:
            args = copy.deepcopy(_args)
            kwargs = copy.deepcopy(_kwargs)
        return pyll.scope._impls[node.name](*args, **kwargs)


class SuggestAlgo(ExprEvaluator):
    __doc__ = 'Add constructor and call signature to match suggest()\n\n    Also, detect when on_node is handling a hyperparameter, and\n    delegate that to an `on_node_hyperparameter` method. This method\n    must be implemented by a derived class.\n    '

    def __init__(self, domain, trials, seed):
        ExprEvaluator.__init__(self, domain.s_idxs_vals)
        self.domain = domain
        self.trials = trials
        self.label_by_node = dict([(n, l) for l, n in list(self.domain.vh.vals_by_label().items())])
        self._seed = seed
        self.rng = np.random.RandomState(seed)

    def __call__(self, new_id):
        self.rng.seed(self._seed + new_id)
        memo = self.eval_nodes(memo={self.domain.s_new_ids: [new_id], 
         self.domain.s_rng: self.rng})
        idxs, vals = memo[self.expr]
        new_result = self.domain.new_result()
        new_misc = dict(tid=new_id, cmd=self.domain.cmd, workdir=self.domain.workdir)
        miscs_update_idxs_vals([new_misc], idxs, vals)
        rval = self.trials.new_trial_docs([
         new_id], [None], [new_result], [new_misc])
        return rval

    def on_node(self, memo, node):
        if node in self.label_by_node:
            label = self.label_by_node[node]
            return self.on_node_hyperparameter(memo, node, label)
        else:
            return ExprEvaluator.on_node(self, memo, node)

    def batch(self, new_ids):
        new_ids = list(new_ids)
        self.rng.seed([self._seed] + new_ids)
        memo = self.eval_nodes(memo={self.domain.s_new_ids: new_ids, 
         self.domain.s_rng: self.rng})
        idxs, vals = memo[self.expr]
        return (idxs, vals)