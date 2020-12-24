# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iii/Documents/projects/ahorn/venv/lib/python3.4/site-packages/ahorn/Controller.py
# Compiled at: 2016-08-01 05:02:01
# Size of source mod 2**32: 1322 bytes


class Controller(object):
    __doc__ = 'A controller is used to play a game\n\n    The controller servers as the main interface to playing games.\n\n    Parameters\n    ----------\n    players: List\n        List of Player objects\n    inititial_state: State\n        State object from which to start the game\n\n    Returns\n    -------'

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