# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/finish_rule/manual_interruption.py
# Compiled at: 2016-09-21 07:18:58
import os
from kyoka.finish_rule.base_finish_rule import BaseFinishRule

class ManualInterruption(BaseFinishRule):
    TARGET_WARD = 'stop'

    def __init__(self, monitor_file_path, log_interval=100):
        BaseFinishRule.__init__(self, log_interval)
        self.monitor_file_path = monitor_file_path

    def check_condition(self, _iteration_count, _deltas):
        return self.__order_found_in_monitoring_file(self.monitor_file_path, self.TARGET_WARD)

    def generate_progress_message(self, _iteration_count, _deltas):
        return

    def generate_finish_message(self, iteration_count, _deltas):
        base_msg = 'Interrupt GPI after %d iterations because interupption order found in [ %s ].'
        return base_msg % (iteration_count, self.monitor_file_path)

    def __order_found_in_monitoring_file(self, filepath, target_word):
        return os.path.isfile(filepath) and self.__found_target_ward_in_file(filepath, target_word)

    def __found_target_ward_in_file(self, filepath, target_word):
        search_word = lambda src, target: target in src
        src = self.__read_data(filepath)
        if src:
            return search_word(src, target_word)
        return False

    def __read_data(self, filepath):
        with open(filepath, 'rb') as (f):
            return f.read()