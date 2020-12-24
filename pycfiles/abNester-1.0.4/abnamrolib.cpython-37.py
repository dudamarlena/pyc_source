# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ctyfoxylos/personal/python/abnamrolib/abnamrolib/abnamrolib.py
# Compiled at: 2019-12-10 08:56:16
# Size of source mod 2**32: 19926 bytes
__doc__ = '\nMain code for abnamrolib.\n\n.. _Google Python Style Guide:\n   http://google.github.io/styleguide/pyguide.html\n\n'
import logging
from datetime import date
from datetime import timedelta
from urllib3.util import parse_url
from dateutil.parser import parse
from ynabinterfaceslib import Comparable, Transaction, Contract
from .common import CookieAuthenticator
from .abnamrolibexceptions import InvalidDateFormat
__author__ = 'Costas Tyfoxylos <costas.tyf@gmail.com>'
__docformat__ = 'google'
__date__ = '19-07-2019'
__copyright__ = 'Copyright 2019, Costas Tyfoxylos'
__credits__ = ['Costas Tyfoxylos', 'Gareth Hawker']
__license__ = 'MIT'
__maintainer__ = 'Costas Tyfoxylos'
__email__ = '<costas.tyf@gmail.com>'
__status__ = 'Development'
LOGGER_BASENAME = 'abnamrolib'
LOGGER = logging.getLogger(LOGGER_BASENAME)
LOGGER.addHandler(logging.NullHandler())

class AccountContract(Contract, CookieAuthenticator):
    """AccountContract"""

    def __init__(self, cookie_file):
        CookieAuthenticator.__init__(self, cookie_file)
        self._base_url = 'https://www.abnamro.nl'
        self._accounts = None

    @property
    def host(self):
        """Host."""
        return parse_url(self.base_url).host

    @property
    def base_url(self):
        """Base url."""
        return self._base_url

    @property
    def accounts(self):
        """Accounts."""
        if self._accounts is None:
            url = f"{self.base_url}/contracts"
            headers = {'x-aab-serviceversion': 'v2'}
            response = self.session.get(url, headers=headers)
            if not response.ok:
                self._logger.warning('Error retrieving accounts for contract')
                return []
            self._accounts = [Account(self, data) for data in response.json().get('contractList', [])]
            self._accounts.extend(self._get_foreign_accounts())
        return self._accounts

    def _get_foreign_accounts(self):
        url = f"{self.base_url}/mul/accounts/v1"
        response = self.session.get(url)
        if response.status_code == 403:
            self._logger.info('No foreign accounts enabled on this account')
            return []
        if not response.ok:
            self._logger.warning('Could not get info on foreign accounts')
            return []
        return [ForeignAccount(self, data) for data in response.json().get('accounts')]

    def get_account(self, id_):
        """Retrieves the account by the provided id.

        Args:
            id_ (str): The iban to retrieve the account for

        Returns:
            account (Account): The account if it exists, None otherwise.

        """
        return self.get_account_by_iban(id_)

    def get_account_by_iban(self, iban):
        """Retrieves an account object by the provided IBAN.

        Args:
            iban (str): The iban to match the account with

        Returns:
            account (Account): Account object on match, None otherwise

        """
        return next((account for account in self.accounts if account.account_number.lower() == iban.lower()), None)

    def get_mortgage_account(self, account_number):
        """Retrieves a mortgage account by account number.

        Args:
            account_number (str): The account number of the mortgage account to match

        Returns:
            account (MortgageAccount): A MortgageAccount object on success, None otherwise

        """
        return next((MortgageAccount(self, account) for account in self.accounts if all([account.product.group == 'MORTGAGE',
         account.number == account_number])), None)


class Customer:
    """Customer"""

    def __init__(self, data):
        self._data = data

    @property
    def appearance_type(self):
        """Appearence type."""
        return self._data.get('appearanceType')

    @property
    def bc_number(self):
        """BC Number."""
        return self._data.get('bcNumber')

    @property
    def interpay_name(self):
        """Interpay name."""
        return self._data.get('interpayName')


