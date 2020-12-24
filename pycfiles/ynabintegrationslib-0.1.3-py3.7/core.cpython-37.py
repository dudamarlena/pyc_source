# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ctyfoxylos/personal/python/ynabintegrationslib/ynabintegrationslib/lib/core.py
# Compiled at: 2019-09-13 12:35:13
# Size of source mod 2**32: 5652 bytes
"""
Main code for core.

.. _Google Python Style Guide:
   http://google.github.io/styleguide/pyguide.html

"""
import abc, logging, importlib
from ynabinterfaceslib import Comparable
from ynabintegrationslib.ynabintegrationslibexceptions import InvalidAccount, InvalidBudget
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '24-06-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'core'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class YnabContract:
    __doc__ = 'Models a ynab contract.'

    def __init__(self, name, bank, contract_type, credentials):
        self.name = name
        self.bank = bank
        self.type = contract_type
        self.contract = self._get_contract(bank, contract_type, credentials)

    @staticmethod
    def _get_contract(bank, type_, credentials):
        contract_object = getattr(importlib.import_module('ynabintegrationslib.adapters'), f"{bank}{type_}Contract")
        return contract_object(**credentials)


class YnabAccount(Comparable):
    __doc__ = 'Models a YNAB account.'

    def __init__(self, bank_account, ynab_service, budget_name, ynab_account_name):
        super().__init__(bank_account._data)
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.bank_account = bank_account
        self.ynab = ynab_service
        self._budget, self._ynab_account = self._get_budget_and_account(budget_name, ynab_account_name)

    @property
    def _comparable_attributes(self):
        return ['budget',
         'ynab_account']

    def _get_budget_and_account(self, budget_name, account_name):
        budget = self.ynab.get_budget_by_name(budget_name)
        if not budget:
            raise InvalidBudget(budget_name)
        account = budget.get_account_by_name(account_name)
        if not account:
            raise InvalidAccount(account_name)
        return (
         budget, account)

    @property
    def budget(self):
        """Budget."""
        return self._budget

    @property
    def ynab_account(self):
        """Ynab account."""
        return self._ynab_account

    @abc.abstractmethod
    def transactions(self):
        """Transactions."""
        pass

    @abc.abstractmethod
    def get_latest_transactions(self):
        """Retrieves latest transactions from account."""
        pass


class YnabTransaction(Comparable):
    __doc__ = 'Models the interface for ynab transaction.'

    def __init__(self, transaction, account):
        super().__init__(transaction._data)
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self._transaction = transaction
        self.account = account

    @property
    def _comparable_attributes(self):
        return ['payload']

    @abc.abstractmethod
    def amount(self):
        """Amount."""
        pass

    @abc.abstractmethod
    def payee_name(self):
        """Payee Name."""
        pass

    @abc.abstractmethod
    def memo(self):
        """Memo."""
        pass

    @abc.abstractmethod
    def date(self):
        """Date."""
        pass

    @staticmethod
    def _clean_up(string):
        if string:
            return ' '.join(string.split())
        return ''

    @property
    def payload(self):
        """Payload."""
        return {'account_id':self.account.id, 
         'amount':self.amount, 
         'payee_name':self.payee_name, 
         'memo':self.memo, 
         'date':self.date}


class YnabServerTransaction(YnabTransaction):
    __doc__ = 'Models an ynab uploaded transaction.'

    @property
    def amount(self):
        """Amount."""
        return self._transaction.amount

    @property
    def payee_name(self):
        """Payee Name."""
        return self._transaction.payee_name

    @property
    def memo(self):
        """Memo of maximum 200 characters."""
        return self._transaction.memo

    @property
    def date(self):
        """Date."""
        return self._transaction.date