# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/Controller.py
# Compiled at: 2016-08-01 05:02:01
# Size of source mod 2**32: 1322 bytes


class Controller(object):
    """Controller"""

    def __init__(self, initial_state, verbose=False):
        self.state = initial_state
        self.verbose = verbose

    def play(self):
        """Plays the game untill a final state is reached

        Parameters
        ----------

        Returns
        -------
        final_state: State
            The final state"""
        state = self.state
        while not state.is_final():
            actor = state.get_actor()
            if self.verbose:
                print(state.str(actor))
            action = actor.get_action(state.get_random(actor))
            assert str(action) in [str(a) for a in state.get_legal_actions(actor)]
            state = action.execute(state)
            if self.verbose:
                print(str(action))
                continue

        self.state = state
        if self.verbose:
            print(state.str(actor))
            print('Points: {}'.format(' ,'.join([str(state.get_utility(player)) for player in state.get_players()])))
        return self.state