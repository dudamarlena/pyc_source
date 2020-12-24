# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/ppo1/run_humanoid.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 2753 bytes
import os
from deephyper.search.nas.baselines.common.cmd_util import make_mujoco_env, mujoco_arg_parser
from deephyper.search.nas.baselines.common import tf_util as U
from deephyper.search.nas.baselines import logger
import gym

def train(num_timesteps, seed, model_path=None):
    env_id = 'Humanoid-v2'
    from deephyper.search.nas.baselines.ppo1 import mlp_policy, pposgd_simple
    U.make_session(num_cpu=1).__enter__()

    def policy_fn(name, ob_space, ac_space):
        return mlp_policy.MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space, hid_size=64,
          num_hid_layers=2)

    env = make_mujoco_env(env_id, seed)
    env = RewScale(env, 0.1)
    logger.log('NOTE: reward will be scaled by a factor of 10  in logged stats. Check the monitor for unscaled reward.')
    pi = pposgd_simple.learn(env, policy_fn, max_timesteps=num_timesteps,
      timesteps_per_actorbatch=2048,
      clip_param=0.1,
      entcoeff=0.0,
      optim_epochs=10,
      optim_stepsize=0.0001,
      optim_batchsize=64,
      gamma=0.99,
      lam=0.95,
      schedule='constant')
    env.close()
    if model_path:
        U.save_state(model_path)
    return pi


class RewScale(gym.RewardWrapper):

    def __init__(self, env, scale):
        gym.RewardWrapper.__init__(self, env)
        self.scale = scale

    def reward(self, r):
        return r * self.scale


def main():
    logger.configure()
    parser = mujoco_arg_parser()
    parser.add_argument('--model-path',
      default=(os.path.join(logger.get_dir(), 'humanoid_policy')))
    parser.set_defaults(num_timesteps=(int(50000000.0)))
    args = parser.parse_args()
    if not args.play:
        train(num_timesteps=(args.num_timesteps), seed=(args.seed),
          model_path=(args.model_path))
    else:
        pi = train(num_timesteps=1, seed=(args.seed))
        U.load_state(args.model_path)
        env = make_mujoco_env('Humanoid-v2', seed=0)
        ob = env.reset()
        while 1:
            action = pi.act(stochastic=False, ob=ob)[0]
            ob, _, done, _ = env.step(action)
            env.render()
            if done:
                ob = env.reset()


if __name__ == '__main__':
    main()