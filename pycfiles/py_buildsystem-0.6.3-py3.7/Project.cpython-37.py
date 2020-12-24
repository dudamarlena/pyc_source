# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Project\Project.py
# Compiled at: 2019-06-15 04:57:33
# Size of source mod 2**32: 2150 bytes
from py_buildsystem.common import logger
import py_buildsystem.Step.StepFactory as StepFactory
import py_buildsystem.ConfigReader.ConfigReader as ConfigReader

class Project(ConfigReader):

    def __init__(self, project_config_file, toolchain):
        logger.debug('Reading project configuration file.')
        ConfigReader.__init__(self, project_config_file)
        self._Project__project_name = project_config_file.replace('\\', '/').split('/')[(-1)].split('.')[0]
        self._Project__toolchain = toolchain
        self._Project__toolchain.get_compiler().set_defines(self._Project__defines)
        self._Project__toolchain.get_compiler().set_includes(self._Project__includes)
        self._parse_steps_list()
        self.run()

    def _check_config(self):
        try:
            self._Project__defines = self.configuration['defines']
        except KeyError:
            logger.debug('defines not set')
            self._Project__defines = []

        try:
            self._Project__includes = self.configuration['includes']
        except KeyError:
            logger.debug('defines not set')
            self._Project__includes = []

        try:
            self._Project__steps_list = self.configuration['steps']
        except KeyError:
            logger.debug('steps not set')
            self._Project__steps_list = []

        self._Project__steps = []

    def get_project_name(self):
        return self._Project__project_name

    def get_defines(self):
        return self._Project__defines

    def get_includes(self):
        return self._Project__includes

    def _parse_steps_list(self):
        for step in self._Project__steps_list:
            self._Project__steps.append(StepFactory.create(step, object_to_inject=(self._Project__toolchain)))

    def run(self):
        logger.info('Starting ' + self._Project__project_name + ' project')
        for step in self._Project__steps:
            logger.info('Performing ' + step.get_type() + ' ' + step.get_name())
            step.perform()
            logger.info('Finished ' + step.get_type() + ' ' + step.get_name())

    def get_exit_codes(self):
        return [step.get_exit_code() for step in self._Project__steps]