# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/ynabintegrationslib/ynabintegrationslib/adapters/abnamro.py
# Compiled at: 2019-12-10 09:27:05
# Size of source mod 2**32: 6444 bytes
"""
Main code for abnamro.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import logging
from abnamrolib import AccountContract as AbnAmroAccountContract
from abnamrolib import CreditCardContract as AbnAmroCreditCardContract
from ynabintegrationslib.lib.core import YnabAccount, YnabTransaction
assert AbnAmroAccountContract
assert AbnAmroCreditCardContract
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '24-06-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'abnamro'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class AbnAmroAccount(YnabAccount):
    __doc__ = 'Models an Abn Amro account.'

    @property
    def _comparable_attributes(self):
        return ['ynab_account_name',
         'bank_account_number']

    @property
    def ynab_account_name(self):
        """Ynab account name."""
        return self.ynab_account.name

    @property
    def bank_account_number(self):
        """Bank account number."""
        return self.bank_account.account_number

    @property
    def transactions(self):
        """Transactions."""
        for transaction in self.bank_account.transactions:
            yield AbnAmroAccountTransaction(transaction, self._ynab_account)

    def get_latest_transactions(self):
        """Retrieves latest transactions."""
        for transaction in self.bank_account.get_latest_transactions():
            yield AbnAmroAccountTransaction(transaction, self._ynab_account)

    def get_transactions_for_date(self, date):
        """Retrieves transactions for date."""
        for transaction in self.bank_account.get_transactions_for_date(date):
            yield AbnAmroAccountTransaction(transaction, self._ynab_account)

    def get_transactions_for_date_range(self, date_from, date_to):
        """Retrieves transactions for date."""
        for transaction in self.bank_account.get_transactions_for_date_range(date_from, date_to):
            yield AbnAmroAccountTransaction(transaction, self._ynab_account)

    def transactions_since_date(self, date):
        """Retrieves transactions for date."""
        for transaction in self.bank_account.transactions_since_date(date):
            yield AbnAmroAccountTransaction(transaction, self._ynab_account)


class AbnAmroCreditCard(YnabAccount):
    __doc__ = 'Models an Abn Amro credit card account.'

    @property
    def _comparable_attributes(self):
        return ['ynab_account_name',
         'bank_account_number']

    @property
    def ynab_account_name(self):
        """Ynab account name."""
        return self.ynab_account.name

    @property
    def bank_account_number(self):
        """Bank account number."""
        return self.bank_account.number

    @property
    def transactions(self):
        """Transactions."""
        for transaction in self.bank_account.transactions:
            yield AbnAmroCreditCardTransaction(transaction, self._ynab_account)

    def get_latest_transactions(self):
        """Retrieves latest transactions."""
        for transaction in self.bank_account.get_current_period_transactions():
            yield AbnAmroCreditCardTransaction(transaction, self._ynab_account)


class AbnAmroAccountTransaction(YnabTransaction):
    __doc__ = 'Models an Abn Amro account transaction.'

    @property
    def amount(self):
        """Amount."""
        if self._transaction.amount:
            return int(float(self._transaction.amount) * 1000)

    @property
    def payee_name(self):
        """Payee Name."""
        return self._clean_up(self._transaction.counter_account_name)

    @property
    def memo(self):
        """Memo of maximum 200 characters."""
        return self._transaction.description[:200]

    @property
    def date(self):
        """Date."""
        return self._transaction.transaction_date.strftime('%Y-%m-%d')


class AbnAmroCreditCardTransaction(YnabTransaction):
    __doc__ = 'Models an Abn Amro credit card transaction.'

    @property
    def amount(self):
        """Amount."""
        amount = int(self._transaction.billing_amount * 1000)
        if self._transaction.type_of_transaction == 'P':
            return abs(amount)
        return amount * -1

    @property
    def payee_name(self):
        """Payee Name."""
        return self._clean_up(self._transaction.description)

    @property
    def memo(self):
        """Memo."""
        return f"Description: {self._transaction.description}\nBuyer: {self._transaction.embossing_name}\nMerchant Category: {self._transaction.merchant_category_description}\nAmount: {self._transaction.billing_amount} {self._transaction.billing_currency}"[:200]

    @property
    def date(self):
        """Date."""
        return self._transaction.transaction_date

    @property
    def is_reserved(self):
        """Is reserved."""
        return self._transaction.type_of_transaction == 'A'