# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tomaatti/internal/configuration.py
# Compiled at: 2018-10-10 03:16:16
# Size of source mod 2**32: 4203 bytes
from datetime import datetime
from tomaatti import TimerType, ConfigHelper

class Configuration(object):

    def __init__(self, configuration_parser=None):
        from os.path import expanduser, exists, join
        from os import makedirs
        from configparser import ConfigParser
        self._config_directory = expanduser('~/.config/tomaatti')
        if not exists(self._config_directory):
            makedirs(self._config_directory)
        else:
            self._config_app_state = join(self._config_directory, 'application_state.ini')
            if configuration_parser:
                self._application_config = configuration_parser
            else:
                self._application_config = ConfigParser()
                self._create_initial_config()
        if exists(self._config_app_state):
            self._application_config.read(self._config_app_state)

    def _create_initial_config(self) -> None:
        self._application_config.add_section('timer')
        self._application_config.add_section('periods')
        self._application_config.add_section('experimental')
        self._application_config.add_section('ui')
        self._application_config.set('timer', 'mode', str(TimerType.WORKING.value))
        self._application_config.set('timer', 'is_running', ConfigHelper.bool_to_config_str(False))
        self._application_config.set('timer', 'end_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self._application_config.set('periods', 'working', '25')
        self._application_config.set('periods', 'break', '5')
        self._application_config.set('ui', 'fontawesome', ConfigHelper.bool_to_config_str(False))
        self._application_config.set('experimental', 'overlay', ConfigHelper.bool_to_config_str(False))
        self._application_config.set('experimental', 'blur', ConfigHelper.bool_to_config_str(False))

    @property
    def mode(self) -> TimerType:
        return TimerType(self._application_config.getint('timer', 'mode'))

    @mode.setter
    def mode(self, value: TimerType) -> None:
        self._application_config.set('timer', 'mode', str(value.value))
        self._persist_current_state()

    @property
    def is_running(self) -> bool:
        return self._application_config.getboolean('timer', 'is_running')

    @is_running.setter
    def is_running(self, value: bool) -> None:
        self._application_config.set('timer', 'is_running', ConfigHelper.bool_to_config_str(value))
        self._persist_current_state()

    @property
    def end_time(self) -> datetime:
        return datetime.strptime(self._application_config.get('timer', 'end_time'), '%Y-%m-%d %H:%M:%S')

    @end_time.setter
    def end_time(self, value: datetime) -> None:
        self._application_config.set('timer', 'end_time', value.strftime('%Y-%m-%d %H:%M:%S'))
        self._persist_current_state()

    @property
    def work_duration(self) -> int:
        return self._application_config.getint('periods', 'working')

    @property
    def break_duration(self) -> int:
        return self._application_config.getint('periods', 'break')

    @property
    def use_fontawesome(self) -> bool:
        return self._application_config.getboolean('ui', 'fontawesome')

    @property
    def use_overlay(self) -> bool:
        return self._application_config.getboolean('experimental', 'overlay')

    @property
    def use_blur(self) -> bool:
        return self._application_config.getboolean('experimental', 'blur')

    def _persist_current_state(self) -> None:
        with open(self._config_app_state, 'w') as (configfile):
            self._application_config.write(configfile)