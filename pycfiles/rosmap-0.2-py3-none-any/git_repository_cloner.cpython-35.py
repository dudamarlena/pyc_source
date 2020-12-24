# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_cloners/git_repository_cloner.py
# Compiled at: 2019-04-26 09:00:27
# Size of source mod 2**32: 2337 bytes
from .i_repository_cloner import IRepositoryCloner
from git import Repo
from git import GitCommandError
from zipfile import ZipFile
import os, re, logging
from shutil import copy
REGEX_REPO_NAME = '\\/([^\\/]+?)\\/([^\\/]+?)\\.git'
REGEX_REPO_USER_GROUP = 1
REGEX_REPO_NAME_GROUP = 2

class GitRepositoryCloner(IRepositoryCloner):

    def __init__(self, settings: dict):
        self._GitRepositoryCloner__settings = settings

    def clone_repositories(self, repository_set: set) -> None:
        copy(os.path.dirname(os.path.realpath(__file__)) + '/git_askpass.py', self._GitRepositoryCloner__settings['analysis_workspace'])
        os.chmod(self._GitRepositoryCloner__settings['analysis_workspace'] + '/git_askpass.py', 511)
        os.environ['GIT_ASKPASS'] = self._GitRepositoryCloner__settings['analysis_workspace'] + '/git_askpass.py'
        print(os.environ['GIT_ASKPASS'])
        os.environ['GIT_USERNAME'] = self._GitRepositoryCloner__settings['github_username']
        os.environ['GIT_PASSWORD'] = self._GitRepositoryCloner__settings['github_password']
        if not os.path.exists(self._GitRepositoryCloner__settings['analysis_workspace'] + self._GitRepositoryCloner__settings['repository_folder'] + 'git/'):
            os.makedirs(self._GitRepositoryCloner__settings['analysis_workspace'] + self._GitRepositoryCloner__settings['repository_folder'] + 'git/')
        for url in repository_set:
            regex_result = re.search(REGEX_REPO_NAME, url)
            if regex_result is not None:
                repo_name = regex_result.group(REGEX_REPO_NAME_GROUP)
                user_name = regex_result.group(REGEX_REPO_USER_GROUP)
                logging.info('[GitRepositoryCloner]: Cloning repository ' + repo_name + ' from ' + url + '...')
                try:
                    directory = self._GitRepositoryCloner__settings['analysis_workspace'] + self._GitRepositoryCloner__settings['repository_folder'] + 'git/' + user_name + '_' + repo_name
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    Repo.clone_from(url, directory)
                except GitCommandError:
                    logging.warning('[GitRepositoryCloner]: Could not clone repository ' + repo_name)

    def clones(self) -> str:
        return 'git'