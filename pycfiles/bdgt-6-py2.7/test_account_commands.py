# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_account_commands.py
# Compiled at: 2014-10-09 13:38:05
from nose.tools import eq_, with_setup
from sqlalchemy import create_engine
from bdgt.commands.accounts import CmdAddAccount, CmdDeleteAccount, CmdListAccounts
from bdgt.models import Account
from bdgt.storage.database import Base, Session, session_scope

def setup():
    global engine
    engine = create_engine('sqlite://', echo=False)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


def teardown():
    engine.dispose()
    Session.remove()


@with_setup(setup, teardown)
def test_cmd_add_account():
    CmdAddAccount('test', '987654321')()
    with session_scope() as (session):
        num = session.query(Account).filter_by(name='test').count()
        eq_(num, 1)


@with_setup(setup, teardown)
def test_cmd_delete_account():
    CmdAddAccount('test', '987654321')()
    CmdDeleteAccount('test')()
    with session_scope() as (session):
        num = session.query(Account).filter_by(name='test').count()
        eq_(num, 0)


@with_setup(setup, teardown)
def test_cmd_list_accounts():
    CmdAddAccount('test1', '987654321')()
    CmdAddAccount('test2', '876543219')()
    CmdAddAccount('test3', '765432198')()
    output = CmdListAccounts()()
    eq_(output, 'test1\ntest2\ntest3\n')