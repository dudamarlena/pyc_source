# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/microcsound/state.py
# Compiled at: 2017-11-14 16:00:36
# Size of source mod 2**32: 1605 bytes
from microcsound import constants

class State(object):

    def __init__(self):
        self.div = 31
        self.instr = 1
        self.tempo = 120
        self.tempostring = 't 0 120 '
        self.outstring = 'i200 0 -1\n'
        self.tie_dict = {}
        self.reset_voice()

    def reset_voice(self):
        self.length = 0.25
        self.octave = 5
        self.articulation = 'non-legato'
        self.grid_time = 0
        self.chord_status = 0
        self.xtra = ['']
        self.octave = constants.MIDDLE_C_OCTAVE
        self.degree = 0
        self.key = 1
        self.length_factor = 1
        self.tie = 0
        self.staccato_length = 0.2
        self.non_legato_space = 0.02
        self.pedal_down = False
        self.arrival = 0
        self.default_attack = 0.66
        self.pan = 0.5
        self.mix = 1
        self.gaussian_rhythm = 0
        self.gaussian_volume = 0
        self.gaussian_staccato = 0


state_obj = State()