# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Step\StepLink.py
# Compiled at: 2019-06-15 04:50:16
# Size of source mod 2**32: 1815 bytes
import os
from py_buildsystem.common import logger
import py_buildsystem.Step.Step as Step
import py_buildsystem.FilesFinder.FilesFinder as FilesFinder

class StepLink(Step):

    def __init__(self, step_config, step_name, linker):
        self.configuration = step_config
        self._check_config()
        self.linker = linker
        self.step_name = step_name
        self.files_finder = FilesFinder(list_of_paths_to_search=(self._StepLink__source_directories))
        self.files_finder.set_files_extentions(self._StepLink__types)

    def _check_config(self):
        try:
            self._StepLink__source_directories = self.configuration['source_directories']
        except KeyError:
            logger.error('No source directories given')
            exit(-1)

        try:
            self._StepLink__output_file = self.configuration['output_file']
        except KeyError:
            logger.error('No output directory given')
            exit(-1)

        try:
            self._StepLink__types = self.configuration['types']
        except KeyError:
            logger.error('No type given')
            exit(-1)

        try:
            self._StepLink__additional_flags = self.configuration['additional_flags']
        except KeyError:
            logger.debug('additional_flags not set.')
            self._StepLink__additional_flags = []

    def get_type(self):
        return 'link'

    def perform(self):
        self._create_output_directory()
        self._find_files()
        self.exit_code = self.linker.link(self._StepLink__files_to_compile, self._StepLink__output_file, self._StepLink__additional_flags)

    def _find_files(self):
        self._StepLink__files_to_compile = self.files_finder.search()

    def _create_output_directory(self):
        os.makedirs((os.path.dirname(self._StepLink__output_file)), exist_ok=True)