# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/testgeneration/testcase_formats/ktest/ktest.py
# Compiled at: 2019-12-05 10:59:06
# Size of source mod 2**32: 12827 bytes
from __future__ import print_function
import os, sys, re, imp
from distutils.spawn import find_executable
import muteria.common.mix as common_mix
from muteria.drivers import DriversUtils
ERROR_HANDLER = common_mix.ErrorHandler

class KTestTestFormat(object):

    @classmethod
    def installed(cls, custom_binary_dir=None):
        """ Check that the tool is installed
            :return: bool reprenting whether the tool is installed or not 
                    (executable accessible on the path)
                    - True: the tool is installed and works
                    - False: the tool is not installed or do not work
        """
        for prog in (cls.tool,):
            if custom_binary_dir is not None:
                prog = os.path.join(custom_binary_dir, prog)
            if not DriversUtils.check_tool(prog=prog, args_list=['--version'], expected_exit_codes=[
             1]):
                return False

        return True

    @classmethod
    def get_test_replay_tool(cls, custom_replay_tool_binary_dir=None):
        if custom_replay_tool_binary_dir is None:
            kr_file = find_executable(cls.tool)
            ERROR_HANDLER.assert_true(kr_file is not None, 'Could not fine test replay tool on path', __file__)
        else:
            kr_file = os.path.join(custom_replay_tool_binary_dir, cls.tool)
            ERROR_HANDLER.assert_true(os.path.isfile(kr_file), 'replay tool not found in custom_binary_dir', __file__)
        return kr_file

    @classmethod
    def _get_replay_prog_args(cls, executable_file, test_file, custom_replay_tool_binary_dir=None):
        prog = cls.tool
        if custom_replay_tool_binary_dir is not None:
            prog = os.path.join(custom_replay_tool_binary_dir, prog)
            ERROR_HANDLER.assert_true(os.path.isfile(prog), 'The tool {} is missing from the specified dir {}'.format(cls.tool, custom_replay_tool_binary_dir), __file__)
        args = [executable_file, test_file]
        return (prog, args)

    @classmethod
    def execute_test(cls, executable_file, test_file, env_vars, timeout=None, collected_output=None, custom_replay_tool_binary_dir=None):
        prog, args = cls._get_replay_prog_args(executable_file, test_file, custom_replay_tool_binary_dir)
        tmp_env = os.environ.copy()
        if env_vars is not None:
            tmp_env.update(env_vars)
        if timeout is not None:
            tmp_env['KLEE_REPLAY_TIMEOUT'] = str(timeout)
        if collected_output is not None:
            retcode, out, err = DriversUtils.execute_and_get_retcode_out_err(prog=prog, args_list=args, env=tmp_env, merge_err_to_out=True)
            out = cls._remove_output_noise(out)
            collected_output.extend((
             retcode, out, retcode in cls.timedout_retcodes))
        else:
            retcode, out, err = DriversUtils.execute_and_get_retcode_out_err(prog=prog, args_list=args, env=tmp_env, out_on=False, err_on=False)
        if retcode in cls.timedout_retcodes + (
         DriversUtils.EXEC_SEGFAULT_OUT_RET_CODE,):
            verdict = common_mix.GlobalConstants.FAIL_TEST_VERDICT
        else:
            verdict = common_mix.GlobalConstants.PASS_TEST_VERDICT
        return verdict

    @classmethod
    def get_replay_test_wrapper_str(cls, exe_env_var, ktest_env_var, timeout_env_var, custom_replay_tool_binary_dir=None):
        prog, args = cls._get_replay_prog_args('${}'.format(exe_env_var), '${}'.format(ktest_env_var), custom_replay_tool_binary_dir)
        python_code = ';'.join(['import sys',
         'from muteria.drivers.testgeneration' + '.testcase_formats.ktest.ktest import KTestTestFormat',
         'r = KTestTestFormat._remove_output_noise(sys.stdin.read())',
         'print(r)'])
        bash_timeout_retcode = os.system('timeout 0.1 sleep 1')
        ret_str = '#! /bin/bash\n\n'
        ret_str += 'set -u\nset -o pipefail\n\n'
        ret_str += 'export KLEE_REPLAY_TIMEOUT={}\n'.format(timeout_env_var)
        ret_str += ' '.join([prog] + args) + ' 2>&1 | {} -c "{}"\n'.format(sys.executable, python_code)
        ret_str += 'exit_code=$?\n'
        ret_str += '{} -c "exit(not($exit_code in {}))" && exit_code={}\n'.format(sys.executable, cls.timedout_retcodes, bash_timeout_retcode)
        ret_str += 'exit $exit_code\n'
        return ret_str

    timedout_retcodes = (88, )
    tool = 'klee-replay'
    clean_everything_regex = re.compile('(' + '|'.join(['^EXIT STATUS: .* \\([0-9]+\\s+seconds\\)$', '' + tool + ': EXIT STATUS: .* \\([0-9]+\\s+seconds\\)$', '' + tool + ': received signal [0-9]+\\s+. ' + 'Killing monitored process\\(es\\)$', '^note: (pty|pipe) (master|slave): ', '' + tool + ': PTY (MASTER|SLAVE): EXIT STATUS: ', '^warning: check_file .*: .* ' + 'mismatch: [0-9]+ [vV][sS] [0-9]+$', '^RUNNING GDB: /usr/bin/gdb --pid [0-9]+ -q --batch', '^TIMEOUT: ATTEMPTING GDB EXIT$', '' + tool + ': TEST CASE: ', '' + tool + ': ARGS: ']) + ')')
    clean_part_regex = re.compile('(' + '|'.join(['^EXIT STATUS: .* \\([0-9]+\\s+seconds\\)$', '' + tool + ': EXIT STATUS: .* \\([0-9]+\\s+seconds\\)$', '' + tool + ': received signal [0-9]+\\s+. ' + 'Killing monitored process\\(es\\)$', '^note: (pty|pipe) (master|slave): ', '' + tool + ': PTY (MASTER|SLAVE): EXIT STATUS: ', '^warning: check_file .*: .* ' + 'mismatch: [0-9]+ [vV][sS] [0-9]+$', '^RUNNING GDB: /usr/bin/gdb --pid [0-9]+ -q --batch', '^TIMEOUT: ATTEMPTING GDB EXIT$']) + ')')

    @classmethod
    def _remove_output_noise(cls, out, clean_everything=True):
        res = []
        if clean_everything:
            regex = cls.clean_everything_regex
        else:
            regex = cls.clean_part_regex
        if out[(-1)] == '\n':
            out = out[:-1]
            last_char = '\n'
        else:
            last_char = ''
        for line in out.encode('utf-8', 'backslashreplace').splitlines():
            line = line.decode('utf-8', 'backslashreplace')
            if regex.search(line) is None:
                res.append(line)

        res = '\n'.join(res) + last_char
        return res

    ktest_extension = '.ktest'

    @classmethod
    def ktest_fdupes(cls, *args, custom_replay_tool_binary_dir=None):
        """
        This function computes the fdupes of the klee ktest directories 
        and ktest files given as arguments. 
        It requires that the files and directories passed as arguments exist

        :param *args: each argument is either a file or a directory that exists

        :return: returns two values: 
                - The first is a python list of tuples. 
                    each tuple represents files that are duplicate with each 
                    other and ranked by their age (modified time) the oldest 
                    first (earliest modified to latest modified).
                - The second is the list of files that are not valid
                    ktest files.
        """
        ktt_dir = os.path.dirname(cls.get_test_replay_tool(custom_replay_tool_binary_dir=custom_replay_tool_binary_dir))
        ktest_tool = imp.load_source('ktest-tool', os.path.join(ktt_dir, 'ktest-tool'))
        ret_fdupes = []
        invalid = []
        file_set = set()
        for file_dir in args:
            if os.path.isfile(file_dir):
                file_set.add(file_dir)
            else:
                if os.path.isdir(file_dir):
                    for root, directories, filenames in os.walk(file_dir):
                        for filename in filenames:
                            if filename.endswith(cls.ktest_extension):
                                file_set.add(os.path.join(root, filename))

                else:
                    ERROR_HANDLER.error_exit('Invalid file or dir passed (inexistant): ' + file_dir, __file__)

        kt2used_dat = {}
        for kf in file_set:
            try:
                b = ktest_tool.KTest.fromfile(kf)
                kt2used_dat[kf] = (b.args[1:], b.objects)
            except:
                invalid.append(kf)

        dup_dict = {}
        keys = list(kt2used_dat.keys())
        for ktest_file in keys:
            if ktest_file in kt2used_dat:
                ktest_file_dat = kt2used_dat[ktest_file]
                del kt2used_dat[ktest_file]
                for other_file in kt2used_dat:
                    if kt2used_dat[other_file] == ktest_file_dat:
                        if ktest_file not in dup_dict:
                            dup_dict[ktest_file] = []
                        dup_dict[ktest_file].append(other_file)

                if ktest_file in dup_dict:
                    for dup_of_kt_file in dup_dict[ktest_file]:
                        del kt2used_dat[dup_of_kt_file]

        for ktest_file in dup_dict:
            tmp = [
             ktest_file] + dup_dict[ktest_file]
            tmp.sort(key=lambda x: os.path.getmtime(x))
            ret_fdupes.append(tuple(tmp))

        return (ret_fdupes, invalid)