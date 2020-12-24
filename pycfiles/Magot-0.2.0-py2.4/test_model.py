# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/magot/tests/test_model.py
# Compiled at: 2006-09-10 16:00:57
"""Unit tests for transaction creation/modification."""
from unittest import TestCase, makeSuite, TestSuite
import unittest
from magot.model import *
from magot.refdata import *

def makeAccounts(self):
    self.root = RootAccount(name='Accounts')
    self.asset = Account(parent=self.root, name='Asset', type=TYPE_ASSET)
    self.checking = Account(parent=self.asset, name='Checking')
    self.computer = Account(parent=self.asset, name='Computer')
    self.expense = Account(parent=self.root, name='Expense', type=TYPE_EXPENSE)
    self.warranty = Account(parent=self.expense, name='Warranty')
    self.cash = Account(parent=self.expense, name='Cash')
    self.income = Account(parent=self.root, name='Income', type=TYPE_INCOME)
    self.salary = Account(parent=self.income, name='Salary')
    self.equity = Account(parent=self.root, name='Equity', type=TYPE_EQUITY)
    self.checking.makeInitialTransaction(self.equity, Money(1))
    assert self.checking.balance == Money(1)
    self.computer.makeInitialTransaction(self.equity, Money(2))
    assert self.computer.balance == Money(2)
    assert self.asset.balance == Money(3)
    self.warranty.makeInitialTransaction(self.equity, Money(3))
    assert self.warranty.balance == Money(3)
    self.cash.makeInitialTransaction(self.equity, Money(4))
    assert self.cash.balance == Money(4)
    assert self.expense.balance == Money(7)
    self.salary.makeInitialTransaction(self.equity, Money(100.5))
    assert self.salary.balance == Money(100.5)
    assert self.equity.balance == Money(-90.5)


