# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/advisor/skopt.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 10055 bytes
from skopt.space import Real, Integer, Categorical
from skopt.optimizer import Optimizer
from collections import OrderedDict
import math, numpy as np
from singa_auto.model import CategoricalKnob, FixedKnob, IntegerKnob, FloatKnob, PolicyKnob
from .constants import ParamsType, Proposal
from .advisor import BaseAdvisor, UnsupportedKnobError
FINAL_TRAIN_HOURS = 1

class BayesOptAdvisor(BaseAdvisor):
    __doc__ = '\n        Performs standard hyperparameter tuning of models using Bayesian Optimization with Gaussian Processes.\n    '

    @staticmethod
    def is_compatible(knob_config, budget):
        return BaseAdvisor.has_only_knob_types(knob_config, [CategoricalKnob, FixedKnob, IntegerKnob, FloatKnob, PolicyKnob])

    def __init__(self, knob_config, budget):
        super().__init__(knob_config, budget)
        self._fixed_knob_config, knob_config = self.extract_knob_type(knob_config, FixedKnob)
        self._policy_knob_config, knob_config = self.extract_knob_type(knob_config, PolicyKnob)
        self._dimensions = self._get_dimensions(knob_config)
        self._optimizer = self._make_optimizer(self._dimensions)
        self._search_results = []
        if not self.has_policies(self.knob_config, ['EARLY_STOP']):
            print('To speed up hyperparameter search with Bayesian Optimization, having `EARLY_STOP` policy is preferred.')

    def propose(self, worker_id, trial_no):
        proposal_type = self._get_proposal_type(trial_no)
        meta = {'proposal_type': proposal_type}
        if proposal_type == 'SEARCH':
            knobs = self._propose_knobs(['EARLY_STOP'])
            return Proposal(trial_no, knobs, meta=meta)
        if proposal_type == 'FINAL_TRAIN':
            knobs = self._propose_search_knobs()
            return Proposal(trial_no, knobs, meta=meta)
        if proposal_type is None:
            return

    def feedback(self, worker_id, result):
        proposal = result.proposal
        score = result.score
        proposal_type = proposal.meta.get('proposal_type')
        knobs = proposal.knobs
        if score is None:
            return
        if proposal_type == 'SEARCH':
            self._search_results.append((score, proposal))
        point = [knobs[name] for name in self._dimensions.keys()]
        self._optimizer.tell(point, -score)

    def _make_optimizer(self, dimensions):
        n_initial_points = 10
        return Optimizer((list(dimensions.values())),
          n_initial_points=n_initial_points,
          base_estimator='gp')

    def _get_dimensions(self, knob_config):
        dimensions = OrderedDict({name:_knob_to_dimension(x) for name, x in knob_config.items()})
        return dimensions

    def _propose_knobs(self, policies=None):
        point = self._optimizer.ask()
        knobs = {name:_simplify_value(value) for name, value in zip(self._dimensions.keys(), point)}
        knobs = self.merge_fixed_knobs(knobs, self._fixed_knob_config)
        knobs = self.merge_policy_knobs(knobs, self._policy_knob_config, policies or [])
        return knobs

    def _propose_search_knobs(self, policies=None):
        search_results = self._search_results
        if len(search_results) == 0:
            return self._propose_knobs(policies)
        else:
            search_results.sort(key=(lambda x: x[0]))
            score, proposal = search_results.pop()
            knobs = proposal.knobs
            knobs = self.merge_policy_knobs(knobs, self._policy_knob_config, policies or [])
            return knobs

    def _get_proposal_type(self, trial_no):
        if self.get_train_hours_left() <= 0:
            return
        else:
            if self.get_trials_left(trial_no) <= 0:
                return
            else:
                if not self.has_policies(self.knob_config, ['EARLY_STOP']):
                    return 'SEARCH'
                if self.get_train_hours_left() <= FINAL_TRAIN_HOURS:
                    return 'FINAL_TRAIN'
            return 'SEARCH'


