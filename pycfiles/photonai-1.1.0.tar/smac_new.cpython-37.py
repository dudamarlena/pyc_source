# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/projects_nils/photon_core/photonai/optimization/smac/smac_new.py
# Compiled at: 2019-11-21 09:20:09
# Size of source mod 2**32: 11055 bytes
import numpy as np, time, copy
import photonai.optimization as PhotonCategorical
from photonai.optimization import FloatRange, IntegerRange
from photonai.optimization.base_optimizer import PhotonBaseOptimizer
from photonai.optimization.smac.execute_ta_run import MyExecuteTARun
try:
    from smac.configspace import UniformFloatHyperparameter, UniformIntegerHyperparameter, CategoricalHyperparameter, ConfigurationSpace, Configuration, InCondition, Constant
    from smac.scenario.scenario import Scenario
    from smac.tae.execute_ta_run import StatusType
    from smac.facade.smac_bo_facade import SMAC4BO
    from smac.intensification.intensification import Intensifier
    __found__ = True
except ModuleNotFoundError:
    __found__ = False

class SMACOptimizer(PhotonBaseOptimizer):

    def __init__(self, run_obj='quality', wallclock_limit: float=float('inf'), min_r=1, max_r=1, run_limit=5, smac_helper=None):
        if __found__:
            self.wallclock_limit = wallclock_limit
            self.minR = min_r
            self.maxR = max_r
            if self.minR != 1 or self.maxR != 1:
                raise NotImplementedError('PHOTONs seed management is not implemented yet. At this juncture we can not run a config multiple times correctly.')
            self.cspace = ConfigurationSpace()
            self.runtime = 0
            self.run_start = 0
            self.run_obj = run_obj
            self.run_limit = run_limit
            self.challengers = []
            self.old_challengers = None
            self.ask_list = []
            self.switch_optiones = {}
            self.hyperparameters = []
            self.budget_exhausted = False
            self.constant_dictionary = {}
            self.smac_helper = smac_helper
            self.maximize_metric = False
        else:
            raise ModuleNotFoundError('Module smac not found or not installed as expected. Please install the smac_requirements.txt PHOTON provides.')

    @staticmethod
    def _convert_photon_to_smac_space(hyperparam: object, name: str):
        """
        Helper function: Convert PHOTON hyperparams to smac params.
        """
        if not hyperparam:
            return
            if isinstance(hyperparam, PhotonCategorical):
                return CategoricalHyperparameter(name, hyperparam.values)
            if isinstance(hyperparam, list):
                return CategoricalHyperparameter(name, hyperparam)
            if isinstance(hyperparam, FloatRange):
                if hyperparam.range_type == 'linspace':
                    return UniformFloatHyperparameter(name, hyperparam.start, hyperparam.stop)
                    if hyperparam.range_type == 'logspace':
                        raise NotImplementedError('Logspace in your float hyperparameter is not implemented in SMAC.')
                else:
                    return UniformFloatHyperparameter(name, hyperparam.start, hyperparam.stop)
        elif isinstance(hyperparam, IntegerRange):
            return UniformIntegerHyperparameter(name, hyperparam.start, hyperparam.stop)

    def build_smac_space(self, pipeline_elements):
        """
        Build entire smac hyperparam space.
        """
        for pipe_element in pipeline_elements:
            if pipe_element.__class__.__name__ == 'Switch':
                algorithm_options = {}
                for algo in pipe_element.elements:
                    algo_params = []
                    for name, value in algo.hyperparameters.items():
                        smac_param = self._convert_photon_to_smac_space(value, pipe_element.name + '__' + name)
                        algo_params.append(smac_param)

                    algorithm_options[pipe_element.name + '__' + algo.name] = algo_params

                algos = CategoricalHyperparameter(name=(pipe_element.name + '__algos'), choices=(algorithm_options.keys()))
                self.switch_optiones[pipe_element.name + '__algos'] = algorithm_options.keys()
                self.cspace.add_hyperparameter(algos)
                for algo, params in algorithm_options.items():
                    for param in params:
                        cond = InCondition(child=param, parent=algos, values=[algo])
                        self.cspace.add_hyperparameter(param)
                        self.cspace.add_condition(cond)

                continue
            if hasattr(pipe_element, 'hyperparameters'):
                for name, value in pipe_element.hyperparameters.items():
                    self.hyperparameters.append(name)
                    if isinstance(value, list):
                        if len(value) < 2:
                            self.constant_dictionary[name] = value[0]
                            continue
                    if isinstance(value, PhotonCategorical):
                        if len(value.values) < 2:
                            self.constant_dictionary[name] = value.values[0]
                            continue
                        smac_param = self._convert_photon_to_smac_space(value, name)
                        if smac_param is not None:
                            self.cspace.add_hyperparameter(smac_param)

    def prepare(self, pipeline_elements: list, maximize_metric: bool):
        self.space = ConfigurationSpace()
        self.build_smac_space(pipeline_elements)
        self.maximize_metric = maximize_metric
        self.scenario = Scenario({'run_obj':self.run_obj,  'cs':self.cspace, 
         'deterministic':'true', 
         'wallclock_limit':self.wallclock_limit})
        self.smac = SMAC4BO(scenario=(self.scenario), rng=(np.random.RandomState(42)),
          tae_runner=MyExecuteTARun)
        if self.smac_helper:
            self.smac_helper['data'] = self.smac
        self.optimizer = self.smac.solver
        self.optimizer.runhistory.overwrite_existing_runs = True
        self.ask = self.ask_generator()

    def tell(self, config, performance):
        if not config:
            return
        else:
            config = copy.copy(config)
            for key in self.switch_optiones.keys():
                config[key] = [x for x in self.switch_optiones[key] if any((x in val for val in config.keys()))][0]

            if self.maximize_metric:
                performance = 1 - performance[1]
            config = Configuration((self.cspace), values=config)
            self.optimizer.stats.ta_runs += 1
            if self.runtime == 0:
                self.optimizer.incumbent = Configuration((self.cspace), values=config)
                self.optimizer.start()
            else:
                if self.optimizer.stats.is_budget_exhausted():
                    self.budget_exhausted = True
        self.optimizer.runhistory.add(config=config, cost=performance, time=0, status=(StatusType.SUCCESS), seed=0)
        self.runtime += 1

    def ask_generator(self):

        def init():
            if self.runtime == 0:
                ta_run = MyExecuteTARun(run_limit=(self.run_limit), runhistory=(self.optimizer.runhistory))
                self.optimizer.intensifier = Intensifier(tae_runner=ta_run, stats=(self.optimizer.stats),
                  traj_logger=None,
                  rng=(np.random.RandomState(42)),
                  instances=(self.scenario.train_insts),
                  minR=1,
                  maxR=1,
                  min_chall=(self.scenario.intens_min_chall),
                  instance_specifics=(self.scenario.instance_specific))
                self.old_challengers = self.optimizer.initial_design.select_configurations()
                self.ask_list = [{key:x.get_dictionary()[key] for key in x.get_dictionary().keys() if 'algos' not in key} for x in self.optimizer.initial_design.select_configurations()]
                self.smac_helper = len(self.ask_list)
                print('-----SMAC INIT READY----')
            else:
                start_time = time.time()
                X, Y = self.optimizer.rh2EPM.transform(self.optimizer.runhistory)
                self.optimizer.logger.debug('Search for next configuration')
                challengers = self.optimizer.choose_next(X, Y)
                time_spent = time.time() - start_time
                time_left = self.optimizer._get_timebound_for_intensification(time_spent)
                if isinstance(challengers, list):
                    self.challengers = challengers[:self.run_limit]
                else:
                    self.challengers = challengers.challengers[:self.run_limit]
                self.ask_list = [{key:x.get_dictionary()[key] for key in x.get_dictionary().keys() if 'algos' not in key} for x in self.challengers]
                if self.old_challengers:
                    self.incumbent, inc_perf = self.optimizer.intensifier.intensify(challengers=(self.old_challengers),
                      incumbent=(self.optimizer.incumbent),
                      run_history=(self.optimizer.runhistory),
                      aggregate_func=(self.optimizer.aggregate_func),
                      log_traj=False,
                      time_bound=(max(self.optimizer.intensifier._min_time, time_left)))
                    self.optimizer.incumbent = self.incumbent
                self.old_challengers = self.challengers
            return 0

        i = init()
        while self.budget_exhausted:
            val = yield {}
            return
            val = yield self.ask_list[i]
            if len(self.ask_list) - 1 == i:
                i = init()
            else:
                i += 1