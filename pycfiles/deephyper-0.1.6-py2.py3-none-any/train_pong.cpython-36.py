# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/deepq/experiments/train_pong.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 902 bytes
from deephyper.search.nas.baselines import deepq
from deephyper.search.nas.baselines import bench
from deephyper.search.nas.baselines import logger
from deephyper.search.nas.baselines.common.atari_wrappers import make_atari

def main():
    logger.configure()
    env = make_atari('PongNoFrameskip-v4')
    env = bench.Monitor(env, logger.get_dir())
    env = deepq.wrap_atari_dqn(env)
    model = deepq.learn(env,
      'conv_only',
      convs=[
     (32, 8, 4), (64, 4, 2), (64, 3, 1)],
      hiddens=[
     256],
      dueling=True,
      lr=0.0001,
      total_timesteps=(int(10000000.0)),
      buffer_size=10000,
      exploration_fraction=0.1,
      exploration_final_eps=0.01,
      train_freq=4,
      learning_starts=10000,
      target_network_update_freq=1000,
      gamma=0.99)
    model.save('pong_model.pkl')
    env.close()


if __name__ == '__main__':
    main()