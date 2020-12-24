# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/sumit/DATA/uChicago/Classes/Q4/Advanced Machine Learning/Advanced Machine Learning and Artificial Intelligence (MScA 32017)_Reinforced Learning/project2/pycman/pycman/test.py
# Compiled at: 2018-07-25 01:58:29
# Size of source mod 2**32: 3363 bytes
import click, json, numpy as np
from pacman import PacmanGame

class PacPlay:

    def __init__(self, start=1, end=100):
        self.test(start, end)

    def recommend_next_step(self, obs, eps=0.05):
        print('Possible actions: ', obs['possible_actions'])
        print('press key: ')
        while True:
            key = click.getchar()
            if int(key) in obs['possible_actions']:
                break
            print('Invalid key. Try again: ')

        return int(key)

    def preprocess(self, start_state):
        start_state['player'] = tuple(start_state['player'])
        start_state['monsters'] = [tuple(m) for m in start_state['monsters']]
        start_state['diamonds'] = [tuple(m) for m in start_state['diamonds']]
        start_state['walls'] = [tuple(m) for m in start_state['walls']]

    def test(self, start=1, end=100, log_file='test_pacman_log.json'):
        with open('test_params.json', 'r') as (file):
            read_params = json.load(file)
        with open(log_file, 'w') as (file):
            saved_game = json.load(file)
        start -= 1
        end -= 1
        game_params = read_params['params']
        test_start_states = read_params['states']
        total_history = [None] * 100
        total_scores = [None] * 100
        env = PacmanGame(**game_params)
        env.render()
        current_mean = 0
        for i in range(start):
            total_history[i] = saved_game[i]
            total_scores[i] = saved_game[i][(-1)]['total_score']

        for i in range(end, 100):
            total_history[i] = saved_game[i]
            total_scores[i] = saved_game[i][(-1)]['total_score']

        current_mean = np.mean(total_scores[(total_scores != None)])
        for index, start_state in enumerate(test_start_states):
            if not index < start:
                if index > end:
                    pass
                else:
                    self.preprocess(start_state)
                    episode_history = []
                    env.reset()
                    env.player = start_state['player']
                    env.monsters = start_state['monsters']
                    env.diamonds = start_state['diamonds']
                    env.walls = start_state['walls']
                    assert len(env.monsters) == env.nmonsters and len(env.diamonds) == env.ndiamonds and len(env.walls) == env.nwalls
                    obs = env.get_obs()
                    episode_history.append(obs)
                    while not obs['end_game']:
                        action = self.recommend_next_step(obs)
                        obs = env.make_action(action)
                        env.render(current_mean=int(current_mean), game_number=index)
                        episode_history.append(obs)

                    total_history[index] = episode_history
                    total_scores[index] = obs['total_score']

        mean_score = np.mean(total_scores)
        env.close()
        with open(log_file, 'w') as (file):
            json.dump(total_history, file)
        print("Your average score is {}, saved log to '{}'. Do not forget to upload it for submission!".format(mean_score, log_file))
        return mean_score


if __name__ == '__main__':
    PacPlay()