# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/ppo.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 4668 bytes
import os
from deephyper.search.nas.nas_search import NeuralArchitectureSearch
try:
    from mpi4py import MPI
except ImportError:
    MPI = None

class Ppo(NeuralArchitectureSearch):
    __doc__ = "Search class to run a proximal policy optimization search. The search is launching as many agents as the number of MPI ranks. Each agent is batch synchronous on a number of DNN evaluations. This number of parallel evaluation is equal for all agents, and automaticaly computed based on the number of available workers when using `evaluator='balsam'`. For other evaluators it will be set to 1.\n\n    Args:\n        problem (str): Module path to the Problem instance you want to use for the search (e.g. deephyper.benchmark.nas.linearReg.Problem).\n        run (str): Module path to the run function you want to use for the search (e.g. deephyper.search.nas.model.run.quick).\n        evaluator (str): value in ['balsam', 'subprocess', 'processPool', 'threadPool'].\n        network: (str): policy network for the search, value in [\n            'ppo_lstm_128',\n            'ppo_lnlstm_128',\n            'ppo_lstm_64',\n            'ppo_lnlstm_64',\n            'ppo_lstm_32',\n            'ppo_lnlstm_32'\n            ].\n    "

    def __init__(self, problem, run, evaluator, network, **kwargs):
        if MPI is None:
            nenvs = 1
        else:
            nranks = MPI.COMM_WORLD.Get_size()
            if evaluator == 'balsam':
                balsam_launcher_nodes = int(os.environ.get('BALSAM_LAUNCHER_NODES', 1))
                deephyper_workers_per_node = int(os.environ.get('DEEPHYPER_WORKERS_PER_NODE', 1))
                nagents = nranks
                n_free_nodes = balsam_launcher_nodes - nranks
                free_workers = n_free_nodes * deephyper_workers_per_node
                nenvs = free_workers // nagents
            else:
                nenvs = 1
        (super().__init__)(problem, run, evaluator, alg='ppo2', 
         network=network, 
         num_envs=nenvs, **kwargs)

    @staticmethod
    def _extend_parser(parser):
        NeuralArchitectureSearch._extend_parser(parser)
        parser.add_argument('--cliprange', type=float,
          default=0.2,
          help='Clipping parameter of PPO.')
        parser.add_argument('--ent-coef', type=float,
          default=0.01,
          help='Entropy parameter for PPO. Adding entropy helps to avoid convergence to a local optimum. To increase the entropy parameter is to increase exploration.')
        parser.add_argument('--gamma', type=float,
          default=1.0,
          help='Gamma parameter for advantage function in RL, discounting factor for rewards.')
        parser.add_argument('--lam', type=float,
          default=0.95,
          help='Lambda parameter for advantage function in RL, advantage estimation discounting factor (lambda in the paper).')
        parser.add_argument('--nminibatches', type=int,
          default=1,
          help="Number of minibatches per environments. Here it's directly the number of batch of architectures.")
        parser.add_argument('--noptepochs', type=int,
          default=10,
          help='Number of optimization steps to do per epochs. Basicaly it means the number of time you want to use learning data.')
        parser.add_argument('--max-evals', type=int, default=10000000000.0, help='maximum number of learning update.')
        parser.add_argument('--network', type=str, default='ppo_lstm_128', choices=[
         'ppo_lstm_128',
         'ppo_lnlstm_128',
         'ppo_lstm_64',
         'ppo_lnlstm_64',
         'ppo_lstm_32',
         'ppo_lnlstm_32'],
          help='Policy-Value network.')
        return parser


if __name__ == '__main__':
    args = Ppo.parse_args()
    search = Ppo(**vars(args))
    search.main()