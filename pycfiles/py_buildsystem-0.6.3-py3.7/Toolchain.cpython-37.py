# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Toolchain\Toolchain.py
# Compiled at: 2019-06-15 04:55:17
# Size of source mod 2**32: 3383 bytes
import os, yaml, subprocess
from py_buildsystem.common import logger
import py_buildsystem.Toolchain.Linker.Linker as Linker
import py_buildsystem.Toolchain.Compiler.Compiler as Compiler
import py_buildsystem.ConfigReader.ConfigReader as ConfigReader
path_to_configs = os.path.dirname(__file__).replace('\\', '/') + '/ToolchainsConfigs'

class Toolchain(ConfigReader):

    def __init__(self, config_yaml_file, path_to_toolchain=''):
        logger.debug('Reading toolchain configuration file.')
        ConfigReader.__init__(self, config_yaml_file)
        self._check_compiler_config_file()
        self._Toolchain__linker_path = os.path.join(path_to_toolchain, self._Toolchain__linker_name).replace('\\', '/')
        self._Toolchain__compiler_path = os.path.join(path_to_toolchain, self._Toolchain__compiler_name).replace('\\', '/')
        self._check_toolchain_path()
        self._Toolchain__compiler = Compiler(self._Toolchain__compiler_path, self._Toolchain__define_flag, self._Toolchain__output_flag, self._Toolchain__compile_flag, self._Toolchain__include_flag)
        self._Toolchain__compiler.set_flags(self._Toolchain__compiler_flags)
        self._Toolchain__linker = Linker(self._Toolchain__linker_path, self._Toolchain__output_flag, self._Toolchain__command_line_file)
        self._Toolchain__linker.set_flags(self._Toolchain__linker_flags)

    def get_compiler(self):
        return self._Toolchain__compiler

    def get_linker(self):
        return self._Toolchain__linker

    def _check_config(self):
        try:
            self._Toolchain__choosen_compiler = self.configuration['compiler']
        except KeyError:
            logger.error('You must provide compiler name in a compiler configuration file')
            exit(-1)

        try:
            self._Toolchain__compiler_flags = self.configuration['compiler_flags']
        except KeyError:
            logger.warning('no compiler_flags_set')
            self._Toolchain__compiler_flags = []

        try:
            self._Toolchain__linker_flags = self.configuration['linker_flags']
        except KeyError:
            logger.warning('no linker_flags')
            self._Toolchain__linker_flags = []

    def _check_compiler_config_file(self):
        try:
            with open(os.path.join(path_to_configs, self._Toolchain__choosen_compiler + '.yaml').replace('\\', '/'), 'r') as (compiler_config_file):
                compiler_config = yaml.load(compiler_config_file)
        except FileNotFoundError:
            logger.error('Configuration file for the compiler was not found.')
            exit(-1)

        self._Toolchain__compiler_name = compiler_config['compiler']
        self._Toolchain__linker_name = compiler_config['linker']
        self._Toolchain__define_flag = compiler_config['define_flag']
        self._Toolchain__output_flag = compiler_config['output_flag']
        self._Toolchain__compile_flag = compiler_config['compile_flag']
        self._Toolchain__include_flag = compiler_config['include_flag']
        self._Toolchain__version_flag = compiler_config['version_flag']
        self._Toolchain__command_line_file = compiler_config['comand_line_file']

    def _check_toolchain_path(self):
        try:
            subprocess.check_output([self._Toolchain__linker_path, self._Toolchain__version_flag])
            subprocess.check_output([self._Toolchain__compiler_path, self._Toolchain__version_flag])
        except FileNotFoundError:
            logger.error('Can not find the compilers executable, check if the compilers path is correct or if the compiler is in a PATH.')
            exit(-1)