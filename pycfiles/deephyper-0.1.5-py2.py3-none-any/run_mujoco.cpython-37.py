# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/ppo1/run_mujoco.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 1213 bytes
from deephyper.search.nas.baselines.common.cmd_util import make_mujoco_env, mujoco_arg_parser
import deephyper.search.nas.baselines.common as U
from deephyper.search.nas.baselines import logger

def train(env_id, num_timesteps, seed):
    from deephyper.search.nas.baselines.ppo1 import mlp_policy, pposgd_simple
    U.make_session(num_cpu=1).__enter__()

    def policy_fn(name, ob_space, ac_space):
        return mlp_policy.MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space, hid_size=64,
          num_hid_layers=2)

    env = make_mujoco_env(env_id, seed)
    pposgd_simple.learn(env, policy_fn, max_timesteps=num_timesteps,
      timesteps_per_actorbatch=2048,
      clip_param=0.2,
      entcoeff=0.0,
      optim_epochs=10,
      optim_stepsize=0.0003,
      optim_batchsize=64,
      gamma=0.99,
      lam=0.95,
      schedule='linear')
    env.close()


def main():
    args = mujoco_arg_parser().parse_args()
    logger.configure()
    train((args.env), num_timesteps=(args.num_timesteps), seed=(args.seed))


if __name__ == '__main__':
    main()