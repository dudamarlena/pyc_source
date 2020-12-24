# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/Arena.py
# Compiled at: 2016-08-02 10:22:46
# Size of source mod 2**32: 4706 bytes
__doc__ = 'Compare the strength of different Players'
import random, statistics, time, ahorn.Controller

class Arena(object):
    """Arena"""

    def __init__(self, Game, players, n_games=50, confidence=0.9, verbose=False, verbose_seconds=5):
        self.Game = Game
        self.players = players
        self.n_games = n_games
        self.confidence = confidence
        self.verbose = verbose
        self.verbose_seconds = verbose_seconds

    @staticmethod
    def bootstrap(series, func=statistics.mean, confidence=0.9):
        """Return the bootstrap confidence interval of a series.

        Parameters
        ----------
        series: List<float>
            your data
        func: function
            function that digests your data, default mean
        confidence: float
            width of the confidence interval, default 0.9

        Returns
        -------
        low: float
            lower bound of confidence interval
        mid: float
            median value of confidence interval
        high: float
            high bound of confidence interval"""
        n = len(series)
        n_bootstrap = 250
        digests = []
        for j in range(n_bootstrap):
            bootstrap_sample = [random.choice(series) for _ in range(n)]
            digest = func(bootstrap_sample)
            digests.append(digest)

        digests.sort()
        low, mid, high = (1.0 - confidence) / 2.0, 0.5, (1.0 + confidence) / 2.0
        low, mid, high = int(low * n_bootstrap), int(mid * n_bootstrap), int(high * n_bootstrap)
        return (
         digests[low], digests[mid], digests[high])

    def play(self):
        """Evaluate the strength of a player on a game.

        If verbose=True, will print intermediate results.

        Parameters
        ----------

        Returns
        -------
        result: dict<player, utility>
            the average utility of each player"""
        utilities = {player:[] for player in self.players}
        start_time = time.time()
        prev_print = 0
        for j in range(self.n_games):
            random.shuffle(self.players)
            initial_state = self.Game(self.players)
            contr = ahorn.Controller(initial_state)
            final_state = contr.play()
            for player in self.players:
                utilities[player].append(final_state.get_utility(player))

            elapsed = time.time() - start_time
            elapsed_since_print = time.time() - prev_print
            if self.verbose and (elapsed_since_print > self.verbose_seconds or j == self.n_games - 1):
                prev_print = time.time()
                print('{}'.format(str(self.Game)))
                print('Game {} out of {} in {:2.1f}s ({:2.1f}s per game)'.format(j + 1, self.n_games, elapsed, elapsed / (j + 1)))
                print('=' * 25)
                for player in sorted(self.players):
                    low, mid, high = Arena.bootstrap(utilities[player], func=statistics.mean, confidence=self.confidence)
                    print('{}\t|\t{:2.3f}/{:2.3f}/{:2.3f}'.format(str(player), low, mid, high))

                print('')
                continue

        result = {player:Arena.bootstrap(utility, func=statistics.mean, confidence=self.confidence)[1] for player, utility in utilities.items()}
        return result