# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Step\StepCommand.py
# Compiled at: 2019-06-16 14:37:02
# Size of source mod 2**32: 1538 bytes
import os, subprocess
from py_buildsystem.common import logger
import py_buildsystem.Step.Step as Step

class StepCommand(Step):

    def __init__(self, step_config, step_name):
        self.configuration = step_config
        self._check_config()
        self.step_name = step_name

    def _check_config(self):
        try:
            self._StepCommand__command_execution_location = self.configuration['location']
        except KeyError:
            logger.warning('location not set, executing from current directory.')
            self._StepCommand__command_execution_location = './'

        try:
            self._StepCommand__commands = self.configuration['commands']
        except KeyError:
            logger.error('no commands given.')
            exit(-1)

    def get_type(self):
        return 'command'

    def perform(self):
        base_location = os.getcwd()
        logger.debug('Changing directory to ' + self._StepCommand__command_execution_location)
        os.chdir(self._StepCommand__command_execution_location)
        exit_code = 0
        for command in self._StepCommand__commands:
            logger.debug('Calling ' + command)
            if command.startswith('cd '):
                os.chdir(command.replace('cd ', ''))
            else:
                exit_code += subprocess.call(command, shell=True)

        logger.debug('Changing directory to ' + base_location)
        os.chdir(base_location)
        if exit_code:
            self.exit_code = -1
        self.exit_code = 0