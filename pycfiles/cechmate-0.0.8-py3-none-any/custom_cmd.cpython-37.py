# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cecdaemon/custom_cmd.py
# Compiled at: 2018-09-22 02:59:00
# Size of source mod 2**32: 994 bytes
__doc__ = 'Runs a command when a button is pressed\n'
from subprocess import Popen, PIPE, STDOUT
import logging
logging.getLogger(__name__)

class CustomCommand:
    """CustomCommand"""

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