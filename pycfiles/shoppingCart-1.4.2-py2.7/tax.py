# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/shoppingCart/tax.py
# Compiled at: 2015-08-10 04:44:00


def calculate(amount, taxes, tax_type, currency_rate=1, price_accuracy=2):
    """
    :return: Tax amount according to currency rate.
    """
    total_tax = 0.0
    if tax_type == 'included':
        tax_percentage = sum([ tax['amount'] for tax in taxes if tax['type'] == 'percentage' ])
    for tax in taxes:
        if tax['type'] == 'percentage':
            if tax_type == 'included':
                total_tax += round(float(amount) / (1 + float(tax_percentage) / 100) * (float(tax['amount']) / 100), price_accuracy)
            else:
                total_tax += round(float(amount) * (float(tax['amount']) / 100), price_accuracy)
        elif tax['type'] == 'fixed':
            total_tax += round(float(tax['amount']) * currency_rate, price_accuracy)

    return round(total_tax, price_accuracy)