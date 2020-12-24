# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/clone.py
# Compiled at: 2018-09-15 14:38:44
# Size of source mod 2**32: 2205 bytes
from __future__ import print_function
import logging, os, git
from . import config
from .local_repo import LocalRepo
from .parameters import GITHUB_ORG
logger = logging.getLogger(__name__)
clone_url_ssh_template = 'git@github.com:{org_name}/{repo_name}.git'

def clone(book_repo_name, library_path=None):
    logger.info('running clone for{}'.format(book_repo_name))
    vat = CloneVat(book_repo_name)
    success, message = vat.clone()
    logger.info(message)
    return LocalRepo(None, cloned_repo=(vat.local_repo))


class CloneVat(object):
    __doc__ = " An object for cloning GITenberg repos\n    :takes: `book_repo_name` --  eg. `'Frankenstein_84`\n\n    "

    def __init__(self, book_repo_name):
        self.book_repo_name = book_repo_name
        self.local_repo = None
        if not config.data:
            config.ConfigFile()

    def library_book_dir(self):
        logger.info('clone {} {}'.format(config.data['library_path'], self.book_repo_name))
        return os.path.join(config.data['library_path'], self.book_repo_name)

    def path_exists(self):
        if os.path.exists(self.library_book_dir()):
            return True
        else:
            return False

    def get_clone_url_ssh(self):
        return clone_url_ssh_template.format(org_name=GITHUB_ORG, repo_name=(self.book_repo_name))

    def clone(self):
        """ clones a book from GITenberg's repo into the library
        assumes you are authenticated to git clone from repo?
        returns True/False, message
        """
        logger.debug('Attempting to clone {0}'.format(self.book_repo_name))
        if self.path_exists():
            return (
             False, 'Error: Local clone of {0} already exists'.format(self.book_repo_name))
        try:
            self.local_repo = git.Repo.clone_from(self.get_clone_url_ssh(), self.library_book_dir())
            return (True, 'Success! Cloned {0}'.format(self.book_repo_name))
        except git.exc.GitCommandError as e:
            print(e)
            logger.debug("clone ran into an issue, likely remote doesn't exist")
            return (False, 'Error git returned  a fail code')