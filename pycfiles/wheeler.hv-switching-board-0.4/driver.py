# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ryan\Documents\dev\python\hv-switching-board-firmware\hv_switching_board\driver.py
# Compiled at: 2016-01-20 22:48:56
from base_node import BaseNode
CMD_SET_STATE_OF_ALL_CHANNELS = 160
CMD_GET_STATE_OF_ALL_CHANNELS = 161

class HVSwitchingBoard(BaseNode):

    def __init__(self, proxy, address):
        BaseNode.__init__(self, proxy, address)

    def set_state_of_all_channels(self, state):
        data = np.array([0] * 5, dtype=np.uint8)
        for i in range(len(state)):
            data[(i / 8)] |= state[i] << i % 8

        for i in range(5):
            self.serialize_uint8(~data[i])

        self.send_command(CMD_SET_STATE_OF_ALL_CHANNELS)

    def state_of_all_channels(self):
        self.data = []
        self.send_command(CMD_GET_STATE_OF_ALL_CHANNELS)
        state = np.zeros(40, dtype=np.uint8)
        for i in range(len(state)):
            state[i] = self.data[(i / 8)] & 1 << i % 8 == 0

        return state