class TestTransaction(TestCase):
    __module__ = __name__

    def setUp(self):
        makeAccounts(self)

    def check_ordered_entries(self, account):
        d = date(2003, 1, 1)
        for e in account.entries:
            assert d <= e.date, '%s > %s' % (d, e.date)
            d = e.date

    def test_account(self):
        assert not hasattr(self.root, 'parent')
        assert self.checking.parent is self.computer.parent is self.asset
        assert self.checking.parent.parent is self.salary.parent.parent is self.root
        assert self.root.subAccounts == [self.asset, self.expense, self.income, self.equity]
        assert self.asset.subAccounts == [self.checking, self.computer]
        assert self.expense.subAccounts == [self.warranty, self.cash]
        assert self.expense.balance == Money(7)
        assert self.asset.balance == Money(3)
        assert self.cash.parent is self.expense
        self.cash.update(parent=self.asset)
        assert self.cash.parent is self.asset
        assert self.asset.subAccounts == [self.checking, self.computer, self.cash]
        assert self.expense.subAccounts == [self.warranty]
        assert self.expense.balance == Money(3)
        assert self.asset.balance == Money(7)
        self.expense.addSubAccount(self.cash)
        assert self.cash.parent is self.expense
        assert self.expense.subAccounts == [self.warranty, self.cash]
        assert self.cash in self.asset.subAccounts
        self.asset.removeSubAccount(self.cash)
        assert self.cash not in self.asset.subAccounts
        assert self.cash.parent is None
        return

    def test_2_ledged_transaction(self):
        salary = Money(100.05)
        tx = Transaction(Date.today(), 'Get salary with check', self.checking, self.salary, salary)
        assert tx.isBalanced
        debit = [ e for e in tx.entries if e.isDebit ][0]
        credit = [ e for e in tx.entries if not e.isDebit ][0]
        assert debit in self.checking.entries
        assert credit in self.salary.entries
        assert self.salary.balance == Money(100.5) + salary
        assert self.checking.balance == Money(1) + salary
        assert self.cash.balance == Money(4)
        self.checking.removeEntry(debit)
        self.cash.addEntry(debit)
        Account.balance.recompute(self.checking)
        Account.balance.recompute(self.cash)
        assert self.checking.balance == Money(1)
        assert self.cash.balance == Money(4) + salary
        assert debit in self.cash.entries
        assert debit not in self.checking.entries

    def test_4_ledged_transaction(self):
        computerAmount = Money(999.99)
        warrantyAmount = Money(100)
        cashAmount = Money(500)
        checkAmount = Money(599.99)
        tx = Transaction(Date.today(), 'Buy a computer and warranty')
        computer = tx._addDebitEntry(self.computer, computerAmount)
        warranty = tx._addDebitEntry(self.warranty, warrantyAmount)
        checking = tx._addCreditEntry(self.checking, checkAmount)
        cash = tx._addCreditEntry(self.cash, cashAmount)
        assert tx.isBalanced
        assert computer in self.computer.entries
        assert warranty in self.warranty.entries
        assert checking in self.checking.entries
        assert cash in self.cash.entries
        assert tx.entries == [computer, warranty, checking, cash]
        assert self.checking.balance == Money(1) - checkAmount
        assert self.computer.balance == Money(2) + computerAmount
        assert self.warranty.balance == Money(3) + warrantyAmount
        assert self.cash.balance == Money(4) - cashAmount
        assert self.asset.balance == Money(3) - checkAmount + computerAmount
        assert self.expense.balance == Money(7) + warrantyAmount - cashAmount
        assert self.income.balance == Money(100.5)
        assert self.equity.balance == Money(-90.5)

    def test_jump_between_tx_entries(self):
        checking_entry = self.checking.entries[0]
        equity_entry = checking_entry.siblings[0]
        assert equity_entry.transaction is checking_entry.transaction
        assert not checking_entry.transaction.isSplit
        assert checking_entry.transaction.entries == [checking_entry] + checking_entry.siblings
        assert equity_entry.account is self.equity
        assert checking_entry.account is self.checking

    def test_entry_balance(self):
        assert self.equity.entries[0].balance == Money(1)
        assert self.equity.entries[1].balance == Money(3)
        assert self.equity.entries[2].balance == Money(6)
        assert self.equity.entries[3].balance == Money(10)
        assert self.equity.entries[4].balance == self.equity.balance == Money(-90.5)

    def test_order_account_entries(self):
        m = Money(1000)
        debit = self.checking
        credit = self.salary
        tx3 = Transaction(Date(2003, 1, 3), 'tx3', debit, credit, m)
        tx1 = Transaction(Date(2003, 1, 1), 'tx1', debit, credit, m)
        tx2 = Transaction(Date(2003, 1, 2), 'tx2', debit, credit, m)
        self.check_ordered_entries(debit)
        tx2._update(date=Date.today())
        self.check_ordered_entries(debit)

    def test_change_entry(self):
        checking = self.checking
        cash = self.cash
        salary = self.salary
        initialCheckingBalance = checking.balance
        initialCashBalance = cash.balance
        initialSalaryBalance = salary.balance
        amount = Money(1000)
        tx = Transaction(Date(2003, 1, 3), b"J'ai d\xe9j\xe0 pay\xe9!")
        ed = tx._addDebitEntry(checking, amount)
        ec = tx._addCreditEntry(salary, amount)
        assert ed.transaction is ec.transaction is tx
        assert checking.balance == initialCheckingBalance + amount
        assert salary.balance == initialSalaryBalance + amount
        ed._update(account=cash)
        Account.balance.recompute(checking)
        Account.balance.recompute(cash)
        assert checking.balance == initialCheckingBalance
        assert cash.balance == initialCashBalance + amount
        assert salary.balance == initialSalaryBalance + amount
        assert ed.isDebit
        ed._update(isDebit=False)
        assert not ed.isDebit
        assert ec.isDebit
        assert tx.isBalanced
        Account.balance.recompute(cash)
        Account.balance.recompute(salary)
        assert cash.balance == initialCashBalance - amount
        assert salary.balance == initialSalaryBalance - amount
        ed._update(amount=Money(2000))
        Account.balance.recompute(cash)
        assert cash.balance == initialCashBalance - Money(2000)
        assert not tx.isBalanced
        ec._update(amount=Money(2000))
        Account.balance.recompute(salary)
        assert salary.balance == initialSalaryBalance - Money(2000)
        assert tx.isBalanced
        assert not tx.isSplit
        tx._update(amount=Money(1999))
        Account.balance.recompute(salary)
        Account.balance.recompute(cash)
        assert tx.isBalanced
        assert cash.balance == initialCashBalance - Money(1999)
        assert salary.balance == initialSalaryBalance - Money(1999)


if __name__ == '__main__':
    unittest.main()