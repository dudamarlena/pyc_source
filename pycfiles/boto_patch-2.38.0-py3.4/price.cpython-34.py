# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/mturk/price.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1967 bytes


class Price(object):

    def __init__(self, amount=0.0, currency_code='USD'):
        self.amount = amount
        self.currency_code = currency_code
        self.formatted_price = ''

    def __repr__(self):
        if self.formatted_price:
            return self.formatted_price
        else:
            return str(self.amount)

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'Amount':
            self.amount = float(value)
        else:
            if name == 'CurrencyCode':
                self.currency_code = value
            elif name == 'FormattedPrice':
                self.formatted_price = value

    def get_as_params(self, label, ord=1):
        return {'%s.%d.Amount' % (label, ord): str(self.amount),  '%s.%d.CurrencyCode' % (label, ord): self.currency_code}