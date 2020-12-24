# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_cloners/subversion_repository_cloner.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 2189 bytes
from .i_repository_cloner import IRepositoryCloner
import os, svn.remote, svn.exception, urllib3, logging

class SubversionRepositoryCloner(IRepositoryCloner):

    def __init__(self, settings: dict):
        """
        Creates a new instance of the SubversionRepositoryCloner-class.
        :param settings: settings including keys analysis_workspace (path) and repository_folder (folder in
        analysis_workspace)
        """
        self._SubversionRepositoryCloner__settings = settings

    def clone_repositories(self, repository_set: set) -> None:
        directory = self._SubversionRepositoryCloner__settings['analysis_workspace'] + self._SubversionRepositoryCloner__settings['repository_folder'] + 'svn/'
        if not os.path.exists(directory):
            os.makedirs(directory)
        for url in repository_set:
            repo_name = url.replace('/', '_')
            logging.info('[SubversionRepositoryCloner]: Cloning repository ' + repo_name + ' from ' + url + '...')
            repo_directory = directory + repo_name
            http = urllib3.PoolManager()
            try:
                status = http.request('GET', url, timeout=2).status
                if status == 200:
                    try:
                        if not os.path.exists(repo_directory):
                            os.makedirs(repo_directory)
                        svn.remote.RemoteClient(url).checkout(repo_directory)
                    except svn.exception.SvnException:
                        logging.warning('[SubversionRepositoryCloner]: Could not clone from ' + url)

                else:
                    logging.warning('[SubversionRepositoryCloner]: Could not clone from ' + url + ', server responded with ' + str(status))
            except urllib3.exceptions.MaxRetryError:
                logging.warning('[SubversionRepositoryCloner]: Could not reach ' + url + ', connection timeout...')

    def clones(self) -> str:
        return 'svn'