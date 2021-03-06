# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/financespy/transaction.py
# Compiled at: 2019-06-26 14:52:36
# Size of source mod 2**32: 1835 bytes
import os, financespy.categories as categories, financespy.money as money

class Transaction:

    def __init__(self, value, description='', categories=[categories.Uncategorized()]):
        self.value = money.Money(value)
        self.categories = categories
        self.description = description

    def as_expense(self):
        new_value = -1 * self.value.abs()
        return Transaction(new_value, self.description, self.categories)

    def as_income(self):
        return Transaction(self.value.abs(), self.description, self.categories)

    def __repr__(self):
        return '%s, %s, %s' % (str(self.value), self.description, str(self.categories)[1:-1])

    def main_category(self):
        return self.categories[0]

    def test_categories(self, category):
        return [category.is_of_category(c) for c in self.categories]

    def is_of_category(self, category):
        for c in self.categories:
            if category.is_of_category(c):
                return True

        return False

    def __getattr__(self, name):
        if name.startswith('is_'):
            cat_name = name[3:]
            return self.is_of_category(categories.get_category(cat_name))

    __str__ = __repr__


def parse_transaction(record, separator=','):
    if isinstance(record, str):
        values = record.split(separator)
    else:
        if isinstance(record, list):
            values = record
        else:
            raise Exception(str(type(record)) + ' not allowed as parameter.')
    values = [s.strip() for s in values if s.strip()]
    if len(values) == 2:
        values.append(values[1])
    value = money.Money(values[0])
    description = values[1]
    category_list = list(set([categories.get_category(s) for s in values[2:]]))
    return Transaction(value, description, category_list)