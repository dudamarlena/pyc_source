# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/iterative_parallel_testcase_driver.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 4306 bytes
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
from collections import OrderedDict
from warrior.Framework import Utils
from warrior.Framework.Utils.print_Utils import print_error, print_debug
from warrior.WarriorCore.multiprocessing_utils import create_and_start_process_with_queue, get_results_from_queue, update_ts_junit_resultfile
from warrior.WarriorCore import sequential_testcase_driver

def execute_iterative_parallel_testcases(system_list, testcase_list, suite_repository, data_repository, from_project, tc_parallel=True, auto_defects=False):
    """Takes a list of systems as input and executes the testcases in parallel by
    creating separate process of testcase_driver for each of these systems """
    jobs_list = []
    output_q = None
    for system in system_list:
        target_module = sequential_testcase_driver.main
        tc_args_dict = OrderedDict([('testcase_list', testcase_list),
         (
          'suite_repository', suite_repository),
         (
          'data_repository', data_repository),
         (
          'from_project', from_project),
         (
          'auto_defects', auto_defects),
         (
          'system', system),
         (
          'tc_parallel', tc_parallel),
         (
          'output_q', output_q),
         ('ts_iter', True)])
        process, jobs_list, output_q = create_and_start_process_with_queue(target_module, tc_args_dict, jobs_list, output_q)

    print_debug('process: {0}'.format(process))
    for job in jobs_list:
        job.join()

    result_list = get_results_from_queue(output_q)
    tc_status_list = []
    tc_name_list = []
    tc_impact_list = []
    tc_duration_list = []
    tc_junit_list = []
    for result in result_list:
        for val in range(len(result[0])):
            tc_status_list.append(result[0][val])
            tc_name_list.append(result[1])
            tc_impact_list.append(result[2][val])
            tc_duration_list.append(result[3][val])

        tc_junit_list.append(result[4])

    update_ts_junit_resultfile(suite_repository['wt_junit_object'], tc_junit_list, data_repository['wt_ts_timestamp'])
    testsuite_status = Utils.testcase_Utils.compute_status_using_impact(tc_status_list, tc_impact_list)
    return testsuite_status


def main(system_list, testcase_list, suite_repository, data_repository, from_project, tc_parallel=False, auto_defects=False):
    """Executes the list of testcases in parallel
    Computes and returns the testsuite status"""
    try:
        testsuite_status = execute_iterative_parallel_testcases(system_list, testcase_list, suite_repository, data_repository, from_project, tc_parallel, auto_defects)
    except Exception:
        testsuite_status = False
        print_error('unexpected error {0}'.format(traceback.format_exc()))

    return testsuite_status