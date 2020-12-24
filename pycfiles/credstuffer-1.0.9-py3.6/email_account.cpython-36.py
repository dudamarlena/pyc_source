# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/email_account.py
# Compiled at: 2019-12-30 19:10:39
# Size of source mod 2**32: 607 bytes
import logging
from abc import abstractmethod
from credstuffer import Account

class EmailAccount(Account):
    __doc__ = ' Base class EmailAccount to provide basic methods for accounts with email accounts\n\n    USAGE:\n            eaccount = EmailAccount()\n\n    '

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