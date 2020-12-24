# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_cloners/mercurial_repository_cloner.py
# Compiled at: 2019-04-26 07:28:00
# Size of source mod 2**32: 1805 bytes
from .i_repository_cloner import IRepositoryCloner
import hglib, os, re, logging
REGEX_REPO_NAME = '\\/([^/]+)\\/*$'
REGEX_REPO_NAME_GROUP = 1

class MercurialRepositoryCloner(IRepositoryCloner):
    __doc__ = '\n    Clones mercurial-repositories.\n    '

    def __init__(self, settings: dict):
        """
        Creates a new instance of the MercurialRepositoryCloner class.
        :param settings: settings including keys analysis_workspace (path) and repository_folder (folder in
        analysis_workspace)
        """
        self._MercurialRepositoryCloner__settings = settings

    def clone_repositories(self, repository_set: set) -> None:
        directory = self._MercurialRepositoryCloner__settings['analysis_workspace'] + self._MercurialRepositoryCloner__settings['repository_folder'] + 'hg/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for url in repository_set:
            regex_result = re.search(REGEX_REPO_NAME, url)
            repo_name = regex_result.group(REGEX_REPO_NAME_GROUP)
            logging.info('[MercurialRepositoryCloner]: Cloning repository ' + repo_name + ' from ' + url + '...')
            try:
                repo_directory = directory + repo_name
                if not os.path.exists(repo_directory):
                    os.makedirs(repo_directory)
                hglib.clone(url, repo_directory)
            except hglib.error.CommandError:
                logging.warning('[MercurialRepositoryCloner]: Could not clone repository ' + repo_name)

    def clones(self) -> str:
        return 'hg'