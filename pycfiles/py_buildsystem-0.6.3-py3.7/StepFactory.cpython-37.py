# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Step\StepFactory.py
# Compiled at: 2019-06-15 04:46:41
# Size of source mod 2**32: 1030 bytes
from py_buildsystem.common import logger
import py_buildsystem.Step.StepCommand as StepCommand
import py_buildsystem.Step.StepCompile as StepCompile
import py_buildsystem.Step.StepLink as StepLink
import py_buildsystem.Step.StepGit as StepGit

class StepFactory:

    @staticmethod
    def create(step_config, object_to_inject=None):
        step_identifier = list(step_config.keys())[0].split(' ')
        step_type = step_identifier[0]
        step_name = ' '.join(step_identifier[1:])
        if 'compile' in step_type:
            return StepCompile(step_config, step_name, object_to_inject.get_compiler())
        if 'link' in step_type:
            return StepLink(step_config, step_name, object_to_inject.get_linker())
        if 'git' in step_type:
            return StepGit(step_config, step_name)
        if 'command' in step_type:
            return StepCommand(step_config, step_name)
        logger.error('Unsuported step type')
        exit(-1)