# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/repositoryandcode/code_transformations/llvm.py
# Compiled at: 2019-09-19 05:11:43
# Size of source mod 2**32: 1095 bytes
from __future__ import print_function
import sys, os, logging, shutil, muteria.common.mix as common_mix, muteria.repositoryandcode.codes_convert_support as ccs
ERROR_HANDLER = common_mix.ErrorHandler
__all__ = [
 'FromLLVMBitcode']

class FromLLVMBitcode(ccs.BaseCodeFormatConverter):

    def __init__(self):
        self.src_formats = [
         ccs.CodeFormats.LLVM_BITCODE]
        self.dest_formats = [
         ccs.CodeFormats.LLVM_BITCODE,
         ccs.CodeFormats.OBJECT_FILE,
         ccs.CodeFormats.NATIVE_CODE]

    def convert_code(self, src_fmt, dest_fmt, file_src_dest_map, repository_manager):
        ERROR_HANDLER.error_exit('Must Implement', __file__)

    def get_source_formats(self):
        return self.src_formats

    def get_destination_formats_for(self, src_fmt):
        return self.dest_formats