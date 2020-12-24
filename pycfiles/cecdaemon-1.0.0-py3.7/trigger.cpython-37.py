# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cecdaemon/trigger.py
# Compiled at: 2018-09-22 02:58:13
# Size of source mod 2**32: 1912 bytes
""" Handles triggers from cec such as standby or wake
"""
import logging
from types import ModuleType
from subprocess import Popen, PIPE, STDOUT
from .const import COMMANDS
logging.getLogger(__name__)

class Trigger:
    __doc__ = ' Takes a libcec object and registers its methods as callbacks for\n        executing custom commands from a config\n\n    :param cec: python-cec instance\n    :type cec: obj\n    '

    def __init__(self, cec=None, triggerconf=None):
        if not isinstance(cec, ModuleType):
            raise AssertionError
        else:
            logging.info('Loading triggers')
            logging.debug(str(COMMANDS))
            logging.debug(str(triggerconf))
            if triggerconf is None:
                logging.warning('No triggers found in config file')
            else:
                self.conf = triggerconf
                cec.add_callback(self.event_handler, cec.EVENT_COMMAND)

    def event_handler(self, event, data):
        """ Checks if the opcode is in the config and passes the command from
            config to the run_command method

        :param event: should be 4 for cec commands
        :type event: int
        :param data: contains the event details
        :type data: dict
        """
        assert event == 4
        opcode = data['opcode']
        logging.debug('Received opcode %s', format(opcode, '02x'))
        if opcode in COMMANDS:
            command = COMMANDS[opcode]
            logging.info('Detected event %s', command)
            self.run_command(self.conf[command])

    def run_command(self, command):
        """ Runs command with Popen

        :param command: shell command to execute
        :type command: str
        """
        logging.info('Running %s', command)
        try:
            cmd = Popen((command.split()), stdout=PIPE, stderr=STDOUT)
            output, _ = cmd.communicate()
            logging.debug(str(output))
        except OSError:
            logging.warning('Failed to run %s', command)