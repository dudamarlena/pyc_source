# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/strip/.local/share/virtualenvs/django-pursed/lib/python3.5/site-packages/wallet/models.py
# Compiled at: 2017-04-18 11:29:16
# Size of source mod 2**32: 2943 bytes
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from .errors import InsufficientBalance
CURRENCY_STORE_FIELD = getattr(settings, 'WALLET_CURRENCY_STORE_FIELD', models.BigIntegerField)

class Wallet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    current_balance = CURRENCY_STORE_FIELD(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def deposit(self, value):
        """Deposits a value to the wallet.

        Also creates a new transaction with the deposit
        value.
        """
        self.transaction_set.create(value=value, running_balance=self.current_balance + value)
        self.current_balance += value
        self.save()

    def withdraw(self, value):
        """Withdraw's a value from the wallet.

        Also creates a new transaction with the withdraw
        value.

        Should the withdrawn amount is greater than the
        balance this wallet currently has, it raises an
        :mod:`InsufficientBalance` error. This exception
        inherits from :mod:`django.db.IntegrityError`. So
        that it automatically rolls-back during a
        transaction lifecycle.
        """
        if value > self.current_balance:
            raise InsufficientBalance('This wallet has insufficient balance.')
        self.transaction_set.create(value=-value, running_balance=self.current_balance - value)
        self.current_balance -= value
        self.save()

    def transfer(self, wallet, value):
        """Transfers an value to another wallet.

        Uses `deposit` and `withdraw` internally.
        """
        self.withdraw(value)
        wallet.deposit(value)


class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet)
    value = CURRENCY_STORE_FIELD(default=0)
    running_balance = CURRENCY_STORE_FIELD(default=0)
    created_at = models.DateTimeField(auto_now_add=True)