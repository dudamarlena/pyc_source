# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/ppo.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 3805 bytes
import os
from deephyper.core.parser import add_arguments_from_signature
from deephyper.search.nas.rl import ReinforcementLearningSearch
try:
    from mpi4py import MPI
except ImportError:
    MPI = None

class Ppo(ReinforcementLearningSearch):
    __doc__ = "Search class to run a proximal policy optimization search. The search is launching as many agents as the number of MPI ranks. Each agent is batch synchronous on a number of DNN evaluations. This number of parallel evaluation is equal for all agents, and automaticaly computed based on the number of available workers when using `evaluator='balsam'`. For other evaluators it will be set to 1.\n\n    Args:\n        problem (str): Module path to the Problem instance you want to use for the search (e.g. deephyper.benchmark.nas.linearReg.Problem).\n        run (str): Module path to the run function you want to use for the search (e.g. deephyper.search.nas.model.run.alpha.run).\n        evaluator (str): value in ['balsam', 'ray', 'subprocess', 'processPool', 'threadPool']. Default to 'ray'.\n        cliprange (float, optional): Clipping parameter of PPO. Defaults to 0.2.\n        ent_coef (float, optional): Entropy parameter for PPO. Adding entropy helps to avoid convergence to a local optimum. To increase the entropy parameter is to increase exploration. Defaults to 0.01.\n        gamma (float, optional): Gamma parameter for advantage function in RL, discounting factor for rewards. Defaults to 1.0.\n        lam (float, optional): Lambda parameter for advantage function in RL, advantage estimation discounting factor (lambda in the paper). Defaults to 0.95.\n        nminibatches (int, optional): Number of minibatches per environments. Here it's directly the number of batch of search_spaces. Defaults to 1.\n        noptepochs (int, optional): Number of optimization steps to do per epochs. Basicaly it means the number of time you want to use learning data. Defaults to 10.\n        network: (str): policy network for the search, value in [\n            'ppo_lstm_128',\n            'ppo_lnlstm_128',\n            'ppo_lstm_64',\n            'ppo_lnlstm_64',\n            'ppo_lstm_32',\n            'ppo_lnlstm_32'\n            ].\n    "

    def __init__(self, problem, run, evaluator, network='ppo_lnlstm_128', cliprange=0.2, ent_coef=0.01, gamma=1.0, lam=0.95, nminibatches=1, noptepochs=10, **kwargs):
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
        (super().__init__)(problem, run, alg='ppo2', 
         num_envs=nenvs, 
         evaluator=evaluator, 
         network=network, 
         cliprange=cliprange, 
         ent_coef=ent_coef, 
         gamma=gamma, 
         lam=lam, 
         nminibatches=nminibatches, 
         noptepochs=noptepochs, **kwargs)

    @staticmethod
    def _extend_parser(parser):
        ReinforcementLearningSearch._extend_parser(parser)
        add_arguments_from_signature(parser, Ppo)
        return parser


if __name__ == '__main__':
    args = Ppo.parse_args()
    search = Ppo(**vars(args))
    search.main()