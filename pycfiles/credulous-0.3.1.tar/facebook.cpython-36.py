# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/accounts/facebook.py
# Compiled at: 2019-12-30 19:10:39
# Size of source mod 2**32: 661 bytes
import logging
from credstuffer import EmailAccount

class Facebook(EmailAccount):
    """Facebook"""

    def __init__(self):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class Facebook')
        super().__init__()

    def login(self, username, password):
        """

        :param username:
        :param password:
        :return:
        """
        print('facebook')

    def set_proxy(self, proxy):
        """

        :return:
        """
        pass