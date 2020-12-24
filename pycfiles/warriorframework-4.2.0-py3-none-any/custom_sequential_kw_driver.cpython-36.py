# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/custom_sequential_kw_driver.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 2089 bytes
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
import traceback
from . import testcase_steps_execution
from warrior.Framework import Utils
from warrior.Framework.Utils.print_Utils import print_debug, print_error

def execute_custom_sequential(step_list, data_repository, tc_status, system_name):
    """ Takes a list of steps as input and executes
    them sequentially by sending then to the
    testcase_steps_execution driver Executes all the steps in custom sequential fashion """
    step_status_list, kw_resultfile_list, step_impact_list = testcase_steps_execution.main(step_list, data_repository, system_name)
    tc_status = Utils.testcase_Utils.compute_status_using_impact(step_status_list, step_impact_list)
    print_debug('Updating Testcase result file...')
    Utils.testcase_Utils.append_result_files(data_repository['wt_resultfile'], kw_resultfile_list)
    return tc_status


def main(step_list, data_repository, tc_status, system_name=None):
    """Executes the list of keyword in sequential order
    Computes and returns the testcase status"""
    try:
        testcase_status = execute_custom_sequential(step_list, data_repository, tc_status, system_name)
    except Exception:
        testcase_status = False
        print_error('unexpected error {0}'.format(traceback.format_exc()))

    return testcase_status