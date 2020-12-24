# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/trpo_mpi/run_atari.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 1558 bytes
from mpi4py import MPI
from baselines.common import set_global_seeds
import os.path as osp, gym, logging
from baselines import logger
from baselines import bench
from baselines.common.atari_wrappers import make_atari, wrap_deepmind
from baselines.common.cmd_util import atari_arg_parser

def train(env_id, num_timesteps, seed):
    from baselines.trpo_mpi.nosharing_cnn_policy import CnnPolicy
    from baselines.trpo_mpi import trpo_mpi
    import baselines.common.tf_util as U
    rank = MPI.COMM_WORLD.Get_rank()
    sess = U.single_threaded_session()
    sess.__enter__()
    if rank == 0:
        logger.configure()
    else:
        logger.configure(format_strs=[])
    workerseed = seed + 10000 * MPI.COMM_WORLD.Get_rank()
    set_global_seeds(workerseed)
    env = make_atari(env_id)

    def policy_fn(name, ob_space, ac_space):
        return CnnPolicy(name=name, ob_space=env.observation_space, ac_space=env.action_space)

    env = bench.Monitor(env, logger.get_dir() and osp.join(logger.get_dir(), str(rank)))
    env.seed(workerseed)
    env = wrap_deepmind(env)
    env.seed(workerseed)
    trpo_mpi.learn(env, policy_fn, timesteps_per_batch=512, max_kl=0.001, cg_iters=10, cg_damping=0.001, max_timesteps=int(num_timesteps * 1.1), gamma=0.98, lam=1.0, vf_iters=3, vf_stepsize=0.0001, entcoeff=0.0)
    env.close()


def main():
    args = atari_arg_parser().parse_args()
    train(args.env, num_timesteps=args.num_timesteps, seed=args.seed)


if __name__ == '__main__':
    main()