# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/testgeneration/testcase_formats/system_devtest/system_devtest_runner.py
# Compiled at: 2019-11-05 12:14:42
# Size of source mod 2**32: 1903 bytes
import os, logging, shutil
from muteria.common.mix import GlobalConstants
from muteria.drivers import DriversUtils
from muteria.drivers.testgeneration.custom_dev_testcase.system_wrappers import TEST_FILE_NAME_ENV_VAR, TEST_EXECUTION_TIMEOUT_ENV_VAR

def system_test_runner(prog, args_list, test_filename, repo_root_dir, exe_path_map=None, env_vars=None, timeout=None, collected_output=None, using_wrapper=False):
    try:
        tmp_env = os.environ.copy()
        if env_vars is not None:
            tmp_env.update(env_vars)
        if test_filename is not None:
            tmp_env[TEST_FILE_NAME_ENV_VAR] = test_filename
        if using_wrapper and timeout is not None:
            tmp_env[TEST_EXECUTION_TIMEOUT_ENV_VAR] = str(timeout)
            timeout = None
        if collected_output is None:
            retcode, _, _ = DriversUtils.execute_and_get_retcode_out_err(prog=prog, args_list=args_list, env=tmp_env, timeout=timeout, out_on=False, err_on=False)
        else:
            retcode, out, err = DriversUtils.execute_and_get_retcode_out_err(prog=prog, args_list=args_list, env=tmp_env, timeout=timeout, merge_err_to_out=True)
            collected_output.append(retcode)
            collected_output.append(out)
    except (ValueError, OSError) as e:
        return GlobalConstants.TEST_EXECUTION_ERROR

    hasfail = False
    hasfail |= retcode != 0
    if hasfail:
        return GlobalConstants.FAIL_TEST_VERDICT
    return GlobalConstants.PASS_TEST_VERDICT