# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/media/drivers/silent.py
# Compiled at: 2009-02-07 06:48:50
"""Fallback driver producing no audio.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: silent.py 1680 2008-01-27 09:13:50Z Alex.Holkner $'
import time
from pyglet.media import AudioPlayer, Listener, AudioData
from pyglet.media import MediaException

class SilentAudioPlayer(AudioPlayer):
    UPDATE_PERIOD = 0.1

    def __init__(self, audio_format):
        super(SilentAudioPlayer, self).__init__(audio_format)
        self._playing = False
        self._eos_count = 0
        self._audio_data_list = []
        self._head_time = 0.0
        self._head_timestamp = 0.0
        self._head_system_time = time.time()

    def get_write_size(self):
        bytes = int(self.audio_format.bytes_per_second * self.UPDATE_PERIOD)
        return max(0, bytes - sum([ a.length for a in self._audio_data_list if a is not None ]))

    def write(self, audio_data):
        if not self._audio_data_list:
            self._head_time = 0.0
            self._head_timestamp = audio_data.timestamp
            self._head_system_time = time.time()
        self._audio_data_list.append(AudioData(None, audio_data.length, audio_data.timestamp, audio_data.duration))
        audio_data.consume(audio_data.length, self.audio_format)
        return

    def write_eos(self):
        if self._audio_data_list:
            self._audio_data_list.append(None)
        return

    def write_end(self):
        pass

    def play(self):
        self._playing = True
        self._head_system_time = time.time()

    def stop(self):
        self._playing = False
        self._head_time = time.time() - self._head_system_time

    def clear(self):
        self._audio_data_list = []
        self._head_time = 0.0
        self._head_system_time = time.time()
        self._eos_count = 0

    def pump(self):
        if not self._playing:
            return
        system_time = time.time()
        head_time = system_time - self._head_system_time
        try:
            while head_time >= self._audio_data_list[0].duration:
                head_time -= self._audio_data_list[0].duration
                self._audio_data_list.pop(0)
                while self._audio_data_list[0] is None:
                    self._eos_count += 1
                    self._audio_data_list.pop(0)

            self._head_timestamp = self._audio_data_list[0].timestamp
            self._head_system_time = system_time - head_time
        except IndexError:
            pass

        return

    def get_time(self):
        if not self._audio_data_list:
            return time.time() - self._head_system_time + self._head_timestamp
        if self._playing:
            system_time = time.time()
            head_time = system_time - self._head_system_time
            return head_time + self._audio_data_list[0].timestamp
        else:
            return self._audio_data_list[0].timestamp + self._head_time

    def clear_eos(self):
        if self._eos_count:
            self._eos_count -= 1
            return True
        return False


class SilentListener(Listener):

    def _set_volume(self, volume):
        self._volume = volume

    def _set_position(self, position):
        self._position = position

    def _set_velocity(self, velocity):
        self._velocity = velocity

    def _set_forward_orientation(self, orientation):
        self._forward_orientation = orientation

    def _set_up_orientation(self, orientation):
        self._up_orientation = orientation

    def _set_doppler_factor(self, factor):
        self._doppler_factor = factor

    def _set_speed_of_sound(self, speed_of_sound):
        self._speed_of_sound = speed_of_sound


def driver_init():
    pass


driver_listener = SilentListener()
driver_audio_player_class = SilentAudioPlayer