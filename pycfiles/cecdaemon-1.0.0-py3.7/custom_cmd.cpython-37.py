# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cecdaemon/custom_cmd.py
# Compiled at: 2018-09-22 02:59:00
# Size of source mod 2**32: 994 bytes
"""Runs a command when a button is pressed
"""
from subprocess import Popen, PIPE, STDOUT
import logging
logging.getLogger(__name__)

class CustomCommand:
    __doc__ = 'Runs a command based on initial configuration\n\n    :str command: the command to run\n    :str holdtime: the minimum length of time in ms\n    '

    def __init__(self, command, holdtime):
        self.holdtime = holdtime
        self.command = command

    def run_command(self, key, state):
        """Runs a command if state > the config holdtime

        :str key: the key pressed
        :int state: the time key was pressed in ms
        """
        logging.info('running command: %s', self.command)
        try:
            if state >= int(self.holdtime):
                cmd = Popen((self.command.split()), stdout=PIPE, stderr=STDOUT)
                output, _ = cmd.communicate()
                logging.debug(str(output))
        except OSError:
            logging.warning('failed to run custom command for key %s', key)