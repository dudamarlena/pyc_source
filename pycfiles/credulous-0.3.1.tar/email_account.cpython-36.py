# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/email_account.py
# Compiled at: 2019-12-30 19:10:39
# Size of source mod 2**32: 607 bytes
import logging
from abc import abstractmethod
from credstuffer import Account

class EmailAccount(Account):
    """EmailAccount"""

    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class EmailAccount')
        super().__init__()

    @abstractmethod
    def login(self, email, password):
        """ abstract method login

        :return: None or request Response
        """
        pass