class BayesOptWithParamSharingAdvisor(BaseAdvisor):
    __doc__ = '\n        Performs hyperparameter tuning of models using Bayesian Optimization with Gaussian Processes,\n        sharing globally best-scoring parameters in a greedy way.\n    '

    @staticmethod
    def is_compatible(knob_config, budget):
        return BaseAdvisor.has_only_knob_types(knob_config, [CategoricalKnob, FixedKnob, IntegerKnob, FloatKnob, PolicyKnob]) and BaseAdvisor.has_policies(knob_config, ['SHARE_PARAMS'])

    def __init__(self, knob_config, budget):
        super().__init__(knob_config, budget)
        self._fixed_knob_config, knob_config = self.extract_knob_type(knob_config, FixedKnob)
        self._policy_knob_config, knob_config = self.extract_knob_type(knob_config, PolicyKnob)
        self._dimensions = self._get_dimensions(knob_config)
        self._optimizer = self._make_optimizer(self._dimensions)
        if not self.has_policies(self.knob_config, ['EARLY_STOP']):
            print('To speed up hyperparameter search with Bayesian Optimization, having `EARLY_STOP` policy is preferred.')

    def propose(self, worker_id, trial_no):
        proposal_type = self._get_proposal_type(trial_no)
        meta = {'proposal_type': proposal_type}
        if proposal_type == 'SEARCH':
            param = self._propose_param()
            knobs = self._propose_knobs(['SHARE_PARAMS', 'EARLY_STOP'])
            return Proposal(trial_no, knobs, params_type=param, meta=meta)
        if proposal_type is None:
            return

    def feedback(self, worker_id, result):
        proposal = result.proposal
        score = result.score
        knobs = proposal.knobs
        if score is None:
            return
        point = [knobs[name] for name in self._dimensions.keys()]
        self._optimizer.tell(point, -score)

    def _make_optimizer(self, dimensions):
        n_initial_points = 10
        return Optimizer((list(dimensions.values())),
          n_initial_points=n_initial_points,
          base_estimator='gp')

    def _get_dimensions(self, knob_config):
        dimensions = OrderedDict({name:_knob_to_dimension(x) for name, x in knob_config.items()})
        return dimensions

    def _propose_knobs(self, policies=None):
        point = self._optimizer.ask()
        knobs = {name:_simplify_value(value) for name, value in zip(self._dimensions.keys(), point)}
        knobs = self.merge_fixed_knobs(knobs, self._fixed_knob_config)
        knobs = self.merge_policy_knobs(knobs, self._policy_knob_config, policies or [])
        return knobs

    def _propose_param(self):
        total_hours = self.total_train_hours
        hours_spent = total_hours - self.get_train_hours_left()
        return _propose_exp_greedy_param(hours_spent, total_hours)

    def _get_proposal_type(self, trial_no):
        if self.get_train_hours_left() <= 0:
            return
        else:
            if self.get_trials_left(trial_no) <= 0:
                return
            return 'SEARCH'


def _propose_exp_greedy_param(t, t_div):
    e = math.exp(-4 * t / t_div)
    if np.random.random() < e:
        return ParamsType.NONE
    else:
        return ParamsType.GLOBAL_BEST


def _knob_to_dimension(knob):
    if isinstance(knob, CategoricalKnob):
        return Categorical([x.value for x in knob.values])
    else:
        if isinstance(knob, IntegerKnob):
            return Integer(knob.value_min, knob.value_max)
        if isinstance(knob, FloatKnob):
            if knob.is_exp:
                value_min = knob.value_min if knob.value_min != 0 else 1e-12
                value_max = knob.value_max if knob.value_max != 0 else 1e-12
                return Real(value_min, value_max, 'log-uniform')
            else:
                return Real(knob.value_min, knob.value_max, 'uniform')
        else:
            raise UnsupportedKnobError(knob.__class__)


def _simplify_value(value):
    if isinstance(value, np.int64):
        return int(value)
    else:
        return value