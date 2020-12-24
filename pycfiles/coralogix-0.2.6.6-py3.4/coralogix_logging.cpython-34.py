# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\coralogix\coralogix_logging.py
# Compiled at: 2015-12-23 07:43:25
# Size of source mod 2**32: 2718 bytes
"""
Exposes the CoralogixLogger functionality as a `logging.Handler` to be used by other Python modules.
"""
import logging
from coralogix import Severity
from .logger import CoralogixLogger
VERBOSE = 15
logging.addLevelName(VERBOSE, 'VERBOSE')
LOGGING_LEVEL_MAP = {logging.DEBUG: Severity.Debug, 
 VERBOSE: Severity.Verbose, 
 logging.INFO: Severity.Info, 
 logging.WARNING: Severity.Warning, 
 logging.ERROR: Severity.Error, 
 logging.CRITICAL: Severity.Critical}

class CoralogixHandler(logging.Handler, object):
    __doc__ = 'A logging handler class which sends logging records to the Coralogix service.'

    def __init__(self, company_id, private_key, app_name=None, subsystem_name=None, config_dir=None):
        try:
            super(CoralogixHandler, self).__init__()
            self._coralogix_logger = CoralogixLogger(config_dir)
            self._coralogix_logger.connect(company_id, private_key, app_name, subsystem_name, raise_exceptions=False)
        except Exception as e:
            print('CoralogixHandler.__init__(): caught exception= {0} when connecting using company_id= {1}, private_key= {2}, app_name= {3}, subsystem_name= {4}'.format(e, company_id, private_key, app_name, subsystem_name))

    def setFormatter(self, fmt):
        """Formatting is not needed for Coralogix."""
        pass

    def emit(self, record):
        """Emits a record. Unlike Python's logging handlers, no formatting is needed for Coralogix."""
        try:
            if record.levelno in LOGGING_LEVEL_MAP:
                level = LOGGING_LEVEL_MAP[record.levelno]
            else:
                levels, levelno_key = sorted(LOGGING_LEVEL_MAP.keys()), None
                for i in range(len(levels) - 1):
                    if levels[i] < record.levelno < levels[(i + 1)]:
                        levelno_key = levels[i] if record.levelno - levels[i] <= abs(record.levelno - levels[(i + 1)]) else levels[(i + 1)]
                        break

                level = LOGGING_LEVEL_MAP[levelno_key]
            self._coralogix_logger.send_log(level, record.getMessage(), record.name, record.module, record.funcName)
        except Exception as e:
            self.handleError(record)