class Product:
    """Product"""

    def __init__(self, data):
        self._data = data

    @property
    def resource_type(self):
        """Resource type."""
        return self._data.get('resourceType')

    @property
    def id(self):
        """ID."""
        return self._data.get('id')

    @property
    def building_block_id(self):
        """Building block ID."""
        return self._data.get('buildingBlockId')

    @property
    def name(self):
        """Name."""
        return self._data.get('name')

    @property
    def group(self):
        """Product group."""
        return self._data.get('productGroup')

    @property
    def account_type(self):
        """Account type."""
        return self._data.get('accountType')

    @property
    def transfer_options(self):
        """Transfer options."""
        return self._data.get('transferOptions')


class Account(Comparable):
    """Account"""

    def __init__(self, contract, data):
        super().__init__(data)
        self.contract = contract

    @property
    def _comparable_attributes(self):
        return [
         'account_number',
         'id',
         'number']

    @property
    def _contract(self):
        """Number."""
        return self._data.get('contract', {})

    @property
    def _balance(self):
        """Balance."""
        return self._data.get('contract', {}).get('balance', {})

    @property
    def account_number(self):
        """Account number."""
        return self._contract.get('accountNumber', '')

    @property
    def resource_type(self):
        """Resource type."""
        return self._contract.get('resourceType')

    @property
    def id(self):
        """Id."""
        return self._contract.get('id')

    @property
    def number(self):
        """Number."""
        return self._contract.get('contractNumber')

    @property
    def chid(self):
        """CHID."""
        return self._contract.get('chid')

    @property
    def status(self):
        """Status."""
        return self._contract.get('status')

    @property
    def is_blocked(self):
        """Is blocked."""
        return self._contract.get('isBlocked')

    @property
    def concerning(self):
        """Concerning."""
        return self._contract.get('concerning')

    @property
    def amount(self):
        """Amount."""
        return self._balance.get('amount')

    @property
    def currency_code(self):
        """Currency code."""
        return self._balance.get('currencyCode')

    @property
    def product(self):
        """Product."""
        return Product(self._contract.get('product'))

    @property
    def customer(self):
        """Customer."""
        return Customer(self._contract.get('customer'))

    @property
    def parent_contract_id(self):
        """Parent Contract."""
        return self._data.get('parentContract', {}).get('id')

    @property
    def iban(self):
        """Iban."""
        return self.account_number

    def _get_transactions(self, params=None):
        if not self.iban:
            self._logger.error('Account does not expose transactions')
            return ([], None)
        else:
            url = f"{self.contract.base_url}/mutations/{self.iban}"
            headers = {'x-aab-serviceversion': 'v3'}
            response = self.contract.session.get(url, headers=headers, params=params)
            response.ok or self._logger.warning('Error retrieving transactions for account "%s" error message was "%s" with status code "%s"', self.account_number, response.text, response.status_code)
            return ([], None)
        mutations_list = response.json().get('mutationsList', {})
        last_mutation_key = mutations_list.get('lastMutationKey', None)
        transactions = [AccountTransaction(data.get('mutation')) for data in mutations_list.get('mutations')]
        return (
         transactions, last_mutation_key)

    @property
    def transactions(self):
        """Transactions."""
        transactions, last_mutation_key = self._get_transactions()
        for transaction in transactions:
            yield transaction

        while last_mutation_key:
            params = {'lastMutationKey': last_mutation_key}
            transactions, last_mutation_key = self._get_transactions(params=params)
            for transaction in transactions:
                yield transaction

    def _parse_date(self, date):
        try:
            date_ = parse(date)
        except ValueError:
            raise InvalidDateFormat(date)

        return date_

    def get_transactions_for_date(self, date):
        date = self._parse_date(date).date()
        last_mutation_key = f"{date.year}-{date.month:02d}-{date.day + 1:02d}-00.00.00.000000"
        while last_mutation_key:
            params = {'lastMutationKey': last_mutation_key}
            transactions, last_mutation_key = self._get_transactions(params=params)
            transactions = [transaction for transaction in transactions if transaction.transaction_date == date]
            if not transactions:
                last_mutation_key = None
            for transaction in transactions:
                yield transaction

    def get_transactions_for_date_range(self, date_from, date_to):
        start_date = self._parse_date(date_to).date()
        end_date = self._parse_date(date_from).date()
        last_mutation_key = f"{start_date.year}-{start_date.month:02d}-{start_date.day + 1:02d}-00.00.00.000000"
        while last_mutation_key:
            params = {'lastMutationKey': last_mutation_key}
            transactions, last_mutation_key = self._get_transactions(params=params)
            transactions = [transaction for transaction in transactions if end_date <= transaction.transaction_date <= start_date]
            if not transactions:
                last_mutation_key = None
            for transaction in transactions:
                yield transaction

    def transactions_since_date(self, date):
        end_date = self._parse_date(date).date()
        for transaction in self.transactions:
            if transaction.transaction_date < end_date:
                break
            yield transaction

    def get_latest_transactions(self):
        """Retrieves the latest transactions.

        Returns:
            transactions (list): A list of transaction objects for the latest transactions

        """
        if not self.iban:
            self._logger.error('Account does not expose transactions')
            return []
        else:
            url = f"{self.contract.base_url}/mutations/{self.iban}"
            headers = {'x-aab-serviceversion': 'v3'}
            response = self.contract.session.get(url, headers=headers)
            response.ok or self._logger.warning('Error retrieving transactions for account "%s"', self.account_number)
            return []
        return [AccountTransaction(data.get('mutation')) for data in response.json().get('mutationsList', {}).get('mutations', [])]


