# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_models.py
# Compiled at: 2014-10-09 13:38:05
import datetime
from nose.tools import eq_
from bdgt.models import Account, Transaction

def test_is_debit():
    account = Account('test', '12345')
    tx = Transaction(account, datetime.datetime.now(), 'desc', 10.0)
    eq_(tx.is_debit(), False)
    tx = Transaction(account, datetime.datetime.now(), 'desc', -10.0)
    eq_(tx.is_debit(), True)
    tx = Transaction(account, datetime.datetime.now(), 'desc', 0.0)
    eq_(tx.is_debit(), False)


def test_is_credit():
    account = Account('test', '12345')
    tx = Transaction(account, datetime.datetime.now(), 'desc', 10.0)
    eq_(tx.is_credit(), True)
    tx = Transaction(account, datetime.datetime.now(), 'desc', -10.0)
    eq_(tx.is_credit(), False)
    tx = Transaction(account, datetime.datetime.now(), 'desc', 0.0)
    eq_(tx.is_credit(), False)


def test_is_in_period():
    account = Account('test', '12345')
    tx = Transaction(account, datetime.date(1859, 11, 24), 'on the origin of species', 13.9)
    eq_(tx.is_in_period(datetime.date(1859, 11, 1), datetime.date(1859, 11, 30)), True)
    eq_(tx.is_in_period(datetime.date(1859, 10, 1), datetime.date(1859, 11, 30)), True)
    eq_(tx.is_in_period(datetime.date(1859, 10, 1), datetime.date(1859, 10, 30)), False)
    tx = Transaction(account, datetime.date(2000, 1, 1), 'desc', 13.9)
    eq_(tx.is_in_period(datetime.date(2000, 1, 1), datetime.date(2000, 1, 31)), True)
    tx = Transaction(account, datetime.date(2000, 1, 31), 'desc', 13.9)
    eq_(tx.is_in_period(datetime.date(2000, 1, 1), datetime.date(2000, 1, 31)), True)