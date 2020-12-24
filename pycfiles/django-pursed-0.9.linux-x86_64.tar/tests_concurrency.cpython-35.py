# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/strip/.local/share/virtualenvs/django-pursed/lib/python3.5/site-packages/wallet/tests/tests_concurrency.py
# Compiled at: 2017-04-18 11:29:16
# Size of source mod 2**32: 6022 bytes
from django.db import transaction
import threading, time
from wallet.models import Wallet
from wallet.errors import InsufficientBalance
from .test_utils import WalletTestCase

class ConcurrentDepositTestCase(WalletTestCase):

    def test_deposit(self):
        """Test two concurrent deposit transactions."""
        DEPOSIT = 100

        def deposit_thread(sleep=False):
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(pk=self.wallet.id)
                wallet.deposit(DEPOSIT)
                if sleep:
                    time.sleep(0.1)

        t1 = threading.Thread(target=deposit_thread, args=(True, ))
        t2 = threading.Thread(target=deposit_thread)
        t2.start()
        t1.run()
        t2.join()
        wallet = Wallet.objects.get(pk=self.wallet.id)
        self.assertEqual(wallet.current_balance, DEPOSIT * 2)
        self.assertEqual(wallet.transaction_set.count(), 2)

    def test_withdraw(self):
        """Test two concurrent withdraw transactions."""
        INITIAL_BALANCE = 200
        self._create_initial_balance(INITIAL_BALANCE)
        WITHDRAW = 100

        def withdraw_thread(sleep=False):
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(pk=self.wallet.id)
                wallet.withdraw(WITHDRAW)
                if sleep:
                    time.sleep(0.1)

        t1 = threading.Thread(target=withdraw_thread, args=(True, ))
        t2 = threading.Thread(target=withdraw_thread)
        t2.start()
        t1.run()
        t2.join()
        wallet = Wallet.objects.get(pk=self.wallet.id)
        self.assertEqual(wallet.current_balance, INITIAL_BALANCE - WITHDRAW * 2)
        self.assertEqual(wallet.transaction_set.count(), 3)

    def test_multiple_withdraw_insufficient_balance(self):
        """We're going to test two concurrent withdraw
        transactions happening in parallel where one would
        end-up with an insufficient balance."""
        INITIAL_BALANCE = 199
        self._create_initial_balance(INITIAL_BALANCE)
        WITHDRAW = 100

        def withdraw_thread(sleep=False):
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(pk=self.wallet.id)
                try:
                    wallet.withdraw(WITHDRAW)
                except InsufficientBalance:
                    pass

                if sleep:
                    time.sleep(0.1)

        t1 = threading.Thread(target=withdraw_thread, args=(True, ))
        t2 = threading.Thread(target=withdraw_thread)
        t2.start()
        t1.run()
        t2.join()
        wallet = Wallet.objects.get(pk=self.wallet.id)
        self.assertEqual(wallet.current_balance, INITIAL_BALANCE - WITHDRAW * 1)
        self.assertEqual(wallet.transaction_set.count(), 2)


class ConcurrentTransferTestCase(WalletTestCase):

    def test_transfer(self):
        """We're going to simulate concurrent transfer to a
        single wallet."""
        INITIAL_BALANCE = 200
        self._create_initial_balance(INITIAL_BALANCE)
        TRANSFER = 100
        _wallet2 = self.user.wallet_set.create()
        wallet2_id = _wallet2.id

        def transfer_thread(sleep=False):
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update().get(pk=self.wallet.id)
                wallet2 = Wallet.objects.select_for_update().get(pk=wallet2_id)
                wallet.transfer(wallet2, TRANSFER)
                if sleep:
                    time.sleep(0.1)

        t1 = threading.Thread(target=transfer_thread, args=(True, ))
        t2 = threading.Thread(target=transfer_thread)
        t2.start()
        t1.run()
        t2.join()
        wallet = Wallet.objects.get(pk=self.wallet.id)
        wallet2 = Wallet.objects.get(pk=wallet2_id)
        self.assertEqual(wallet.current_balance, INITIAL_BALANCE - TRANSFER * 2)
        self.assertEqual(wallet2.current_balance, TRANSFER * 2)