class ForeignAccount(Comparable):
    """ForeignAccount"""

    def __init__(self, contract, data):
        super().__init__(data)
        self._data = data
        self.contract = contract
        self._transactions_url = self._account.get('_links').get('transactions').get('href')

    @property
    def _comparable_attributes(self):
        return [
         'account_number',
         'provider_id',
         'provider_name']

    @property
    def _account(self):
        return self._data.get('account')

    @property
    def id(self):
        """Account number."""
        return self._account.get('id')

    @property
    def account_number(self):
        """Account number."""
        return self._account.get('accountNumber')

    @property
    def iban(self):
        """IBAN."""
        return self._account.get('accountNumber')

    @property
    def provider_id(self):
        """Provider id."""
        return self._account.get('provider').get('providerId')

    @property
    def provider_name(self):
        """Provider id."""
        return self._account.get('provider').get('providerName')

    @property
    def transactions(self):
        """Transactions."""
        for transaction in self.get_latest_transactions():
            yield transaction

    def get_latest_transactions(self):
        """Get transactions from foreign account."""
        response = self.contract.session.get(self._transactions_url)
        if not response.ok:
            self._logger.warning('Error retrieving transactions for account "%s"', self.account_number)
            return []
        return [ForeignAccountTransaction(data.get('transaction', {})) for data in response.json().get('transactionList', {}).get('transactions', [{}])]


