# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/testgeneration/test_oracle_manager.py
# Compiled at: 2019-10-01 10:55:35
# Size of source mod 2**32: 2034 bytes
from __future__ import print_function
import os, muteria.common.fs as common_fs, muteria.common.mix as common_mix
ERROR_HANDLER = common_mix.ErrorHandler

class TestOracleManager(object):
    __doc__ = ' This class represent the test oracle manager\n        TODO: Complete this\n    '
    METADATA_FILE = '.test_oracle_mgr.metadata'

    def __init__(self, config):
        self.config = config
        self.object_to_dir = {}
        self.set_oracle()

    def oracle_checks_output(self):
        return True

    def _is_valid_metadata(self, oracles_dir):
        m_data = os.path.join(oracles_dir, self.METADATA_FILE)
        if not os.path.isfile(m_data):
            return False
        with open(m_data) as (f):
            if f.read().strip() != os.path.abspath(oracles_dir):
                return False
        return True

    def _update_metadata(self, oracles_dir):
        m_data = os.path.join(oracles_dir, self.METADATA_FILE)
        with open(m_data, 'w') as (f):
            f.write(os.path.abspath(oracles_dir))

    def add_mapping(self, tool_object, oracles_dir):
        ERROR_HANDLER.assert_true(tool_object not in self.object_to_dir, 'tool_object is already present with oracle dir: ' + oracles_dir)
        self.object_to_dir[tool_object] = oracles_dir
        if self.oracle_checks_output():
            if not os.path.isdir(oracles_dir):
                os.mkdir(oracles_dir)
            if not self._is_valid_metadata(oracles_dir):
                self._update_metadata(oracles_dir)

    def set_oracle(self, passfail=False, criteria_on=None):
        self.passfail = passfail
        self.criteria_on = criteria_on
        self.watching = self.passfail or self.criteria_on