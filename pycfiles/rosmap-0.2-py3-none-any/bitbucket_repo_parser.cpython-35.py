# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/robotics/rosmap/rosmap/repository_parsers/bitbucket_repo_parser.py
# Compiled at: 2019-04-12 11:02:21
# Size of source mod 2**32: 2688 bytes
import logging
from pyquery import PyQuery
from urllib.error import HTTPError
from .i_repository_parser import IRepositoryParser

class BitbucketRepositoryParser(IRepositoryParser):
    __doc__ = '\n    Parses repository-URLs from Bitbucket using the Bitbucket-search.\n    '

    def __init__(self, settings):
        """
        Creates a new instance for the BitbucketRepositoryParser-class.
        :param settings: Settings dict containing keys bitbucket_repo_page, and bitbucket_repo_search_string.
        """
        self._BitbucketRepositoryParser__settings = settings

    def parse_repositories(self, repository_dict: dict) -> None:
        links = set()
        page_number = 0
        previous_length = -1
        while len(links) != previous_length:
            page_number += 1
            previous_length = len(links)
            d = PyQuery(url=self._BitbucketRepositoryParser__settings['bitbucket_repo_page'] + str(page_number) + '?name=' + self._BitbucketRepositoryParser__settings['bitbucket_repo_search_string'])
            for item in d('.repo-link').items():
                links.add('https://bitbucket.org' + item.attr('href'))

            logging.info('[BitbucketRepoParser]: Parsing BitBucket links... [' + str(len(links)) + ' items]')

        progress_counter = 0
        for link in links:
            progress_counter += 1
            try:
                d = PyQuery(url=link)
                for item in d('.clone-url-input').items():
                    url = str(item.attr('value'))
                    if url[-4:] != 'wiki':
                        vcs_type = url.split('.')[(-1)]
                        if vcs_type != 'git':
                            vcs_type = 'hg'
                        repository_dict[vcs_type].add(url)

                logging.info('[BitbucketRepoParser]: Parsing BitBucket clone-URLs... [' + str(progress_counter) + '/' + str(len(links)) + ']')
            except HTTPError as error:
                logging.warning('[BitbucketRepoParser]: Could not parse from ' + link + ', ' + error.reason)