# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Labtools/digital_channel.py
# Compiled at: 2015-05-14 01:50:09
import numpy as np
from commands_proto import *
digital_channel_names = [
 'ID1', 'ID2', 'ID3', 'ID4']

class digital_channel:

    def __init__(self, a):
        self.name = ''
        self.gain = 0
        self.channel_number = a
        self.digital_channel_names = digital_channel_names
        self.xaxis = np.zeros(10000)
        self.yaxis = np.zeros(10000)
        self.timestamps = np.zeros(10000)
        self.length = 100
        self.initial_state = 0
        self.prescaler = 0
        self.datatype = 'int'
        self.trigger = 0
        self.dlength = 0
        self.plot_length = 0
        self.maximum_time = 0
        self.initial_state_override = False
        self.mode = EVERY_EDGE

    def set_params(self, **keys):
        self.channel_number = keys.get('channel_number', self.channel_number)
        self.name = digital_channel_names[self.channel_number]

    def load_data(self, initial_state, timestamps):
        if self.initial_state_override:
            self.initial_state = self.initial_state_override - 1 == 1
            self.initial_state_override = False
        else:
            self.initial_state = initial_state[self.channel_number]
        self.timestamps = timestamps
        self.dlength = len(self.timestamps)

    def generate_axes(self):
        HIGH = (4 - self.channel_number) * 3
        LOW = HIGH - 2.5
        state = HIGH if self.initial_state else LOW
        if self.prescaler == 0:
            prescale = 1.0 / 64
        elif self.prescaler == 1:
            prescale = 1.0 / 8
        elif self.prescaler == 2:
            prescale = 1.0 / 1
        elif self.prescaler == 3:
            prescale = 4.0 / 1
        if self.mode == DISABLED:
            self.xaxis[0] = 0
            self.yaxis[0] = state
            n = 1
            self.plot_length = n
        if self.mode == EVERY_EDGE:
            self.xaxis[0] = 0
            self.yaxis[0] = state
            n = 1
            for a in range(self.dlength):
                self.xaxis[n] = self.timestamps[a] * prescale
                self.yaxis[n] = state
                state = LOW if state == HIGH else HIGH
                n += 1
                self.xaxis[n] = self.timestamps[a] * prescale
                self.yaxis[n] = state
                n += 1

            self.plot_length = n
        elif self.mode == EVERY_FALLING_EDGE:
            self.xaxis[0] = 0
            self.yaxis[0] = HIGH
            n = 1
            for a in range(self.dlength):
                self.xaxis[n] = self.timestamps[a] * prescale
                self.yaxis[n] = HIGH
                n += 1
                self.xaxis[n] = self.timestamps[a] * prescale
                self.yaxis[n] = LOW
                n += 1
                self.xaxis[n] = self.timestamps[a] * prescale
                self.yaxis[n] = HIGH
                n += 1

            state = HIGH
            self.plot_length = n
        elif self.mode == EVERY_RISING_EDGE or self.mode == EVERY_FOURTH_RISING_EDGE or self.mode == EVERY_SIXTEENTH_RISING_EDGE:
            self.xaxis[0] = 0
            self.yaxis[0] = LOW
            n = 1
            for a in range(self.dlength):
                self.xaxis[n] = self.timestamps[a] * prescale
                self.yaxis[n] = LOW
                n += 1
                self.xaxis[n] = self.timestamps[a] * prescale
                self.yaxis[n] = HIGH
                n += 1
                self.xaxis[n] = self.timestamps[a] * prescale
                self.yaxis[n] = LOW
                n += 1

            state = LOW
            self.plot_length = n

    def get_xaxis(self):
        return self.xaxis[:self.plot_length]

    def get_yaxis(self):
        return self.yaxis[:self.plot_length]