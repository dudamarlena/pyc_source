# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/algorithm.py
# Compiled at: 2020-04-05 08:14:43
# Size of source mod 2**32: 1827 bytes
import logging
from credstuffer.database_stuffer import DatabaseStuffer
from credstuffer.file_stuffer import FileStuffer
from credstuffer.directory_stuffer import DirectoryStuffer

class Algorithm:
    """Algorithm"""

    def __init__(self, accounts, usernames):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Algorithm')
        self.usernames = [user.strip() for user in usernames]
        self.accounts = accounts
        for account in self.accounts:
            account.set_usernames(usernames=(self.usernames))

    def database_stuffing(self, schemas, tables, **dbparams):
        """ creates the DatabaseStuffer instance and starts the run thread

        """
        if all(el is not None for el in [schemas, tables]):
            stuffer = DatabaseStuffer(account=self.accounts[0], schemas=schemas, tables=tables, **dbparams)
            stuffer.start()
        else:
            self.logger.error('Argument schemas or tables is None, can not start DatabaseStuffer')

    def file_stuffing(self, filepath):
        """ creates the FileStuffer instance and starts the run thread

        """
        stuffer = FileStuffer(account=(self.accounts[0]), filepath=filepath)
        stuffer.start()

    def directory_stuffing(self, dirpath):
        """ creates the DirectoryStuffer instance and starts the run thread

        """
        stuffer = DirectoryStuffer(account=(self.accounts[0]), directory_path=dirpath)
        stuffer.start()