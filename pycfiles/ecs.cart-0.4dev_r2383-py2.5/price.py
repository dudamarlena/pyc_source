# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ecs/cart/price.py
# Compiled at: 2009-01-13 06:18:21
"""price module"""

class Price(object):
    """object for manipulate vat and reduction on price"""
    _without_tax = None
    _included_tax = None
    _amount_vat = None

    def __init__(self, included_tax=None, without_tax=None, vat=0.0):
        self._vat = vat
        if included_tax is None and without_tax is None:
            raise ValueError('Need a included tax price or a without tax price')
        elif included_tax is None:
            self.without_tax = float(without_tax)
        else:
            self.included_tax = float(included_tax)
        return

    def __call__(self):
        return {'included_tax': self.included_tax, 'without_tax': self.without_tax, 'amount_vat': self.amount_vat, 
           'vat': self.vat}

    def build_included_tax(self):
        if self._without_tax is None:
            raise ValueError('Without tax is None')
        amount_vat = self.vat * self._without_tax / 100
        self._amount_vat = amount_vat
        self._included_tax = self._without_tax + self.amount_vat
        return

    def build_without_tax(self):
        if self._included_tax is None:
            raise ValueError('Included tax is None')
        without_tax = self._included_tax / (1 + self.vat / 100)
        self._without_tax = without_tax
        self._amount_vat = self._included_tax - self._without_tax
        return

    def _set_without_tax(self, without_tax):
        self._without_tax = without_tax
        self.build_included_tax()

    def _set_included_tax(self, included_tax):
        self._included_tax = included_tax
        self.build_without_tax()

    def _set_vat(self, vat):
        error_message = "It's forbidden to set directly the vat attribute"
        raise AttributeError(error_message)

    def _set_amount_vat(self, amount_vat):
        error_message = "It's forbidden to set directly the vat_amount attribute"
        raise AttributeError(error_message)

    def _get_without_tax(self):
        return self._without_tax

    def _get_included_tax(self):
        return self._included_tax

    def _get_vat(self):
        return self._vat

    def _get_amount_vat(self):
        return self._amount_vat

    without_tax = property(_get_without_tax, _set_without_tax)
    included_tax = property(_get_included_tax, _set_included_tax)
    vat = property(_get_vat, _set_vat)
    amount_vat = property(_get_amount_vat, _set_amount_vat)