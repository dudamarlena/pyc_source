# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prepare_env_test_mode/test_check_env.py
# Compiled at: 2018-09-13 02:55:15
# Size of source mod 2**32: 1019 bytes
from general_conf.generalops import GeneralClass
import os, sys, logging
from general_conf import path_config
logger = logging.getLogger(__name__)

class TestModeConfCheck(GeneralClass):
    __doc__ = '\n    Class for checking environment for running Test Mode.\n    '

    def __init__(self, config=path_config.config_path_file):
        self.conf = config
        super().__init__(config=(self.conf))
        if hasattr(self, 'gitcmd'):
            if hasattr(self, 'testpath'):
                pass
        else:
            logger.critical('Missing needed variables from config file')
            sys.exit(-1)

    def check_test_path(self, path):
        if not os.path.exists(path):
            try:
                logger.debug('Test dir does not exist')
                logger.debug('Creating test mode directory')
                os.makedirs(self.testpath)
                return True
            except Exception as err:
                logger.error(err)
                return False

        else:
            return True