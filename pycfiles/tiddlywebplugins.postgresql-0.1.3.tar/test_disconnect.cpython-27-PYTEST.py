# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.postgresql/test/test_disconnect.py
# Compiled at: 2013-12-12 10:44:39
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, py.test
from tiddlyweb.config import config
from tiddlyweb.store import Store, NoBagError, NoUserError, NoRecipeError, NoTiddlerError
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.user import User
from tiddlywebplugins.postgresql import Base
import simplejson

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1], {'tiddlyweb.config': config})
    Base.metadata.drop_all()
    Base.metadata.create_all()
    import warnings
    warnings.simplefilter('error')


def test_tiddler_text():
    store.put(Bag('onebag'))
    tiddler = Tiddler('tid', 'onebag')
    tiddler.text = "'|| from"
    store.put(tiddler)
    tiddler = store.get(tiddler)
    print tiddler.text