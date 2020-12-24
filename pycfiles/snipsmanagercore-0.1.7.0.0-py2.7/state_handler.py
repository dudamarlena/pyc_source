# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanagercore/state_handler.py
# Compiled at: 2018-01-05 06:03:47
""" Handler for various states of the system. """
from .sound_service import SoundService
from .leds_service import LedsService

class State:
    none, welcome, goodbye, hotword_toggle_on, hotword_detected, asr_start_listening, asr_text_captured, error, idle, session_queued, session_started, session_ended = range(12)


class StateHandler:
    """ Handler for various states of the system. """

    def __init__(self, thread_handler):
        self.leds_service = LedsService(thread_handler)
        self.state = None
        return

    def set_state(self, state):
        if state == State.welcome:
            SoundService.play(SoundService.State.welcome)
        elif state == State.goodbye:
            SoundService.play(SoundService.State.goodbye)
            self.leds_service.start_animation(LedsService.State.none)
        elif state == State.hotword_toggle_on and self.state != state:
            self.leds_service.start_animation(LedsService.State.standby)
        elif state == State.hotword_detected:
            SoundService.play(SoundService.State.hotword_detected)
        elif state == State.asr_start_listening and self.state != state:
            self.leds_service.start_animation(LedsService.State.listening)
        elif state == State.asr_text_captured:
            SoundService.play(SoundService.State.asr_text_captured)
        elif state == State.error:
            self.leds_service.start_animation(LedsService.State.error)
            SoundService.play(SoundService.State.error)
        elif state == State.session_queued:
            pass
        elif state == State.session_started:
            pass
        elif state == State.session_ended:
            pass
        self.state = state