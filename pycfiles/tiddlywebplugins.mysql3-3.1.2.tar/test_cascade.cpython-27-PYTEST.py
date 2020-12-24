# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.mysql/test/test_cascade.py
# Compiled at: 2014-02-23 07:54:53
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, py.test
from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.mysql3 import Base, Session
from tiddlywebplugins.sqlalchemy3 import sText, sTiddler, sTag, sRevision, sField

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1], {'tiddlyweb.config': config})
    Base.metadata.drop_all()
    Base.metadata.create_all()


def test_cascade():
    bag = Bag('holder')
    store.put(bag)
    tiddler = Tiddler('one', 'holder')
    tiddler.text = 'text'
    tiddler.tags = ['tag']
    tiddler.fields = {'fieldone': 'valueone'}
    store.put(tiddler)

    def count_em(count, message):
        text_count = store.storage.session.query(sText).count()
        tag_count = store.storage.session.query(sTag).count()
        tiddler_count = store.storage.session.query(sTiddler).count()
        revision_count = store.storage.session.query(sRevision).count()
        field_count = store.storage.session.query(sField).count()
        store.storage.session.commit()
        message = '%s, but got: text: %s, tag: %s, tiddler: %s, revision: %s, field: %s' % (
         message, text_count, tag_count,
         tiddler_count, revision_count, field_count)
        assert text_count == tag_count == tiddler_count == revision_count == field_count == count, message

    count_em(1, '1 row for the tiddler everywhere')
    store.delete(tiddler)
    count_em(0, '0 rows for the tiddler everywhere')