# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/accounts/facebook.py
# Compiled at: 2019-12-30 19:10:39
# Size of source mod 2**32: 661 bytes
import logging
from credstuffer import EmailAccount

class Facebook(EmailAccount):
    __doc__ = ' class Facebook to provide basic methods for credstuffing facebook.com\n\n    USAGE:\n            facebook = Facebook()\n\n    '

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