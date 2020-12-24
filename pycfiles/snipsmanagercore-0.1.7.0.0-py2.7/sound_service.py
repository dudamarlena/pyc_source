# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanagercore/sound_service.py
# Compiled at: 2017-08-03 18:36:33
""" Sound service for playing various state sounds. """
import os, sys
from .audio_player import AudioPlayer
MODULE_PATH = os.path.dirname(sys.modules[__name__].__file__)
REL_SOUND_DIR = 'data/sounds'
ABS_SOUND_DIR = ('{}/{}').format(MODULE_PATH, REL_SOUND_DIR)

class SoundService:
    """ Sound service for playing various state sounds. """

    class State:
        """ States handled by the sound service. """
        none, welcome, goodbye, hotword_detected, asr_text_captured, error = range(6)

    @staticmethod
    def play(state):
        """ Play sound for a given state.

        :param state: a State value.
        """
        filename = None
        if state == SoundService.State.welcome:
            filename = 'pad_glow_welcome1.wav'
        elif state == SoundService.State.goodbye:
            filename = 'pad_glow_power_off.wav'
        elif state == SoundService.State.hotword_detected:
            filename = 'pad_soft_on.wav'
        elif state == SoundService.State.asr_text_captured:
            filename = 'pad_soft_off.wav'
        elif state == SoundService.State.error:
            filename = 'music_marimba_error_chord_2x.wav'
        if filename is not None:
            AudioPlayer.play_async(('{}/{}').format(ABS_SOUND_DIR, filename))
        return