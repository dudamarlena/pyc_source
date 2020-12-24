# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Step\StepGit.py
# Compiled at: 2019-06-15 06:50:21
# Size of source mod 2**32: 1311 bytes
import git
from py_buildsystem.common import logger
import py_buildsystem.Step.Step as Step

class StepGit(Step):

    def __init__(self, step_config, step_name):
        self.configuration = step_config
        self._check_config()
        self.step_name = step_name
        self.exit_code = 0

    def _check_config(self):
        try:
            self._StepGit__repository_location = self.configuration['repo_location']
        except KeyError:
            logger.error('No repository location given')
            exit(-1)

        try:
            self._StepGit__clone_destination = self.configuration['destination']
        except KeyError:
            logger.error('No clone destination given')
            exit(-1)

        try:
            self._StepGit__branch = self.configuration['branch']
        except KeyError:
            logger.debug('Pulling master branch')
            self._StepGit__branch = 'master'

    def get_type(self):
        return 'git'

    def perform(self):
        logger.info('Cloning ' + self._StepGit__repository_location + ' -- ' + self._StepGit__branch + ' to ' + self._StepGit__clone_destination)
        try:
            git.Repo.clone_from((self._StepGit__repository_location), (self._StepGit__clone_destination), branch=(self._StepGit__branch))
        except git.exc.GitCommandError:
            pass