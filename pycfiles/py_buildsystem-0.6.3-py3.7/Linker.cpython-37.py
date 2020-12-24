# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Toolchain\Linker\Linker.py
# Compiled at: 2019-06-15 04:59:44
# Size of source mod 2**32: 1180 bytes
import os, time, subprocess
from py_buildsystem.common import logger

class Linker:

    def __init__(self, linker_path, output_flag, command_line_file):
        self._Linker__linker_path = linker_path
        self._Linker__output_flag = output_flag
        self._Linker__command_line_file = command_line_file
        self._Linker__flags = []

    def set_flags(self, list_of_flags):
        self._Linker__flags = list_of_flags

    def link(self, list_of_files, output_file, list_of_additional_flags=[]):
        filename = str(int(time.time())) + 'linker_file'
        with open(filename, 'w') as (comand_line_file):
            logger.debug('Created ' + filename)
            for file in list_of_files:
                comand_line_file.write(' ' + file)
                logger.debug('Added ' + file)

        logger.debug('Linking {}'.format(list_of_files))
        command = [self._Linker__linker_path] + self._Linker__flags + [self._Linker__command_line_file + filename] + [self._Linker__output_flag + output_file] + list_of_additional_flags
        exit_code = subprocess.call(command)
        os.remove(filename)
        logger.debug('Removed ' + filename)
        return exit_code