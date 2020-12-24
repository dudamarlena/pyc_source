# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/strip/.local/share/virtualenvs/django-pursed/lib/python3.5/site-packages/wallet/tests/tests.py
# Compiled at: 2017-04-18 11:29:16
# Size of source mod 2**32: 3053 bytes
from wallet.errors import InsufficientBalance
from .test_utils import WalletTestCase

class BalanceTestCase(WalletTestCase):

    def test_default_balance(self):
        self.assertEqual(self.wallet.current_balance, 0)


class DepositTestCase(WalletTestCase):

    def test_deposit(self):
        """Test the basic wallet deposit operation."""
        DEPOSIT = 100
        self.wallet.deposit(DEPOSIT)
        self.assertEqual(self.wallet.current_balance, DEPOSIT)
        self.assertEqual(self.wallet.transaction_set.first().value, DEPOSIT)


class WithdrawTestCase(WalletTestCase):

    def test_withdraw(self):
        """Test the basic wallet withdraw operation on a
        wallet that has an initial balance."""
        INITIAL_BALANCE = 100
        self._create_initial_balance(INITIAL_BALANCE)
        WITHDRAW = 99
        self.wallet.withdraw(WITHDRAW)
        self.assertEqual(self.wallet.current_balance, INITIAL_BALANCE - WITHDRAW)
        self.assertEqual(self.wallet.transaction_set.last().value, -WITHDRAW)

    def test_no_balance_withdraw(self):
        """Test the basic wallet withdraw operation on a
        wallet without any transaction.
        """
        with self.assertRaises(InsufficientBalance):
            self.wallet.withdraw(100)


class TransferTestCase(WalletTestCase):

    def test_transfer(self):
        """Test the basic tranfer operation on a wallet."""
        INITIAL_BALANCE = 100
        TRANSFER_AMOUNT = 100
        self._create_initial_balance(INITIAL_BALANCE)
        wallet2 = self.user.wallet_set.create()
        self.wallet.transfer(wallet2, TRANSFER_AMOUNT)
        self.assertEqual(self.wallet.current_balance, INITIAL_BALANCE - TRANSFER_AMOUNT)
        self.assertEqual(wallet2.current_balance, TRANSFER_AMOUNT)

    def test_transfer_insufficient_balance(self):
        """Test a scenario where a transfer is done on a
        wallet with an insufficient balance."""
        INITIAL_BALANCE = 100
        TRANSFER_AMOUNT = 150
        self._create_initial_balance(INITIAL_BALANCE)
        wallet2 = self.user.wallet_set.create()
        with self.assertRaises(InsufficientBalance):
            self.wallet.transfer(wallet2, TRANSFER_AMOUNT)