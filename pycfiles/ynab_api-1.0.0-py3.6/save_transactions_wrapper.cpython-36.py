# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ynab_api/models/save_transactions_wrapper.py
# Compiled at: 2019-11-21 19:08:24
# Size of source mod 2**32: 4529 bytes
"""
    YNAB API Endpoints

    Our API uses a REST based design, leverages the JSON data format, and relies upon HTTPS for transport. We respond with meaningful HTTP response codes and if an error occurs, we include error details in the response body.  API Documentation is at https://api.youneedabudget.com  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""
import pprint, re, six
from ynab_api.configuration import Configuration

class SaveTransactionsWrapper(object):
    __doc__ = 'NOTE: This class is auto generated by OpenAPI Generator.\n    Ref: https://openapi-generator.tech\n\n    Do not edit the class manually.\n    '
    openapi_types = {'transaction':'SaveTransaction', 
     'transactions':'list[SaveTransaction]'}
    attribute_map = {'transaction':'transaction', 
     'transactions':'transactions'}

    def __init__(self, transaction=None, transactions=None, local_vars_configuration=None):
        """SaveTransactionsWrapper - a model defined in OpenAPI"""
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        else:
            self.local_vars_configuration = local_vars_configuration
            self._transaction = None
            self._transactions = None
            self.discriminator = None
            if transaction is not None:
                self.transaction = transaction
            if transactions is not None:
                self.transactions = transactions

    @property
    def transaction(self):
        """Gets the transaction of this SaveTransactionsWrapper.  # noqa: E501

        :return: The transaction of this SaveTransactionsWrapper.  # noqa: E501
        :rtype: SaveTransaction
        """
        return self._transaction

    @transaction.setter
    def transaction(self, transaction):
        """Sets the transaction of this SaveTransactionsWrapper.

        :param transaction: The transaction of this SaveTransactionsWrapper.  # noqa: E501
        :type: SaveTransaction
        """
        self._transaction = transaction

    @property
    def transactions(self):
        """Gets the transactions of this SaveTransactionsWrapper.  # noqa: E501

        :return: The transactions of this SaveTransactionsWrapper.  # noqa: E501
        :rtype: list[SaveTransaction]
        """
        return self._transactions

    @transactions.setter
    def transactions(self, transactions):
        """Sets the transactions of this SaveTransactionsWrapper.

        :param transactions: The transactions of this SaveTransactionsWrapper.  # noqa: E501
        :type: list[SaveTransaction]
        """
        self._transactions = transactions

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}
        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(lambda x: x.to_dict() if hasattr(x, 'to_dict') else x, value))
            else:
                if hasattr(value, 'to_dict'):
                    result[attr] = value.to_dict()
                else:
                    if isinstance(value, dict):
                        result[attr] = dict(map(lambda item: (item[0], item[1].to_dict()) if hasattr(item[1], 'to_dict') else item, value.items()))
                    else:
                        result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SaveTransactionsWrapper):
            return False
        else:
            return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SaveTransactionsWrapper):
            return True
        else:
            return self.to_dict() != other.to_dict()