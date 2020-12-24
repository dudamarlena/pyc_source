# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/testgeneration/tools_by_languages/c/semu/semu.py
# Compiled at: 2019-12-17 08:12:18
# Size of source mod 2**32: 9660 bytes
from __future__ import print_function
import os, sys, glob, shutil, logging, resource, random, numpy as np, muteria.common.fs as common_fs, muteria.common.mix as common_mix, muteria.common.matrices as common_matrices, muteria.drivers.criteria as criteria, muteria.controller.explorer as fd_structure
from muteria.repositoryandcode.codes_convert_support import CodeFormats
from muteria.drivers.testgeneration.base_testcasetool import BaseTestcaseTool
from muteria.drivers.testgeneration.testcases_info import TestcasesInfoObject
from muteria.drivers import DriversUtils
from muteria.drivers.testgeneration.testcase_formats.ktest.ktest import KTestTestFormat
from muteria.drivers.testgeneration.tools_by_languages.c.klee.klee import TestcasesToolKlee
ERROR_HANDLER = common_mix.ErrorHandler

class TestcasesToolSemu(TestcasesToolKlee):

    @classmethod
    def installed(cls, custom_binary_dir=None):
        """ Check that the tool is installed
            :return: bool reprenting whether the tool is installed or not 
                    (executable accessible on the path)
                    - True: the tool is installed and works
                    - False: the tool is not installed or do not work
        """
        for prog in ('klee-semu', ):
            if custom_binary_dir is not None:
                prog = os.path.join(custom_binary_dir, prog)
            if not DriversUtils.check_tool(prog=prog, args_list=['--version'], expected_exit_codes=[
             0, 1]):
                return False

        return KTestTestFormat.installed(custom_binary_dir=custom_binary_dir)

    def __init__(self, *args, **kwargs):
        TestcasesToolKlee.__init__(self, *args, **kwargs)
        self.cand_muts_file = os.path.join(self.tests_working_dir, 'cand_muts_file.txt')
        self.sm_mat_file = self.head_explorer.get_file_pathname(fd_structure.CRITERIA_MATRIX[criteria.TestCriteria.STRONG_MUTATION])
        self.mutants_by_funcs = None

    def _get_default_params(self):
        bool_params = {'-ignore-solver-failures': None, 
         '-allow-external-sym-calls': True, 
         '-posix-runtime': True, 
         '-dump-states-on-halt': True, 
         '-only-output-states-covering-new': None, 
         '-use-cex-cache': True, 
         '-semu-disable-statediff-in-testgen': None, 
         '-semu-continue-mindist-out-heuristic': None, 
         '-semu-use-basicblock-for-distance': None, 
         '-semu-forkprocessfor-segv-externalcalls': True, 
         '-semu-testsgen-only-for-critical-diffs': None, 
         '-semu-consider-outenv-for-diffs': None}
        key_val_params = {'-output-dir': self.tests_storage_dir, 
         '-solver-backend': 'z3', 
         '-max-solver-time': '300', 
         '-search': 'bfs', 
         '-max-memory': None, 
         '-max-time': self.config.TEST_GENERATION_MAXTIME, 
         '-libc': 'uclibc', 
         '-max-sym-array-size': '4096', 
         '-max-instruction-time': '10.', 
         '-semu-mutant-max-fork': '0', 
         '-semu-checknum-before-testgen-for-discarded': '2', 
         '-semu-mutant-state-continue-proba': '0.25', 
         '-semu-precondition-length': '0', 
         '-semu-max-total-tests-gen': None, 
         '-semu-max-tests-gen-per-mutant': '5', 
         '-semu-loop-break-delay': '120.0'}
        key_val_params.update({})
        if os.path.isfile(self.sm_mat_file):
            key_val_params['-semu-candidate-mutants-list-file'] = self.cand_muts_file
        return (
         bool_params, key_val_params)

    def _call_generation_run(self, runtool, args):
        max_mutant_count_per_cluster = self.get_value_in_arglist(args, 'DRIVER_max_mutant_count_per_cluster')
        if max_mutant_count_per_cluster is None:
            max_mutant_count_per_cluster = 100
        else:
            max_mutant_count_per_cluster = float(max_mutant_count_per_cluster)
            self.remove_arg_and_value_from_arglist(args, 'DRIVER_max_mutant_count_per_cluster')
        cand_mut_file_bak = self.cand_muts_file + '.bak'
        mut_list = []
        with open(self.cand_muts_file) as (f):
            for m in f:
                m = m.strip()
                ERROR_HANDLER.assert_true(m.isdigit(), 'Invalid mutant ID', __file__)
                mut_list.append(m)

        random.shuffle(mut_list)
        nclust = int(len(mut_list) / max_mutant_count_per_cluster)
        if len(mut_list) != max_mutant_count_per_cluster * nclust:
            nclust += 1
        clusters = np.array_split(mut_list, nclust)
        if len(clusters) > 1:
            cur_max_time = float(self.get_value_in_arglist(args, 'max-time'))
            self.set_value_in_arglist(args, 'max-time', str(max(1, cur_max_time / len(clusters))))
        shutil.move(self.cand_muts_file, cand_mut_file_bak)
        c_dirs = []
        for c_id, clust in enumerate(clusters):
            logging.debug('SEMU: targeting mutant cluster {}/{} ...'.format(c_id + 1, len(clusters)))
            with open(self.cand_muts_file, 'w') as (f):
                for m in clust:
                    f.write(m + '\n')

            super(TestcasesToolSemu, self)._call_generation_run(runtool, args)
            c_dir = os.path.join(os.path.dirname(self.tests_storage_dir), str(c_id))
            shutil.move(self.tests_storage_dir, c_dir)
            c_dirs.append(c_dir)

        os.mkdir(self.tests_storage_dir)
        for c_dir in c_dirs:
            shutil.move(c_dir, self.tests_storage_dir)

        shutil.move(cand_mut_file_bak, self.cand_muts_file)

    def _get_tool_name(self):
        return 'klee-semu'

    def _get_input_bitcode_file(self, code_builds_factory, rel_path_map, meta_criteria_tool_obj=None):
        mutant_gen_tool_name = 'mart'
        mut_tool_alias_to_obj = meta_criteria_tool_obj.get_criteria_tools_by_name(mutant_gen_tool_name)
        if len(mut_tool_alias_to_obj) == 0:
            logging.warning('SEMu requires Mart to generate mutants but none used')
        ERROR_HANDLER.assert_true(len(mut_tool_alias_to_obj) == 1, 'SEMu supports tests generation froma single .bc file for now (todo).', __file__)
        t_alias2metamu_bc = {}
        t_alias2mutantInfos = {}
        for alias, obj in mut_tool_alias_to_obj.items():
            dest_bc = rel_path_map[list(rel_path_map)[0]] + '.bc'
            shutil.copy2(obj.get_test_gen_metamutant_bc(), dest_bc)
            t_alias2metamu_bc[alias] = dest_bc
            t_alias2mutantInfos[alias] = obj.get_criterion_info_object(None)

        self.mutants_by_funcs = {}
        single_alias = list(t_alias2mutantInfos)[0]
        single_tool_obj = t_alias2mutantInfos[single_alias]
        for mut in single_tool_obj.get_elements_list():
            func = single_tool_obj.get_element_data(mut)['mutant_function_name']
            if func not in self.mutants_by_funcs:
                self.mutants_by_funcs[func] = set()
            self.mutants_by_funcs[func].add(mut)

        if os.path.isfile(self.sm_mat_file):
            sm_mat = common_matrices.ExecutionMatrix(filename=self.sm_mat_file)
            mut2killing_tests = sm_mat.query_active_columns_of_rows()
            alive_muts = [m for m, k_t in mut2killing_tests.items() if len(k_t) == 0]
            with open(self.cand_muts_file, 'w') as (f):
                for meta_m in alive_muts:
                    t_alias, m = DriversUtils.reverse_meta_element(meta_m)
                    if t_alias in t_alias2metamu_bc:
                        f.write(str(m) + '\n')

        return t_alias2metamu_bc[list(t_alias2metamu_bc)[0]]

    def requires_criteria_instrumented(self):
        return True