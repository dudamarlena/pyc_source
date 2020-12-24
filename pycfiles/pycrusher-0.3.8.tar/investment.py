# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/investment.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node

@six.python_2_unicode_compatible
class Investment(Node):
    """Represents a Investment (investor-investment) on CrunchBase"""
    KNOWN_PROPERTIES = [
     'type',
     'uuid',
     'money_invested',
     'money_invested_currency_code',
     'money_invested_usd',
     'is_lead_investor']
    KNOWN_RELATIONSHIPS = [
     'funding_round',
     'invested_in',
     'investors']

    def __str__(self):
        if self.money_invested:
            return ('Investment: {invested}').format(invested=self.money_invested)
        if hasattr(self, 'investors'):
            return ('Investment: {investors}').format(investors=self.investors)
        return 'Investment'

    def __repr__(self):
        return self.__str__()