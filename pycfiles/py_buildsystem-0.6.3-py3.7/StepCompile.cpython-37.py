# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Step\StepCompile.py
# Compiled at: 2019-06-15 04:59:01
# Size of source mod 2**32: 2208 bytes
import os
from py_buildsystem.common import logger
import py_buildsystem.Step.Step as Step
import py_buildsystem.FilesFinder.FilesFinder as FilesFinder

class StepCompile(Step):

    def __init__(self, step_config, step_name, compiler):
        self.configuration = step_config
        self._check_config()
        self.compiler = compiler
        self.step_name = step_name
        self.files_finder = FilesFinder(list_of_paths_to_search=(self._StepCompile__source_directories), search_subdirectories=(self._StepCompile__search_subdirectories))
        self.files_finder.set_files_extentions(self._StepCompile__types)

    def perform(self):
        self._create_outpu_directory()
        self._find_files()
        self.exit_code = self.compiler.compile(self._StepCompile__files_to_compile, self._StepCompile__output_directory, self._StepCompile__additional_flags)

    def get_type(self):
        return 'compile'

    def _check_config(self):
        try:
            self._StepCompile__source_directories = self.configuration['source_directories']
        except KeyError:
            logger.error('No source directories given')
            exit(-1)

        try:
            self._StepCompile__output_directory = self.configuration['output_direcotry']
        except KeyError:
            logger.error('No output directory given')
            exit(-1)

        try:
            self._StepCompile__types = self.configuration['types']
        except KeyError:
            logger.error('No type given')
            exit(-1)

        try:
            self._StepCompile__additional_flags = self.configuration['additional_flags']
        except KeyError:
            self._StepCompile__additional_flags = []

        try:
            self._StepCompile__search_subdirectories = self.configuration['search_subdirectories']
        except KeyError:
            self._StepCompile__search_subdirectories = True

    def _find_files(self):
        self._StepCompile__files_to_compile = self.files_finder.search()

    def _create_outpu_directory(self):
        logger.debug('Creating ' + self._StepCompile__output_directory)
        os.makedirs((self._StepCompile__output_directory), exist_ok=True)