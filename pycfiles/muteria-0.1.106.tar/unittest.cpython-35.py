# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/testgeneration/testcase_formats/python_unittest/unittest.py
# Compiled at: 2019-09-19 05:11:43
# Size of source mod 2**32: 1423 bytes
import os, sys
from muteria.common.mix import GlobalConstants
from muteria.drivers import DriversUtils

def python_unittest_runner(test_name, repo_root_dir, exe_path_map, env_vars, timeout):

    def parse_test(s):
        return s.split('...')[0].replace(':', '/').replace(' ', '')

    cwd = os.getcwd()
    os.chdir(repo_root_dir)
    try:
        args_list = ['-m', 'unittest', test_name, '-v']
        retcode, stdout, _ = DriversUtils.execute_and_get_retcode_out_err(prog=sys.executable, args_list=args_list, timeout=timeout, merge_err_to_out=True)
        stdout = stdout.splitlines()
    except:
        os.chdir(cwd)
        return GlobalConstants.TEST_EXECUTION_ERROR

    subtests_verdicts = {}
    hasfail = False
    hasfail |= retcode != 0
    for s in stdout:
        if s.endswith('... FAIL'):
            hasfail = True
            subtests_verdicts[parse_test(s)] = True
        elif s.endswith('... ok'):
            subtests_verdicts[parse_test(s)] = False

    os.chdir(cwd)
    if hasfail:
        return GlobalConstants.FAIL_TEST_VERDICT
    return GlobalConstants.PASS_TEST_VERDICT