class MortgageAccount(Comparable):
    """MortgageAccount"""

    def __init__(self, contract, account):
        self._logger = logging.getLogger(f"{LOGGER_BASENAME}.{self.__class__.__name__}")
        self.contract = contract
        self.account = account
        self._data = self._get_data()
        super().__init__(self._data)

    @property
    def _comparable_attributes(self):
        return [
         '_back_office_loan_number',
         'payer_account',
         'contract_number']

    def _get_data(self):
        url = f"{self.contract.base_url}/nl/havikonline/service/api/v1/Hypotheek/{self.account.number}"
        response = self.contract.session.get(url)
        if not response.ok:
            self._logger.warning('Error retrieving data for mortgage account "%s"', self.account.number)
            return {}
        return response.json()

    @property
    def _back_office_loan_number(self):
        """Back office loan number."""
        return self._data.get('backOfficeLeningnummer')

    @property
    def payer_account(self):
        """Payer account."""
        return self._data.get('bankrekeningIncassoHoofdschuldenaar')

    @property
    def contract_number(self):
        """Contract number."""
        return self._data.get('contractnummer')

    @property
    def full_amount(self):
        """Full amount."""
        return self._data.get('leningdelen', [{}])[0].get('oorspronkelijkHypotheekbedrag')

    @property
    def remaining_amount(self):
        """Remaining amount."""
        return self._data.get('totaalResterendHypotheekbedrag')

    @property
    def remaining_months(self):
        """Remaining months."""
        return self._data.get('leningdelen', [{}])[0].get('restantLooptijdInMaanden')

    @property
    def monthly_amount(self):
        """Monthly amount."""
        return self._data.get('leningdelen', [{}])[0].get('brutoMaandlast')

    @property
    def mortgage_type(self):
        """Mortgage type."""
        return self._data.get('leningdelen', [{}])[0].get('hypotheeksoort')


class AccountTransaction(Transaction):
    """AccountTransaction"""

    @property
    def _comparable_attributes(self):
        return [
         'description',
         'transaction_date',
         'account_number',
         'amount']

    @property
    def mutation_code(self):
        """Mutation code."""
        return self._data.get('mutationCode')

    @property
    def description(self):
        """Description."""
        return ' '.join([self._clean_up(line.strip()) for line in self._data.get('descriptionLines', [])])

    @staticmethod
    def _timestamp_to_date(timestamp):
        if timestamp is None:
            return
        return date.fromtimestamp(int(timestamp) / 1000)

    @property
    def transaction_date(self):
        """Transaction date."""
        return self._timestamp_to_date(self._data.get('transactionDate'))

    @property
    def value_date(self):
        """Value date."""
        return self._timestamp_to_date(self._data.get('valueDate'))

    @property
    def book_date(self):
        """Book date."""
        return self._timestamp_to_date(self._data.get('bookDate'))

    @property
    def balance_after_mutation(self):
        """Balance after mutation."""
        return self._data.get('balanceAfterMutation')

    @property
    def transaction_type(self):
        """Transaction type."""
        return self._data.get('debitCredit')

    @property
    def indicator_digital_invoice(self):
        """Indicator digital invoice."""
        return self._data.get('indicatorDigitalInvoice')

    @property
    def counter_account_number(self):
        """Counter account number."""
        return self._data.get('counterAccountNumber')

    @property
    def counter_account_type(self):
        """Counter account type."""
        return self._data.get('counterAccountType')

    @property
    def counter_account_name(self):
        """Counter account name."""
        return self._data.get('counterAccountName')

    @property
    def currency_iso_code(self):
        """Currency iso code."""
        return self._data.get('currencyIsoCode')

    @property
    def source_inquiry_number(self):
        """Source in inquiry number."""
        return self._data.get('sourceInquiryNumber')

    @property
    def account_number(self):
        """Account number."""
        return self._data.get('accountNumber')

    @property
    def account_number_type(self):
        """Account number type."""
        return self._data.get('accountNumberType')

    @property
    def transaction_timestamp(self):
        """Transaction timestamp."""
        return self._data.get('transactionTimestamp')

    @property
    def status_timestamp(self):
        """Status timestamp."""
        return self._data.get('statusTimestamp')

    @property
    def amount(self):
        """Amount."""
        return float(self._data.get('amount'))


class ForeignAccountTransaction(AccountTransaction):
    """ForeignAccountTransaction"""

    @property
    def description(self):
        """Description."""
        return ' '.join([self._clean_up(line.strip()) for line in self._data.get('description', [])])

    @property
    def counter_account_name(self):
        """Counter account name."""
        return self._data.get('holder', {}).get('name', '')