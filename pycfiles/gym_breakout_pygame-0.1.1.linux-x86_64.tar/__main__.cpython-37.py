# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marcofavorito/.pyenv/versions/3.7.6/lib/python3.7/site-packages/gym_breakout_pygame/__main__.py
# Compiled at: 2020-04-04 09:47:59
# Size of source mod 2**32: 1768 bytes
"""Run a short demo.

Example of usage:

    python3 gym_breakout_pygame --rows 3 --columns 3 --fire --record

"""
import time
from argparse import ArgumentParser
from datetime import datetime
from gym.wrappers import Monitor
from gym_breakout_pygame.breakout_env import BreakoutConfiguration
from gym_breakout_pygame.wrappers.dict_space import BreakoutDictSpace

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--rows', type=int, default=3, help='Number of rows')
    parser.add_argument('--columns', type=int, default=3, help='Number of columns')
    parser.add_argument('--fire', action='store_true', help='Enable fire.')
    parser.add_argument('--disable-ball', action='store_true', help='Disable the ball.')
    parser.add_argument('--record', action='store_true', help='Record a video.')
    parser.add_argument('--output-dir', type=str, default=('videos/' + str(datetime.now())), help='Video directory.')
    parser.add_argument('--random', action='store_true', help='Play randomly')
    return parser.parse_args()


def _play_randomly(env):
    env.reset()
    env.render(mode='human')
    done = False
    while not done:
        time.sleep(0.01)
        env.render(mode='human')
        obs, r, done, info = env.step(env.action_space.sample())

    env.close()


if __name__ == '__main__':
    args = parse_arguments()
    config = BreakoutConfiguration(brick_rows=(args.rows),
      brick_cols=(args.columns),
      fire_enabled=(args.fire),
      ball_enabled=(not args.disable_ball))
    env = BreakoutDictSpace(config)
    if args.record:
        env = Monitor(env, args.output_dir)
    elif args.random:
        _play_randomly(env)
    else:
        env.play()