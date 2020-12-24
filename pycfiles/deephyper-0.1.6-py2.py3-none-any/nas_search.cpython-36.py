# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/nas_search.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 8736 bytes
import json, math, sys, os, time, datetime
from importlib import import_module
from deephyper.search import Search, util
from deephyper.evaluator.evaluate import Encoder
from deephyper.search.nas.baselines import logger
from deephyper.search.nas.baselines.common.cmd_util import common_arg_parser, make_env, make_vec_env, parse_unknown_args
from deephyper.search.nas.baselines.common.tf_util import get_session
from deephyper.search.nas.baselines.common.vec_env import VecEnv, VecFrameStack, VecNormalize
from deephyper.search.nas.baselines.common.vec_env.vec_video_recorder import VecVideoRecorder
from deephyper.search.nas.env.neural_architecture_envs import NeuralArchitectureVecEnv
from deephyper.search.nas.utils._logging import JsonMessage as jm
try:
    from mpi4py import MPI
except ImportError:
    MPI = None

dhlogger = util.conf_logger('deephyper.search.nas.nas_search')

def key(d):
    return json.dumps(dict(arch_seq=(d['arch_seq'])))


class NeuralArchitectureSearch(Search):
    __doc__ = "Represents different kind of RL algorithms working with NAS.\n\n    Args:\n        problem (str): Module path to the Problem instance you want to use for the search (e.g. deephyper.benchmark.nas.linearReg.Problem).\n        run (str): Module path to the run function you want to use for the search (e.g. deephyper.search.nas.model.run.quick).\n        evaluator (str): value in ['balsam', 'subprocess', 'processPool', 'threadPool'].\n        alg (str): algorithm to use among ['ppo2',].\n        network (str/function): policy network.\n        num_envs (int): number of environments per agent to run in\n            parallel, it corresponds to the number of evaluation per\n            batch per agent.\n    "

    def __init__(self, problem, run, evaluator, alg, network, num_envs, **kwargs):
        self.kwargs = kwargs
        if evaluator == 'balsam':
            balsam_launcher_nodes = int(os.environ.get('BALSAM_LAUNCHER_NODES', 1))
            deephyper_workers_per_node = int(os.environ.get('DEEPHYPER_WORKERS_PER_NODE', 1))
            nworkers = balsam_launcher_nodes * deephyper_workers_per_node
        else:
            nworkers = None
        if MPI is None:
            self.rank = 0
            (super().__init__)(problem, run, evaluator, cache_key=key, **kwargs)
            dhlogger.info(jm(type='start_infos',
              alg=alg,
              network=network,
              num_envs_per_agent=num_envs,
              nagents=1,
              nworkers=nworkers,
              encoded_space=json.dumps((self.problem.space), cls=Encoder)))
        else:
            self.rank = MPI.COMM_WORLD.Get_rank()
            if self.rank == 0:
                (super().__init__)(problem, run, evaluator, cache_key=key, **kwargs)
                dhlogger.info(jm(type='start_infos',
                  alg=alg,
                  network=network,
                  num_envs_per_agent=num_envs,
                  nagents=(MPI.COMM_WORLD.Get_size()),
                  nworkers=nworkers,
                  encoded_space=json.dumps((self.problem.space), cls=Encoder)))
            MPI.COMM_WORLD.Barrier()
        if self.rank != 0:
            (super().__init__)(problem, run, evaluator, cache_key=key, **kwargs)
        self.num_evals = kwargs.get('max_evals')
        if self.num_evals is None:
            self.num_evals = math.inf
        self.space = self.problem.space
        dhlogger.info(f"evaluator: {type(self.evaluator)}")
        dhlogger.info(f"rank: {self.rank}")
        dhlogger.info(f"alg: {alg}")
        dhlogger.info(f"network: {network}")
        dhlogger.info(f"num_envs_per_agent: {num_envs}")
        self.alg = alg
        self.network = network
        self.num_envs_per_agent = num_envs

    @staticmethod
    def _extend_parser(parser):
        parser.add_argument('--problem', type=str,
          default='deephyper.benchmark.nas.linearReg.Problem',
          help='Module path to the Problem instance you want to use for the search (e.g. deephyper.benchmark.nas.linearReg.Problem).')
        parser.add_argument('--run', type=str,
          default='deephyper.search.nas.model.run.alpha.run',
          help='Module path to the run function you want to use for the search (e.g. deephyper.search.nas.model.run.alpha.run).')
        parser.add_argument('--max-evals', type=int,
          default=10000000000.0,
          help='maximum number of evaluations.')
        parser.add_argument('--network', type=str,
          default='ppo_lstm',
          choices=[
         'ppo_lstm'],
          help='Policy-Value network.')
        return parser

    def main(self):
        if MPI is None or MPI.COMM_WORLD.Get_rank() == 0:
            logger.configure()
        else:
            logger.configure(format_strs=[])
        self.train(space=(self.space), evaluator=(self.evaluator),
          alg=(self.alg),
          network=(self.network),
          num_evals=(self.num_evals),
          num_envs=(self.num_envs_per_agent))

    def train(self, space, evaluator, alg, network, num_evals, num_envs):
        """Function to train ours agents.

        Args:
            space (dict): space of the search (i.e. params dict)
            evaluator (Evaluator): evaluator we are using for the search.
            alg (str): TODO
            network (str): TODO
            num_evals (int): number of evaluations to run. (i.e. number of
                episodes for NAS)

        Returns:
            [type]: [description]
        """
        seed = 2019
        learn = get_learn_function(alg)
        alg_kwargs = get_learn_function_defaults(alg)
        for k in self.kwargs:
            if k in alg_kwargs:
                alg_kwargs[k] = self.kwargs[k]

        env = build_env(num_envs, space, evaluator)
        total_timesteps = num_evals * env.num_actions_per_env
        alg_kwargs['network'] = network
        alg_kwargs['nsteps'] = env.num_actions_per_env
        model = learn(env=env, 
         seed=seed, 
         total_timesteps=total_timesteps, **alg_kwargs)
        return (
         model, env)


def build_env(num_envs, space, evaluator):
    """Build nas environment.

    Args:
        num_envs (int): number of environments to run in parallel (>=1).
        space (dict): space of the search (i.e. params dict)
        evaluator (Evaluator): evaluator object to use.

    Returns:
        VecEnv: vectorized environment.
    """
    if not num_envs >= 1:
        raise AssertionError(f"num_envs={num_envs}")
    else:
        cs_kwargs = space['create_structure'].get('kwargs')
        if cs_kwargs is None:
            structure = space['create_structure']['func']()
        else:
            structure = (space['create_structure']['func'])(**cs_kwargs)
    env = NeuralArchitectureVecEnv(num_envs, space, evaluator, structure)
    return env


def get_alg_module(alg, submodule=None):
    submodule = submodule or alg
    alg_module = import_module('.'.join(['deephyper.search.nas.baselines', alg, submodule]))
    try:
        alg_module = import_module('.'.join(['deephyper.search.nas.baselines', alg, submodule]))
    except ImportError:
        alg_module = import_module('.'.join(['rl_algs', alg, submodule]))

    return alg_module


def get_learn_function(alg):
    return get_alg_module(alg).learn


def get_learn_function_defaults(alg):
    env_type = 'nas'
    try:
        alg_defaults = get_alg_module(alg, 'defaults')
        kwargs = getattr(alg_defaults, env_type)()
    except (ImportError, AttributeError):
        kwargs = {}

    return kwargs


if __name__ == '__main__':
    kwargs = get_learn_function_defaults('ppo2')
    from pprint import pprint
    pprint(kwargs)