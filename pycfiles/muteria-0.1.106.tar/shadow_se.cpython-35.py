# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/testgeneration/tools_by_languages/c/shadow_se/shadow_se.py
# Compiled at: 2019-12-17 08:04:35
# Size of source mod 2**32: 14097 bytes
from __future__ import print_function
import os, sys, glob, shutil, logging, re, muteria.common.fs as common_fs, muteria.common.mix as common_mix, muteria.common.matrices as common_matrices, muteria.controller.explorer as fd_structure, muteria.drivers.criteria as criteria
from muteria.repositoryandcode.codes_convert_support import CodeFormats
from muteria.drivers.testgeneration.base_testcasetool import BaseTestcaseTool
from muteria.drivers.testgeneration.testcases_info import TestcasesInfoObject
from muteria.drivers import DriversUtils
from muteria.repositoryandcode.callback_object import DefaultCallbackObject
from muteria.drivers.testgeneration.tools_by_languages.c.klee.klee import TestcasesToolKlee
ERROR_HANDLER = common_mix.ErrorHandler

class TestcasesToolShadowSE(TestcasesToolKlee):
    __doc__ = " Make sure to set the path to binarydir in user customs to use this\n        The path to binary should be set to the path to the shadow \n        directory. in Shadow VM, it should be '/home/shadowvm/shadow'\n    "

    def __init__(self, *args, **kwargs):
        TestcasesToolKlee.__init__(self, *args, **kwargs)
        ERROR_HANDLER.assert_true(self.custom_binary_dir is not None, 'Custom binary dir must be set for shadow', __file__)
        self.shadow_folder_path = os.sep.join(os.path.abspath(self.custom_binary_dir).split(os.sep)[:-3])
        self.llvm_29_compiler_path = os.path.join(self.shadow_folder_path, 'kleeDeploy/llvm-2.9/Release+Asserts/bin')
        self.llvm_gcc_path = os.path.join(self.shadow_folder_path, 'kleeDeploy/llvm-gcc4.2-2.9-x86_64-linux/bin')
        self.wllvm_path = os.path.join(self.shadow_folder_path, 'kleeDeploy/whole-program-llvm')
        self.klee_change_locs_list_file = os.path.join(self.tests_working_dir, 'klee_change_locs.json')
        self.replay_using_src_test = False
        self.keep_first_test = False

    def set_keep_first_test(self, bool_val):
        ERROR_HANDLER.assert_true(type(bool_val) == bool, 'invalid bool_val type. Must be bool', __file__)
        self.keep_first_test = bool_val

    def _get_default_params(self):
        bool_params = {'-ignore-solver-failures': None, 
         '-allow-external-sym-calls': True, 
         '-posix-runtime': True, 
         '-dump-states-on-halt': True, 
         '--zest': True, 
         '--shadow': True, 
         '-emit-all-errors': True, 
         '-no-std-out': True, 
         '-shadow-allow-allocs': True, 
         '-watchdog': True, 
         '-shadow-replay-standalone': False, 
         '-shadow-only-symbolic-tests': True}
        key_val_params = {'-search': None, 
         '-max-memory': None, 
         '-max-time': self.config.TEST_GENERATION_MAXTIME, 
         '-libc': 'uclibc', 
         '-use-shadow-version': 'product', 
         '-program-name': None}
        return (
         bool_params, key_val_params)

    def _get_sym_args(self):
        default_sym_args = []
        klee_sym_args = default_sym_args
        return klee_sym_args

    def _get_back_llvm_compiler(self):
        return 'clang'

    def _get_back_llvm_compiler_path(self):
        return self.llvm_29_compiler_path

    def _call_generation_run(self, runtool, args):
        for d in os.listdir(self.tests_working_dir):
            if d.startswith('klee-out-'):
                shutil.rmtree(os.path.join(self.tests_working_dir, d))

        call_shadow_wrapper_file = os.path.join(self.tests_working_dir, 'shadow_wrap')
        test_list = list(self.code_builds_factory.repository_manager.get_dev_tests_list())
        devtest_toolalias = self.parent_meta_tool.get_devtest_toolalias()
        klee_change_stmts = []
        get_lines_callback_obj = self.GetLinesCallbackObject()
        get_lines_callback_obj.set_pre_callback_args(self.code_builds_factory.repository_manager.revert_src_list_files)
        get_lines_callback_obj.set_post_callback_args(klee_change_stmts)
        pre_ret, post_ret = self.code_builds_factory.repository_manager.custom_read_access(get_lines_callback_obj)
        ERROR_HANDLER.assert_true(pre_ret == common_mix.GlobalConstants.COMMAND_SUCCESS, 'pre failed', __file__)
        ERROR_HANDLER.assert_true(post_ret == common_mix.GlobalConstants.COMMAND_SUCCESS, 'post failed', __file__)
        ERROR_HANDLER.assert_true(len(klee_change_stmts) > 0, 'No klee_change statement in the sources', __file__)
        stmt_cov_mat_file = self.head_explorer.get_file_pathname(fd_structure.CRITERIA_MATRIX[criteria.TestCriteria.STATEMENT_COVERAGE])
        cov_tests = None
        if os.path.isfile(stmt_cov_mat_file):
            stmt_cov_mat = common_matrices.ExecutionMatrix(filename=stmt_cov_mat_file)
            tmp_test_list = []
            for mt in stmt_cov_mat.get_nonkey_colname_list():
                alias, t = DriversUtils.reverse_meta_element(mt)
                if alias == devtest_toolalias:
                    tmp_test_list.append(t)

            test_list = tmp_test_list
            meta_stmts = list(stmt_cov_mat.get_keys())
            tool_aliases = set()
            for meta_stmt in meta_stmts:
                alias, stmt = DriversUtils.reverse_meta_element(meta_stmt)
                tool_aliases.add(alias)

            klee_change_meta_stmts = []
            for alias in tool_aliases:
                klee_change_meta_stmts += [DriversUtils.make_meta_element(e, alias) for e in klee_change_stmts]

            klee_change_meta_stmts = list(set(meta_stmts) & set(klee_change_meta_stmts))
            cov_tests = set()
            if len(klee_change_meta_stmts) > 0:
                for _, t in stmt_cov_mat.query_active_columns_of_rows(row_key_list=klee_change_meta_stmts).items():
                    cov_tests |= set(t)

        else:
            logging.warning('No test covers the patch (SHADOW)!')
        os.mkdir(self.tests_storage_dir)
        cand_testpair_list = []
        for test in test_list:
            meta_test = DriversUtils.make_meta_element(test, devtest_toolalias)
            if cov_tests is not None and meta_test not in cov_tests:
                pass
            else:
                cand_testpair_list.append((test, meta_test))

        if len(cand_testpair_list) > 0:
            cur_max_time = float(self.get_value_in_arglist(args, 'max-time'))
            self.set_value_in_arglist(args, 'max-time', str(max(1, cur_max_time / len(cand_testpair_list))))
        with open(call_shadow_wrapper_file, 'w') as (wf):
            wf.write('#! /bin/bash\n\n')
            wf.write('ulimit -s unlimited\n')
            wf.write(' '.join(['exec', runtool] + args + ['"${@:1}"']) + '\n')
        os.chmod(call_shadow_wrapper_file, 509)
        exes, _ = self.code_builds_factory.repository_manager.get_relative_exe_path_map()
        ERROR_HANDLER.assert_true(len(exes) == 1, 'Must have a single exe', __file__)
        exe_path_map = {e:call_shadow_wrapper_file for e in exes}
        env_vars = {}
        self._dir_chmod777(self.tests_storage_dir)
        for test, meta_test in cand_testpair_list:
            self.parent_meta_tool.execute_testcase(meta_test, exe_path_map, env_vars, with_output_summary=False)
            test_out = os.path.join(self.tests_storage_dir, test.replace(os.sep, '_'))
            os.mkdir(test_out)
            for d in glob.glob(self.tests_working_dir + '/klee-out-*'):
                self._dir_chmod777(d)
                if not self.keep_first_test:
                    first_test = os.path.join(d, 'test000001.ktest')
                    if os.path.isfile(first_test):
                        shutil.move(first_test, first_test + '.disable')
                    shutil.move(d, test_out)

            ERROR_HANDLER.assert_true(len(list(os.listdir(test_out))) > 0, 'Shadow generated no test for tescase: ' + test, __file__)
            if os.path.islink(os.path.join(self.tests_working_dir, 'klee-last')):
                os.unlink(os.path.join(self.tests_working_dir, 'klee-last'))

        common_fs.dumpJSON(klee_change_stmts, self.klee_change_locs_list_file)

    class GetLinesCallbackObject(DefaultCallbackObject):

        def before_command(self):
            revert_src_func = self.pre_callback_args
            revert_src_func()
            return common_mix.GlobalConstants.COMMAND_SUCCESS

        def after_command(self):
            if self.op_retval == common_mix.GlobalConstants.COMMAND_FAILURE:
                return common_mix.GlobalConstants.COMMAND_FAILURE
            m_regex = re.compile('({}|{}|{})'.format('klee_change', 'klee_get_true', 'klee_get_false'))
            matched_lines = set()
            for src in self.source_files_to_objects:
                with open(os.path.join(self.repository_rootdir, src), encoding='UTF-8') as (f):
                    for lnum, line in enumerate(f.readlines()):
                        if m_regex.search(line) is not None:
                            matched_lines.add(DriversUtils.make_meta_element(str(lnum + 1), src))

            ret_lines = self.post_callback_args
            ret_lines.extend(matched_lines)
            return common_mix.GlobalConstants.COMMAND_SUCCESS

    def _get_testexec_extra_env_vars(self, testcase):
        pass

    def _do_generate_tests(self, exe_path_map, code_builds_factory, meta_criteria_tool_obj=None, max_time=None):
        env_path_bak = os.environ['PATH']
        os.environ['PATH'] = os.pathsep.join([self.llvm_gcc_path,
         self.wllvm_path, os.environ['PATH']])
        super(TestcasesToolShadowSE, self)._do_generate_tests(exe_path_map, code_builds_factory, meta_criteria_tool_obj=meta_criteria_tool_obj, max_time=max_time)
        os.environ['PATH'] = env_path_bak