# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/clone.py
# Compiled at: 2016-03-01 16:53:08
""" Implements functionality for cloning a gitenberg repo book from GITenberg """
import logging, os, sh
from .book_identity import BookRepoName
from . import config
from .library import GitbergLibraryManager

def clone(arg_book_name, library_path=None):
    logging.info('running clone')
    book_repo_name = BookRepoName(arg_book_name)
    vat = CloneVat(book_repo_name)
    success, message = vat.clone()
    logging.info(message)


class CloneVat(object):
    """ An object for cloning GITenberg repos
    :takes: `book_repo_name` -- a BookRepoName instance eg. `BookRepoName('Frankenstein_84)`

    """

    def __init__(self, book_repo_name, config=None):
        self.book_repo_name = book_repo_name
        self.l_manager = GitbergLibraryManager(config=config)

    def library_book_dir(self):
        return os.path.join(self.l_manager.library_base_path(), self.book_repo_name.repo_name)

    def path_exists(self):
        if os.path.exists(self.library_book_dir()):
            return True
        else:
            return False

    def clone(self):
        """ clones a book from GITenberg's repo into the library
        assumes you are authenticated to git clone from repo?
        returns True/False, message
        """
        logging.debug(('Attempting to clone {0}').format(self.book_repo_name.repo_name))
        if self.path_exists():
            return (False,
             ('Error: Local clone of {0} already exists').format(self.book_repo_name.repo_name))
        try:
            sh.git('clone', self.book_repo_name.get_clone_url_ssh(), self.library_book_dir())
            return (True, ('Success! Cloned {0}').format(self.book_repo_name.repo_name))
        except sh.ErrorReturnCode_128:
            logging.debug('clone ran into an issue, likely this already exists')
            return (False, 'Error sh.py returned with a fail code')