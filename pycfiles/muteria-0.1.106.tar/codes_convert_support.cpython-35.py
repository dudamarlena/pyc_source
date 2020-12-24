# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/repositoryandcode/codes_convert_support.py
# Compiled at: 2019-09-19 05:11:43
# Size of source mod 2**32: 3216 bytes
from __future__ import print_function
import os, sys, logging, shutil, abc, muteria.common.mix as common_mix
from muteria.repositoryandcode.callback_object import DefaultCallbackObject
ERROR_HANDLER = common_mix.ErrorHandler

class CodeFormats(common_mix.EnumAutoName):
    NATIVE_CODE = 'NATIVE_CODE'
    OBJECT_FILE = 'OBJECT_FILE'
    ASSEMBLY_CODE = 'ASSEMBLY_CODE'
    LLVM_BITCODE = 'LLVM_BITCODE'
    C_SOURCE = 'C_SOURCE'
    C_PREPROCESSED_SOURCE = 'C_PREPROCESSED_SOURCE'
    CPP_SOURCE = 'CPP_SOURCE'
    CPP_PREPROCESSED_SOURCE = 'CPP_PREPROCESSED_SOURCE'
    JAVA_SOURCE = 'JAVA_SOURCE'
    JAVA_BITCODE = 'JAVA_BITCODE'
    PYTHON_SOURCE = 'PYTHON_SOURCE'
    JAVASCRIPT_SOURCE = 'JAVASCRIPT_SOURCE'


class BaseCodeFormatConverter(abc.ABC):

    @abc.abstractmethod
    def convert_code(self, src_fmt, dest_fmt, file_src_dest_map, repository_manager, **kwargs):
        pass

    @abc.abstractmethod
    def get_source_formats(self):
        pass

    @abc.abstractmethod
    def get_destination_formats_for(self, src_fmt):
        pass


class IdentityCodeConverter(BaseCodeFormatConverter):

    class CopyCallbackObject(DefaultCallbackObject):

        def after_command(self):
            file_src_dest_map = self.post_callback_args
            self._copy_from_repo(file_src_dest_map)
            return DefaultCallbackObject.after_command(self)

    def convert_code(self, src_fmt, dest_fmt, file_src_dest_map, repository_manager, **kwargs):
        ERROR_HANDLER.assert_true(src_fmt == dest_fmt, 'different formats', __file__)
        ERROR_HANDLER.assert_true(len(file_src_dest_map) == len({file_src_dest_map[fn] for fn in file_src_dest_map}), 'Must specify one destination for each file', __file__)
        copy_callback_obj = self.CopyCallbackObject()
        copy_callback_obj.set_post_callback_args(file_src_dest_map)
        b_ret, a_ret = repository_manager.custom_read_access(copy_callback_obj)
        ERROR_HANDLER.assert_true(b_ret == common_mix.GlobalConstants.COMMAND_SUCCESS & a_ret == common_mix.GlobalConstants.COMMAND_SUCCESS, 'code copy failed', __file__)
        return (b_ret, common_mix.GlobalConstants.COMMAND_UNCERTAIN, a_ret)

    def get_source_formats(self):
        ERROR_HANDLER.error_exit('get_source_formats must not be called here', __file__)

    def get_destination_formats_for(self, src_fmt):
        ERROR_HANDLER.error_exit('get_destination_formats must not be called here', __file__)