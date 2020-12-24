# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pytrack_analysis/logger.py
# Compiled at: 2017-07-17 09:52:02
# Size of source mod 2**32: 2378 bytes
import logging, logging.config, sys
from .profile import get_log

class Logger(object):
    __doc__ = '\n    This class creates an object for the main entry point of logging\n    '

    def __init__(self, profile, scriptname):
        """ Defines formatting and filehandler for logging """
        self.profile = profile
        self.scriptname = scriptname
        self.file_name = get_log(profile)
        self.fh = logging.FileHandler(self.file_name)
        self.log = logging.getLogger(scriptname)
        self.log.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.fh.setFormatter(formatter)
        self.log.addHandler(self.fh)
        self.log.info('==================================================')
        self.log.info('===* STARTING SCRIPT: {:} *==='.format(scriptname))
        self.log.info('Timestamp: {:}'.format(profile[profile['active']]['last active']))
        self.log.info('Part of project {:} (current user: {:})'.format(profile['active'], profile['activeuser']))
        project = profile[profile['active']]
        active_sys = profile['activesys']
        system = project['systems'][active_sys]
        self.log.info('Hosted @ {:} (OS: {:})'.format(active_sys, system['os']))
        self.log.info('Python version: {:}'.format(sys.version))

    def show(self):
        """ Prints out last log entry """
        print('\nLast log entry:\n')
        file_name = get_log(self.profile)
        with open(file_name) as (f):
            lines = f.readlines()
        out = []
        count = 0
        for _line in reversed(lines):
            out.append(_line)
            if '==================================================' in _line:
                count += 1
            elif count == 2:
                break

        outstr = ''
        for _lin in reversed(out):
            outstr += _lin

        print(outstr)

    def close(self):
        """ Closing of log """
        logger = logging.getLogger(self.scriptname)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(self.fh)
        logger.info('===*  ENDING SCRIPT  *===')
        logger.info('==================================================')