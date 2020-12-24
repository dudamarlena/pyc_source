# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/criteria/tools_by_languages/python/coverage_py/coverage.py
# Compiled at: 2019-11-25 05:17:07
# Size of source mod 2**32: 14774 bytes
from __future__ import print_function
import os, sys, re, shutil, glob, logging, configparser, muteria.common.mix as common_mix, muteria.common.fs as common_fs
from muteria.repositoryandcode.codes_convert_support import CodeFormats
from muteria.repositoryandcode.callback_object import DefaultCallbackObject
from muteria.drivers.criteria.base_testcriteriatool import BaseCriteriaTool
from muteria.drivers.criteria import TestCriteria
from muteria.drivers import DriversUtils
try:
    import coverage
except ImportError:
    pass

ERROR_HANDLER = common_mix.ErrorHandler

class CriteriaToolCoveragePy(BaseCriteriaTool):

    def __init__(self, *args, **kwargs):
        BaseCriteriaTool.__init__(self, *args, **kwargs)
        self.instrumentation_details = os.path.join(self.instrumented_code_storage_dir, '.instru.meta.json')
        self.cov_data_filename = 'cov_data.json'
        self.used_srcs_dir = os.path.join(self.instrumented_code_storage_dir, 'used_srcs_dir')
        self.preload_dir = os.path.join(self.instrumented_code_storage_dir, 'config_dir')
        self.preload_file = os.path.join(self.preload_dir, 'usercustomize.py')
        self.config_file = os.path.join(self.instrumented_code_storage_dir, '.configrc')
        self.raw_data_file = os.path.join(self.instrumented_code_storage_dir, '.rawdata')
        for file_ in glob.glob(self.raw_data_file + '*'):
            os.remove(file_)

    @classmethod
    def installed(cls, custom_binary_dir=None):
        """ Check that the tool is installed
            :return: bool reprenting whether the tool is installed or not 
                    (executable accessible on the path)
                    - True: the tool is installed and works
                    - False: the tool is not installed or do not work
        """
        try:
            import coverage
        except ImportError:
            return False

        return True

    @classmethod
    def _get_meta_instrumentation_criteria(cls):
        """ Criteria where all elements are instrumented in same file
            :return: list of citeria
        """
        return [
         TestCriteria.STATEMENT_COVERAGE,
         TestCriteria.BRANCH_COVERAGE]

    @classmethod
    def _get_separated_instrumentation_criteria(cls):
        """ Criteria where all elements are instrumented in different files
            :return: list of citeria
        """
        return []

    def get_instrumented_executable_paths_map(self, enabled_criteria):
        crit_to_exes_map = {}
        obj = common_fs.loadJSON(self.instrumentation_details)
        exes = obj
        for criterion in enabled_criteria:
            crit_to_exes_map[criterion] = exes

        return crit_to_exes_map

    def get_criterion_info_object(self, criterion):
        pass

    def _get_criterion_element_executable_path(self, criterion, element_id):
        ERROR_HANDLER.error_exit('not applicable for coverage_py', __file__)

    def _get_criterion_element_environment_vars(self, criterion, element_id):
        """
            return: python dictionary with environment variable as key
                     and their values as value (all strings)
        """
        ERROR_HANDLER.error_exit('not applicable for coverage_py', __file__)

    def _get_criteria_environment_vars(self, result_dir_tmp, enabled_criteria):
        """
        return: python dictionary with environment variable as key
                     and their values as value (all strings)
        """
        python_path = self.preload_dir
        if 'PYTHONPATH' is os.environ:
            python_path += ':' + os.environ['PYTHONPATH']
        return {criterion:{'PYTHONPATH': python_path, 'COVERAGE_PROCESS_START': self.config_file} for criterion in enabled_criteria}

    class PathAliases(object):

        def __init__(self, data_files, exe_rel_files, inst_top_dir, top_out_dir, repo_dir):
            repo_dir = os.path.join(os.path.normpath(repo_dir), '')
            top_out_dir = os.path.join(os.path.normpath(top_out_dir), '')
            prefix_dirs = (repo_dir, top_out_dir)
            self.alias_map = {}
            for _, dfile in enumerate(data_files):
                src = tmp = None
                for p_dir in prefix_dirs:
                    if dfile.startswith(p_dir):
                        tmp = dfile[len(p_dir):]
                        if tmp in exe_rel_files:
                            src = tmp
                            break

                if src is None:
                    ERROR_HANDLER.assert_true(tmp is None, 'The file {} {} {} {}'.format(dfile, 'is in the right dirs and in', 'coverage but was not specified.', 'Bug in coverage.py?'), __file__)
                    self.alias_map[dfile] = dfile
                else:
                    self.alias_map[dfile] = os.path.join(inst_top_dir, src)

        def map(self, in_dat_file):
            return self.alias_map[in_dat_file]

    def _collect_temporary_coverage_data(self, criteria_name_list, test_execution_verdict, used_environment_vars, result_dir_tmp, testcase):
        """ extract coverage data into json file in result_dir_tmp
        """
        cov_obj = coverage.Coverage(config_file=self.config_file)
        cov_obj.combine()
        tmp_dat_obj = cov_obj.get_data()
        in_dat_files = tmp_dat_obj.measured_files()
        try:
            self.exes_rel
        except AttributeError:
            obj = common_fs.loadJSON(self.instrumentation_details)
            self.exes_abs = []
            self.exes_rel = []
            for rp, ap in list(obj.items()):
                self.exes_rel.append(rp)
                self.exes_abs.append(ap)

            self.exes_rel, self.exes_abs = zip(*sorted(zip(self.exes_rel, self.exes_abs), key=lambda x: x.count(os.path.sep)))
            self.executable_lines = {}
            self.executable_arcs = {}
            for fn in self.exes_abs:
                pser = coverage.parser.PythonParser(filename=fn)
                pser.parse_source()
                self.executable_lines[fn] = pser.statements
                self.executable_arcs[fn] = pser.arcs()

        dat_obj = coverage.CoverageData()
        if len(in_dat_files) > 0:
            file_map = self.PathAliases(in_dat_files, self.exes_rel, self.used_srcs_dir, self._get_latest_top_output_dir(), self.code_builds_factory.repository_manager.repo_abs_path(''))
            dat_obj.update(tmp_dat_obj, aliases=file_map)
        res = {c:{} for c in criteria_name_list}
        if TestCriteria.STATEMENT_COVERAGE in criteria_name_list:
            for rel_fn, abs_fn in zip(self.exes_rel, self.exes_abs):
                res[TestCriteria.STATEMENT_COVERAGE][rel_fn] = {ln:0 for ln in self.executable_lines[abs_fn]}
                ln_list = dat_obj.lines(abs_fn)
                if ln_list is not None:
                    res[TestCriteria.STATEMENT_COVERAGE][rel_fn].update({ln:1 for ln in ln_list})

        if TestCriteria.BRANCH_COVERAGE in criteria_name_list:
            for rel_fn, abs_fn in zip(self.exes_rel, self.exes_abs):
                res[TestCriteria.BRANCH_COVERAGE][rel_fn] = {str(an):0 for an in self.executable_arcs[abs_fn]}
                an_list = dat_obj.arcs(abs_fn)
                if an_list is not None:
                    res[TestCriteria.BRANCH_COVERAGE][rel_fn].update({str(an):1 for an in an_list})

        res_str = {v.get_str():res[v] for v in res}
        common_fs.dumpJSON(res_str, os.path.join(result_dir_tmp, self.cov_data_filename))
        cov_obj.erase()
        for file_ in glob.glob(self.raw_data_file + '*'):
            os.remove(file_)

    def _extract_coverage_data_of_a_test(self, enabled_criteria, test_execution_verdict, result_dir_tmp):
        """ read json files and extract data
            return: the dict of criteria with covering count
        """
        in_file = os.path.join(result_dir_tmp, self.cov_data_filename)
        cov_dat_obj = common_fs.loadJSON(in_file)
        cov_dat_obj = {TestCriteria[v]:cov_dat_obj[v] for v in cov_dat_obj}
        ERROR_HANDLER.assert_true(set(cov_dat_obj) == set(enabled_criteria), 'mismatching criteria enabled', __file__)
        res = {c:{} for c in enabled_criteria}
        for c in cov_dat_obj:
            for filename, filedat in list(cov_dat_obj[c].items()):
                if filedat is not None:
                    for id_, cov in list(filedat.items()):
                        ident = DriversUtils.make_meta_element(str(id_), filename)
                        res[c][ident] = cov

        os.remove(in_file)
        return res

    def _do_instrument_code(self, exe_path_map, code_builds_factory, enabled_criteria, parallel_count=1):
        if os.path.isdir(self.instrumented_code_storage_dir):
            shutil.rmtree(self.instrumented_code_storage_dir)
        os.mkdir(self.instrumented_code_storage_dir)
        if os.path.isdir(self.used_srcs_dir):
            shutil.rmtree(self.used_srcs_dir)
        os.mkdir(self.used_srcs_dir)
        if os.path.isdir(self.preload_dir):
            shutil.rmtree(self.preload_dir)
        os.mkdir(self.preload_dir)
        rel_path_map = {}
        exes, src_inter_map = code_builds_factory.repository_manager.get_relative_exe_path_map()
        for f in src_inter_map:
            rel_path_map[f] = os.path.join(self.used_srcs_dir, f)
            relloc = os.path.join(self.used_srcs_dir, os.path.dirname(f))
            if not os.path.isdir(relloc):
                os.makedirs(relloc)

        not_none_dest = {k:v for k, v in list(rel_path_map.items())}
        pre_ret, ret, post_ret = code_builds_factory.transform_src_into_dest(src_fmt=CodeFormats.PYTHON_SOURCE, dest_fmt=CodeFormats.PYTHON_SOURCE, src_dest_files_paths_map=not_none_dest)
        ERROR_HANDLER.assert_true(not os.path.isfile(self.instrumentation_details), 'must not exist here', __file__)
        common_fs.dumpJSON(rel_path_map, self.instrumentation_details)
        if ret == common_mix.GlobalConstants.COMMAND_FAILURE:
            ERROR_HANDLER.error_exit('Problem with copying python sources', __file__)
        with open(self.preload_file, 'w') as (f):
            f.write('import coverage\ncoverage.process_startup()\n')
        concurrencies = ['thread', 'multiprocessing', 'gevent', 'greenlet',
         'eventlet']
        concurrency_support = 'thread'
        config = {}
        config['run'] = {'include': [os.path.join('*', v) for v in rel_path_map.keys()], 
         
         'data_file': self.raw_data_file, 
         'branch': TestCriteria.BRANCH_COVERAGE in enabled_criteria, 
         
         'parallel': True, 
         'concurrency': concurrency_support}
        with open(self.config_file, 'w') as (f):
            for k, v in list(config.items()):
                f.write('[' + k + ']' + '\n')
                for kk, vv in list(v.items()):
                    if type(vv) == list:
                        f.write(kk + ' = \n')
                        for vvv in vv:
                            f.write('\t' + str(vvv) + '\n')

                    else:
                        f.write(kk + ' = ' + str(vv) + '\n')