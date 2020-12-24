# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_category_commands.py
# Compiled at: 2014-10-31 03:15:09
from nose.tools import eq_, with_setup
from sqlalchemy import create_engine
from bdgt.commands.categories import CmdAdd
from bdgt.models import Category
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
def test_cmd_add():
    CmdAdd('category1')()
    with session_scope() as (session):
        num = session.query(Category).filter_by(name='category1').count()
        eq_(num, 1)


@with_setup(setup, teardown)
def test_cmd_add_subcategory():
    CmdAdd('category1')()
    CmdAdd('category2', 'category1')()
    with session_scope() as (session):
        category2 = session.query(Category).filter_by(name='category2').one()
        eq_(category2.parent.name, 'category1')
        category1 = session.query(Category).filter_by(name='category1').one()
        eq_(len(category1.subcategories), 1)