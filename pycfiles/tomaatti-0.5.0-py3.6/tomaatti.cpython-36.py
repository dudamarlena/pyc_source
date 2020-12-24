# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/internal/tomaatti.py
# Compiled at: 2018-10-10 03:06:45
# Size of source mod 2**32: 3534 bytes
from tomaatti import ScreenOverlay
from .configuration import Configuration
from .timertype import TimerType

class Tomaatti(object):

    def initialize(self, configuration_parser=None):
        self._config = Configuration(configuration_parser)

    @staticmethod
    def translate_string(input_text: str) -> str:
        from gettext import gettext, bindtextdomain, textdomain
        bindtextdomain('tomaatti', '/path/to/my/language/directory')
        textdomain('tomaatti')
        return gettext(input_text)

    @property
    def is_timer_up(self) -> bool:
        from datetime import datetime
        time_to_end = self._config.end_time - datetime.now()
        return time_to_end.days < 0

    @property
    def current_label(self) -> str:
        prefix = ''
        if self._config.use_fontawesome:
            prefix = '&#xf017;  '
        if not self._config.is_running:
            return '{}{}'.format(prefix, self.translate_string('Tomaatti'))
        else:
            from datetime import datetime
            time_to_end = self._config.end_time - datetime.now()
            return '{}{:02}:{:02}'.format(prefix, time_to_end.seconds % 3600 // 60, time_to_end.seconds % 60)

    def toggle_timer(self) -> None:
        from datetime import datetime, timedelta
        self._config.is_running = not self._config.is_running
        if self._config.is_running:
            current_time = datetime.now()
            period = self._config.work_duration
            if TimerType.BREAK == self._config.mode:
                period = self._config.break_duration
            time_period = timedelta(minutes=period)
            end_time = current_time + time_period
            self._config.end_time = end_time

    def show_message(self, message: str) -> None:
        if not self._config.use_overlay:
            from easygui import msgbox
            msgbox(message, Tomaatti.translate_string('Tomaatti'))
        else:
            overlay = ScreenOverlay()
            overlay.show_overlay(message)

    def check_state(self):
        if self._config.is_running:
            if self.is_timer_up:
                self.toggle_timer()
                if TimerType.WORKING == self._config.mode:
                    self.show_message(self.translate_string("It's time for a break. You worked so hard for the last %d minutes :)" % self._config.work_duration))
                    self._config.mode = TimerType.BREAK
                else:
                    if TimerType.BREAK == self._config.mode:
                        self.show_message(self.translate_string('You had %d minutes of break. Time to start working again!' % self._config.break_duration))
                        self._config.mode = TimerType.WORKING
                    else:
                        self.show_message(self.translate_string('ERROR: %s') % str(self._config.mode))
                    self.toggle_timer()

    def switch_mode(self):
        was_running = False
        if self._config.is_running:
            self.toggle_timer()
            was_running = True
        else:
            if TimerType.WORKING == self._config.mode:
                self._config.mode = TimerType.BREAK
            else:
                self._config.mode = TimerType.WORKING
        if was_running:
            self.toggle_timer()