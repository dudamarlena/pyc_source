# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Toolchain\Compiler\Compiler.py
# Compiled at: 2019-06-15 07:55:29
# Size of source mod 2**32: 2264 bytes
import subprocess
from py_buildsystem.common import logger

class Compiler:

    def __init__(self, compiler_path, define_flag, output_flag, compile_flag, include_flag):
        self._Compiler__compiler_path = compiler_path
        self._Compiler__define_flag = define_flag
        self._Compiler__output_flag = output_flag
        self._Compiler__compile_flag = compile_flag
        self._Compiler__include_flag = include_flag
        self._Compiler__flags = []
        self._Compiler__defines = []
        self._Compiler__includes = []

    def set_flags(self, list_of_flags):
        self._Compiler__flags = list_of_flags

    def set_defines(self, list_of_defines):
        self._Compiler__defines = list_of_defines

    def set_includes(self, list_of_includes):
        self._Compiler__includes = list_of_includes

    def compile(self, list_of_files, output_directory, list_of_additional_flags=[], list_of_additional_defines=[], list_of_additionals_includes=[]):
        exit_code = 0
        flags = self._Compiler__flags + list_of_additional_flags + [self._Compiler__compile_flag]
        defines = self._compose_defines(self._Compiler__defines + list_of_additional_defines)
        includes = self._compose_includes(self._Compiler__includes + list_of_additionals_includes)
        for file in list_of_files:
            output_file_name = file.split('/')[(-1)]
            output_file_name = output_file_name.split('.')[0] + '.o'
            output_flag = self._Compiler__output_flag + '/'.join([output_directory, output_file_name])
            logger.debug('Compiling: ' + file)
            command = [self._Compiler__compiler_path] + flags + defines + includes + [output_flag] + [file]
            exit_code += subprocess.call(command)

        if exit_code != 0:
            return -1
        return 0

    def _compose_defines(self, list_of_defines):
        composed_defines = []
        for define in list_of_defines:
            composed_defines.append(self._Compiler__define_flag + define)

        return composed_defines

    def _compose_includes(self, list_of_includes):
        composed_includes = []
        for include in list_of_includes:
            composed_includes.append(self._Compiler__include_flag + include)

        return composed_includes