# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/Classes/iterative_testsuite_class.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 6508 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from warrior.Framework.Utils import data_Utils
from warrior.Framework.Utils.testcase_Utils import pNote
from warrior.WarriorCore import sequential_testcase_driver, iterative_parallel_testcase_driver

class IterativeTestsuite(object):
    __doc__ = '\n    Class for Iterative Suite\n    '

    def __init__(self, testcase_list, suite_repository, data_repository, from_project, auto_defects):
        """
        Constructor
        """
        self.testcase_list = testcase_list
        self.suite_repository = suite_repository
        self.data_repository = data_repository
        self.from_project = from_project
        self.auto_defects = auto_defects
        self.ts_datafile = self.suite_repository['data_file']
        self.system_name_list, self.system_node_list = data_Utils.get_system_list((self.ts_datafile), node_req=True)
        self.iter_sysnamelist, self.iter_sysnode_list = data_Utils.get_iteration_syslist(self.system_node_list, self.system_name_list)

    def execute_iterative_sequential(self):
        """
        Execute the cases in a suite in iterative
        sequential fashion
        """
        ts_status = True
        if self.iter_sysnamelist == []:
            pNote('Testsuite exec_type=iterative_sequential but there are no systems in the datafile={0} that can be iterated upon, please check the iter parameter os the systems in the datafile'.format(self.ts_datafile), 'error')
            ts_status = False
        for system in self.iter_sysnamelist:
            ts_result = sequential_testcase_driver.main((self.testcase_list), (self.suite_repository), (self.data_repository),
              (self.from_project), (self.auto_defects),
              iter_ts_sys=system)
            if ts_result == 'ERROR':
                ts_status = 'ERROR'
            else:
                ts_status = ts_result and ts_status

        return ts_status

    def execute_iterative_parallel(self):
        """
        Execute the testcases in a testsuite in a iterative
        parallel fashion
        """
        ts_status = True
        if self.iter_sysnamelist == []:
            pNote('Testsuite exec_type=iterative_sequential but there are no systems in the datafile= {0} that can be iterated upon, please check the iter parameter os the systems in the datafile'.format(self.ts_datafile), 'error')
            ts_status = False
        else:
            ts_status = iterative_parallel_testcase_driver.main(self.iter_sysnamelist, self.testcase_list, self.suite_repository, self.data_repository, self.from_project, True, self.auto_defects)
        return ts_status