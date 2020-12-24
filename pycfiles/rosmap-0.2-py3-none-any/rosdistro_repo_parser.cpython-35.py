# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_parsers/rosdistro_repo_parser.py
# Compiled at: 2019-02-05 11:52:53
# Size of source mod 2**32: 3553 bytes
import yaml, os, git, logging
from .i_repository_parser import IRepositoryParser

class RosdistroRepositoryParser(IRepositoryParser):
    __doc__ = '\n    Pulls the rosdistro-package and gets all urls from the rosdistro files.\n    '

    def __init__(self, settings: dict):
        """
        Creates a new instance of the RosdistroRepositoryParser class
        :param settings: Settings containing information about rosdistro_workspace and rosdistro_url
        """
        self._RosdistroRepositoryParser__settings = settings

    def _RosdistroRepositoryParser__get_rosdistro_repository(self) -> None:
        """
        Clones the repository from rosdistro_url into rosdistro_workspace (defined in settings)
        :return: None
        """
        if not os.path.exists(self._RosdistroRepositoryParser__settings['rosdistro_workspace']):
            os.makedirs(self._RosdistroRepositoryParser__settings['rosdistro_workspace'])
        try:
            logging.info('[RosdistroRepositoryParser]: Cloning rosdistro repository...')
            git.Repo.clone_from(self._RosdistroRepositoryParser__settings['rosdistro_url'], self._RosdistroRepositoryParser__settings['rosdistro_workspace'])
        except git.exc.GitCommandError:
            logging.warning('[RosdistroRepositoryParser]: Repository already exists, pulling changes...')
            repo = git.Repo(self._RosdistroRepositoryParser__settings['rosdistro_workspace'])
            repo.remotes.origin.pull()

        logging.info('[RosdistroRepositoryParser]: Rosdistro up-to-date...')

    def _RosdistroRepositoryParser__get_urls_from_file(self, file_path: str, repository_dict: dict) -> None:
        """
        Gets the URLs from a distribution.yaml that adheres to rosdistro-specs.
        :param file_path: path to a distribution.yaml file
        :param repository_dict: dictionary with repository-type (git, svn, hg, ...) as key and the repo-url as value
        :return: None
        """
        file = open(file_path, 'r')
        rosdistro = yaml.load(file)
        for repository in rosdistro['repositories']:
            try:
                vcs_type = str(rosdistro['repositories'][repository]['doc']['type'])
                url = str(rosdistro['repositories'][repository]['doc']['url'])
                repository_dict[vcs_type].add(url)
            except KeyError:
                pass

            try:
                vcs_type = str(rosdistro['repositories'][repository]['doc']['type'])
                url = str(rosdistro['repositories'][repository]['source']['url'])
                repository_dict[vcs_type].add(url)
            except KeyError:
                pass

            try:
                repository_dict['git'].add(rosdistro['repositories'][repository]['release']['url'])
            except KeyError:
                pass

    def parse_repositories(self, repository_dict: dict) -> None:
        self._RosdistroRepositoryParser__get_rosdistro_repository()
        index_file = open(self._RosdistroRepositoryParser__settings['rosdistro_workspace'] + 'index.yaml', 'r')
        index_yaml = yaml.load(index_file)
        for distribution in index_yaml['distributions']:
            logging.info('Parsing distribution ' + index_yaml['distributions'][distribution]['distribution'][0])
            self._RosdistroRepositoryParser__get_urls_from_file(self._RosdistroRepositoryParser__settings['rosdistro_workspace'] + index_yaml['distributions'][distribution]['distribution'][0], repository_dict)