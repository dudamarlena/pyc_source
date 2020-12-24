# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prepare_env_test_mode/prepare_backup.py
# Compiled at: 2018-09-13 02:55:15
# Size of source mod 2**32: 593 bytes
from backup_prepare.prepare import Prepare
from general_conf import path_config

class WrapperForPrepareTest(Prepare):

    def __init__(self, config=path_config.config_path_file, full_dir=None, inc_dir=None):
        self.conf = config
        super().__init__(config=(self.conf))
        if full_dir is not None:
            self.full_dir = full_dir
        if inc_dir is not None:
            self.inc_dir = inc_dir

    def run_prepare_backup(self):
        self.prepare_inc_full_backups()
        return True

    def run_copy_back(self):
        self.copy_back_action()
        return True