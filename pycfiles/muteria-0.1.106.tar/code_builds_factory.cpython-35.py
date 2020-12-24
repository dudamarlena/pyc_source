# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/repositoryandcode/code_builds_factory.py
# Compiled at: 2019-12-05 11:36:54
# Size of source mod 2**32: 11846 bytes
"""
"""
from __future__ import print_function
import sys, os, logging, shutil, muteria.common.mix as common_mix, muteria.common.fs as common_fs, muteria.repositoryandcode.code_transformations as ct_modules, muteria.repositoryandcode.codes_convert_support as ccs
from muteria.repositoryandcode.callback_object import DefaultCallbackObject
ERROR_HANDLER = common_mix.ErrorHandler
formatfrom_function_tuples = [
 (
  ccs.CodeFormats.C_SOURCE, ct_modules.c_cpp.FromC()),
 (
  ccs.CodeFormats.C_PREPROCESSED_SOURCE, ct_modules.c_cpp.FromC()),
 (
  ccs.CodeFormats.CPP_SOURCE, ct_modules.c_cpp.FromCpp()),
 (
  ccs.CodeFormats.CPP_PREPROCESSED_SOURCE, ct_modules.c_cpp.FromCpp()),
 (
  ccs.CodeFormats.LLVM_BITCODE, ct_modules.llvm.FromLLVMBitcode()),
 (
  ccs.CodeFormats.JAVASCRIPT_SOURCE, ccs.IdentityCodeConverter()),
 (
  ccs.CodeFormats.PYTHON_SOURCE, ccs.IdentityCodeConverter())]

