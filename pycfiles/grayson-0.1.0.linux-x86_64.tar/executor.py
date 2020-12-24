# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scox/dev/grayson/venv/lib/python2.7/site-packages/grayson/executor.py
# Compiled at: 2012-06-27 18:00:38
""" system """
from string import Template
import logging, os, traceback, subprocess
logger = logging.getLogger(__name__)

class Executor:

    def __init__(self, context=None):
        self.context = context

    def execute(self, command, pipe=True, processor=None, raiseException=True):
        textCommand = command
        if self.context:
            template = Template(command)
            textCommand = template.substitute(self.context)
            logging.info('   --context: %s' % self.context)
        logger.debug('executing command: %s', textCommand)
        output = os.popen(textCommand)
        line = output.readline()
        while line:
            if processor:
                processor(line)
            else:
                logging.info('           >:    %s', line.rstrip())
            line = output.readline()

        status = output.close()
        if status and status != 0 and raiseException:
            logging.error('error executing command: [%s]' % textCommand)
            raise ValueError('error executing command: [%s]' % textCommand)