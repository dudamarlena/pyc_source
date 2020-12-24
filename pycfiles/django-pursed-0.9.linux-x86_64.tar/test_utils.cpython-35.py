# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/strip/.local/share/virtualenvs/django-pursed/lib/python3.5/site-packages/wallet/tests/test_utils.py
# Compiled at: 2017-04-18 11:29:16
# Size of source mod 2**32: 679 bytes
from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
import logging
User = get_user_model()
logger = logging.getLogger(__name__)

class WalletTestCase(TransactionTestCase):

    def _create_initial_balance(self, value):
        self.wallet.transaction_set.create(value=value, running_balance=value)
        self.wallet.current_balance = value
        self.wallet.save()

    def setUp(self):
        logger.info('Creating wallet...')
        self.user = User()
        self.user.save()
        self.wallet = self.user.wallet_set.create()
        self.wallet.save()
        logger.info('Wallet created.')