class CodeBuildsFactory(object):

    def __init__(self, repository_manager, workdir=None):
        self.repository_manager = repository_manager
        self.workdir = workdir
        self.src_dest_fmt_to_handling_obj = {}
        self.code_conversion_tracker_file = None
        self.stored_files_mapping = None
        self.stored_files_mapping_file = None
        if self.workdir is not None:
            self.repo_path_saved_file = os.path.join(self.workdir, 'saved_repo_path')
            self.code_conversion_tracker_file = os.path.join(self.workdir, 'is_converting')
            self.stored_files_mapping_file = os.path.join(self.workdir, 'files_map')
            exes, src_obj_map = self.repository_manager.get_relative_exe_path_map()
            if os.path.isdir(self.workdir):
                tmp = common_fs.loadJSON(self.stored_files_mapping_file)
                self.stored_files_mapping = {k:os.path.join(self.workdir, v) for k, v in tmp.items()}
        else:
            count = 0
            self.stored_files_mapping = {}
            tmp = {}
            for f in exes:
                tmp[f] = str(count)
                self.stored_files_mapping[f] = os.path.join(self.workdir, str(count))
                count += 1

            for s, o in list(src_obj_map.items()):
                tmp[o] = str(count)
                self.stored_files_mapping[o] = os.path.join(self.workdir, str(count))
                count += 1

            os.mkdir(self.workdir)
            common_fs.dumpJSON(tmp, self.stored_files_mapping_file, pretty=True)
        for src_fmt, obj_cls in formatfrom_function_tuples:
            if isinstance(obj_cls, ccs.IdentityCodeConverter):
                self._fmt_from_to_registration(src_fmt, src_fmt, obj_cls)
            else:
                ERROR_HANDLER.assert_true(src_fmt in obj_cls.get_source_formats(), '{} {} {} {}'.format("Error in 'formatfrom_function_tuples'", 'src_fmt', src_fmt, 'not in corresponding obj...'), __file__)
                for dest_fmt in obj_cls.get_destination_formats_for(src_fmt):
                    self._fmt_from_to_registration(src_fmt, dest_fmt, obj_cls)

    def _fmt_from_to_registration(self, src_fmt, dest_fmt, handling_obj):
        if src_fmt not in self.src_dest_fmt_to_handling_obj:
            self.src_dest_fmt_to_handling_obj[src_fmt] = {}
        ERROR_HANDLER.assert_true(dest_fmt not in self.src_dest_fmt_to_handling_obj[src_fmt], 'dest_fmt {} added twice for same src_fmt {}'.format(src_fmt, dest_fmt), __file__)
        self.src_dest_fmt_to_handling_obj[src_fmt][dest_fmt] = handling_obj

    def transform_src_into_dest(self, src_fmt, dest_fmt, src_dest_files_paths_map, **kwargs):
        ERROR_HANDLER.assert_true(src_fmt in self.src_dest_fmt_to_handling_obj, 'src_fmt {} not supported yet.'.format(src_fmt), __file__)
        ERROR_HANDLER.assert_true(dest_fmt in self.src_dest_fmt_to_handling_obj[src_fmt], 'dest_fmt {} not supported yet for src_fmt {}.'.format(dest_fmt, src_fmt), __file__)
        handler = self.src_dest_fmt_to_handling_obj[src_fmt][dest_fmt]
        if self.repository_manager.should_build():
            with open(self.code_conversion_tracker_file, 'w') as (f):
                f.write('converting code...')
        pre_ret, ret, post_ret = handler.convert_code(src_fmt, dest_fmt, src_dest_files_paths_map, repository_manager=self.repository_manager, **kwargs)
        if self.repository_manager.should_build():
            os.remove(self.code_conversion_tracker_file)
        return (pre_ret, ret, post_ret)

    def override_registration(self, src_fmt, dest_fmt, handling_obj):
        """set another obj to handle src dest pair or a new one
        """
        if src_fmt in self.src_dest_fmt_to_handling_obj and dest_fmt in self.src_dest_fmt_to_handling_obj[src_fmt]:
            del self.src_dest_fmt_to_handling_obj[src_fmt][dest_fmt]
        self._fmt_from_to_registration(src_fmt, dest_fmt, handling_obj)

    class CopyCallbackObject(DefaultCallbackObject):

        def before_command(self):
            revert_src_func = self.pre_callback_args
            revert_src_func()
            return common_mix.GlobalConstants.COMMAND_SUCCESS

        def after_command(self):
            if self.op_retval == common_mix.GlobalConstants.COMMAND_FAILURE:
                return common_mix.GlobalConstants.COMMAND_FAILURE
            file_src_dest_map, reverse = self.post_callback_args
            if reverse:
                self._copy_to_repo(file_src_dest_map[0])
            else:
                self._copy_from_repo(file_src_dest_map[0])
                self._copy_from_repo(file_src_dest_map[1])
            return common_mix.GlobalConstants.COMMAND_SUCCESS

    def set_repo_to_build_default(self, also_copy_to_map={}):
        if self.repository_manager.should_build():
            files_backed = False
            if self.stored_files_mapping is not None and len(self.stored_files_mapping) > 0:
                if os.path.isfile(self.code_conversion_tracker_file):
                    for _, savef in self.stored_files_mapping.items():
                        if os.path.isfile(savef):
                            os.remove(savef)

                files_backed = os.path.isfile(self.stored_files_mapping[list(self.stored_files_mapping.keys())[0]])
                copy_callback_obj = self.CopyCallbackObject()
                copy_callback_obj.set_pre_callback_args(self.repository_manager.revert_src_list_files)
            new_repo_path = self.repository_manager.get_repository_dir_path()
            if os.path.isfile(self.repo_path_saved_file):
                with open(self.repo_path_saved_file) as (f):
                    old_repo_path = f.read().strip()
                if new_repo_path != old_repo_path:
                    files_backed = False
            else:
                files_backed = False
            if files_backed:
                copy_callback_obj.set_post_callback_args([
                 (
                  self.stored_files_mapping, also_copy_to_map),
                 True])
                b_ret, a_ret = self.repository_manager.custom_read_access(copy_callback_obj)
                ERROR_HANDLER.assert_true(b_ret == common_mix.GlobalConstants.COMMAND_SUCCESS & a_ret == common_mix.GlobalConstants.COMMAND_SUCCESS, 'code copy failed', __file__)
                for src, dest in also_copy_to_map.items():
                    try:
                        shutil.copy2(self.stored_files_mapping[src], dest)
                    except PermissionError:
                        os.remove(dest)
                        shutil.copy2(self.stored_files_mapping[src], dest)

            else:
                if self.stored_files_mapping is None:
                    copy_callback_obj.set_post_callback_args([({}, also_copy_to_map), False])
                    co = copy_callback_obj
                else:
                    copy_callback_obj.set_post_callback_args([
                     (
                      self.stored_files_mapping, also_copy_to_map),
                     False])
                    co = copy_callback_obj
                    with open(self.repo_path_saved_file, 'w') as (f):
                        f.write(new_repo_path)
                pre, ret, post = self.repository_manager.build_code(clean_tmp=True, reconfigure=True, callback_object=co)
                if pre == common_mix.GlobalConstants.COMMAND_FAILURE:
                    ERROR_HANDLER.error_exit('default build failed (pre).', __file__)
                if ret == common_mix.GlobalConstants.COMMAND_FAILURE:
                    ERROR_HANDLER.error_exit('default build failed (ret).', __file__)
                if post == common_mix.GlobalConstants.COMMAND_FAILURE:
                    ERROR_HANDLER.error_exit('default build failed (post).', __file__)
        else:
            ERROR_HANDLER.error_exit('TODO: implement baking relevant files')