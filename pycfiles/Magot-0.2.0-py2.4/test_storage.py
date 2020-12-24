# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/magot/tests/test_storage.py
# Compiled at: 2006-11-05 11:10:39
import cPickle
from magot.model import *
from magot.refdata import *
from magot.storage import *
from peak.api import *

def makeAccounts():
    root = RootAccount(name='root')
    assets = Account(root, 'Assets', type=TYPE_ASSET)
    currentAssets = Account(assets, 'Current Assets')
    cash = Account(currentAssets, 'Cash')
    tBills = Account(currentAssets, 'T-Bills')
    receivable = Account(currentAssets, 'Accounts Receivable')
    inventory = Account(assets, 'Inventory')
    rawMaterials = Account(inventory, 'Raw Materials')
    wip = Account(inventory, 'Work-In-Progress')
    finishedGoods = Account(inventory, 'Finished Goods')
    longTermAssets = Account(assets, 'Long-Term Assets')
    land = Account(longTermAssets, 'Land')
    machinery = Account(longTermAssets, 'Machinery')
    depreciation = Account(longTermAssets, 'Depreciation')
    patents = Account(longTermAssets, 'Patents')
    expense = Account(root, 'Expenses', type=TYPE_EXPENSE)
    warranty = Account(expense, 'Warranty')
    computer = Account(expense, 'Computer')
    liabilities = Account(root, "Liabilities and Owners' Equity", type=TYPE_LIABILITY)
    currentLiabilities = Account(liabilities, 'Short-Term liabilities')
    accPayable = Account(currentLiabilities, 'Accounts Payable')
    divPayable = Account(currentLiabilities, 'Dividend Payable')
    taxesPayable = Account(currentLiabilities, 'Taxes Payable')
    longTermLiabilities = Account(liabilities, 'Long-Term liabilities')
    loans = Account(longTermLiabilities, 'Bank Loans')
    equity = Account(liabilities, "Owners' Equity")
    capital = Account(equity, 'Capital')
    retainedEarnings = Account(equity, 'Retained Earnings')
    income = Account(root, 'Income', type=TYPE_INCOME)
    salary = Account(income, 'Salaries')
    cash.makeInitialTransaction(capital, Money(500000), Date(2005, 2, 1))
    tBills.makeInitialTransaction(capital, Money(1000000), Date(2005, 2, 2))
    receivable.makeInitialTransaction(capital, Money(7000000), Date(2005, 2, 3))
    rawMaterials.makeInitialTransaction(capital, Money(825000), Date(2005, 2, 1))
    wip.makeInitialTransaction(capital, Money(750000), Date(2005, 2, 2))
    finishedGoods.makeInitialTransaction(capital, Money(1200000), Date(2005, 2, 3))
    land.makeInitialTransaction(capital, Money(30000000), Date(2005, 2, 1))
    machinery.makeInitialTransaction(capital, Money(20000000), Date(2005, 3, 1))
    Transaction(Date.today(), 'First depreciation', capital, depreciation, Money(5000000))
    patents.makeInitialTransaction(capital, Money(1000000), Date(2005, 5, 1))
    computer.makeInitialTransaction(capital, Money(999), Date(2005, 11, 1))
    warranty.makeInitialTransaction(capital, Money(253), Date(2005, 1, 1))
    salary.makeInitialTransaction(capital, Money(2133), Date(2005, 1, 1))
    return root


def readDB():
    root = cPickle.load(open(filename))
    assert root.name == 'root'


def makeDB(filename):
    root = makeAccounts()
    cPickle.dump(root, open(filename, 'w'))


if __name__ == '__main__':
    readDB()