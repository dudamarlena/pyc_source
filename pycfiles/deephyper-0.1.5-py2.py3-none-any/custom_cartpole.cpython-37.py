# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/deepq/experiments/custom_cartpole.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 3484 bytes
import gym, itertools, numpy as np, tensorflow as tf
import tensorflow.contrib.layers as layers
import deephyper.search.nas.baselines.common.tf_util as U
from deephyper.search.nas.baselines import logger
from deephyper.search.nas.baselines import deepq
from deephyper.search.nas.baselines.deepq.replay_buffer import ReplayBuffer
from deephyper.search.nas.baselines.deepq.utils import ObservationInput
from deephyper.search.nas.baselines.common.schedules import LinearSchedule

def model(inpt, num_actions, scope, reuse=False):
    """This model takes as input an observation and returns values of all actions."""
    with tf.variable_scope(scope, reuse=reuse):
        out = inpt
        out = layers.fully_connected(out, num_outputs=64, activation_fn=(tf.nn.tanh))
        out = layers.fully_connected(out, num_outputs=num_actions, activation_fn=None)
        return out


if __name__ == '__main__':
    with U.make_session(num_cpu=8):
        env = gym.make('CartPole-v0')
        act, train, update_target, debug = deepq.build_train(make_obs_ph=(lambda name: ObservationInput((env.observation_space), name=name)),
          q_func=model,
          num_actions=(env.action_space.n),
          optimizer=tf.train.AdamOptimizer(learning_rate=0.0005))
        replay_buffer = ReplayBuffer(50000)
        exploration = LinearSchedule(schedule_timesteps=10000, initial_p=1.0, final_p=0.02)
        U.initialize()
        update_target()
        episode_rewards = [
         0.0]
        obs = env.reset()
        for t in itertools.count():
            action = act((obs[None]), update_eps=(exploration.value(t)))[0]
            new_obs, rew, done, _ = env.step(action)
            replay_buffer.add(obs, action, rew, new_obs, float(done))
            obs = new_obs
            episode_rewards[(-1)] += rew
            if done:
                obs = env.reset()
                episode_rewards.append(0)
            is_solved = t > 100 and np.mean(episode_rewards[-101:-1]) >= 200
            if is_solved:
                env.render()
            else:
                if t > 1000:
                    obses_t, actions, rewards, obses_tp1, dones = replay_buffer.sample(32)
                    train(obses_t, actions, rewards, obses_tp1, dones, np.ones_like(rewards))
                if t % 1000 == 0:
                    update_target()
            if done and len(episode_rewards) % 10 == 0:
                logger.record_tabular('steps', t)
                logger.record_tabular('episodes', len(episode_rewards))
                logger.record_tabular('mean episode reward', round(np.mean(episode_rewards[-101:-1]), 1))
                logger.record_tabular('% time spent exploring', int(100 * exploration.value(t)))
                logger.dump_tabular()