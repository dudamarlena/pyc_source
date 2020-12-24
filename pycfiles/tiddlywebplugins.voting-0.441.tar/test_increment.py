# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jon/Documents/TiddlyWiki/Trunk/contributors/JonRobson/TiddlyWeb/plugins/voting/test/test_increment.py
# Compiled at: 2010-04-26 06:55:09
from tiddlyweb.config import config
from tiddlywebplugins import voting
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.user import User
from tiddlyweb.model.policy import Policy
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import Store, NoTiddlerError, NoBagError, NoRecipeError
from tiddlyweb import control
import selector
from test_config import setup, votebag

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1], environ={'tiddlyweb.config': config})
    module.environ = {'tiddlyweb.store': module.store, 'tiddlyweb.config': config}


def test_string_to_float():
    actual = voting.string_to_float(None)
    assert actual == 0
    return


def test_read_slices():
    setup(store)
    actual = voting.read_slices('config::snow white', 'tiddlyvoting')
    expected = {'increment.range': '-5,30', 'increment.limit': '2'}
    for i in actual:
        assert i in expected
        assert expected[i] == actual[i]


def test_vote_log():
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'jon'}
    config['tiddlyweb.query'] = {'bag': ['mr_and_mrs'], 'tiddler': ['little miss naughty']}
    config['tiddlyweb.query']['value'] = ['10']
    (vote1, code1) = voting.perform_action(config)
    config['tiddlyweb.query']['value'] = ['14']
    (vote2, code2) = voting.perform_action(config)
    tiddler = store.get(Tiddler('little miss naughty', 'mr_and_mrs'))
    tiddler.fields['tiddlyvoting.total'] = '2000000'
    store.put(tiddler)
    config['tiddlyweb.query']['value'] = [
     '-2']
    (vote3, code3) = voting.perform_action(config)
    assert vote1 is True
    assert vote2 is True
    assert vote3 is True
    try:
        voteLog = store.get(Tiddler('data::little miss naughty in mr_and_mrs', 'tiddlyvoting'))
        expected = ['-2::1', '10::1', '14::1', 'tiddlyvoting.total::22', 'tiddlyvoting.frequency::3', 'tiddlyvoting.average::7.33']
        actual = voteLog.text.split('\n')
        for i in expected:
            assert i in actual

    except NoTiddlerError:
        assert False is True

    try:
        tiddler = store.get(Tiddler('little miss naughty', 'mr_and_mrs'))
        revision = tiddler.revision
        value = tiddler.fields['tiddlyvoting.total']
    except KeyError:
        value = False
        revision = False

    assert revision == 5
    assert value == '22'


def test_alloweduser_increments():
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'jon'}
    config['tiddlyweb.query'] = {'bag': ['mr_and_mrs'], 'tiddler': ['mr strong']}
    (result, code) = voting.perform_action(config)
    assert result is True
    try:
        tiddler = store.get(Tiddler('mr strong', 'mr_and_mrs'))
        value = tiddler.fields[('%s.total' % votebag)]
    except KeyError:
        value = False

    assert value == '1'
    try:
        tiddler = store.get(Tiddler('jon increment mr strong in mr_and_mrs', votebag))
    except NoTiddlerError:
        tiddler = False

    assert tiddler is not False


def test_unauthenticated_user_increments():
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'GUEST'}
    config['tiddlyweb.query'] = {'bag': ['mr_and_mrs'], 'tiddler': ['mr strong']}
    (result, code) = voting.perform_action(config)
    assert result is False
    try:
        tiddler = store.get(Tiddler('mr strong', 'mr_and_mrs'))
        value = tiddler.fields[('%s.total' % votebag)]
    except KeyError:
        value = False

    assert value == '923'


def test_unprivileged_user_increments():
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'FND'}
    config['tiddlyweb.query'] = {'bag': ['mr_and_mrs'], 'tiddler': ['mr strong']}
    (result, code) = voting.perform_action(config)
    assert result is False
    try:
        tiddler = store.get(Tiddler('mr strong', 'mr_and_mrs'))
        value = tiddler.fields[('%s.total' % votebag)]
    except KeyError:
        value = False

    assert value == '923'


def test_multiple_votes():
    """
  test 1  no limit
  
  """
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'jon'}
    config['tiddlyweb.query'] = {'bag': ['mr_and_mrs'], 'tiddler': ['mr small']}
    for i in range(1, 5):
        value = i * 10
        config['tiddlyweb.query']['value'] = ['%s' % value]
        voting.perform_action(config)

    try:
        tiddler = store.get(Tiddler('mr small', 'mr_and_mrs'))
        value = tiddler.fields[('%s.total' % votebag)]
    except KeyError:
        value = False

    assert value == '100'
    try:
        tiddler = store.get(Tiddler('jon increment mr small in mr_and_mrs', votebag))
        assert tiddler.revision == 4
    except NoTiddlerError:
        tiddler = False

    assert tiddler is not False
    config['tiddlyweb.usersign'] = {'name': 'jon'}
    config['tiddlyweb.query'] = {'bag': ['snow white'], 'tiddler': ['grumpy']}
    for i in range(1, 5):
        value = i * 10
        config['tiddlyweb.query']['value'] = ['%s' % value]
        voting.perform_action(config)

    try:
        tiddler = store.get(Tiddler('grumpy', 'snow white'))
        value = tiddler.fields[('%s.total' % votebag)]
    except KeyError:
        value = False

    assert value == '30'
    try:
        tiddler = store.get(Tiddler('jon increment grumpy in snow white', votebag))
        assert tiddler.revision == 2
    except NoTiddlerError:
        tiddler = False

    assert tiddler is not False


def test_minmax_votes():
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'jon'}
    config['tiddlyweb.query'] = {'bag': ['snow white'], 'tiddler': ['grumpy']}
    for i in range(-25, 10):
        value = i
        config['tiddlyweb.query']['value'] = ['%s' % value]
        voting.perform_action(config)

    try:
        tiddler = store.get(Tiddler('grumpy', 'snow white'))
        value = tiddler.fields[('%s.total' % votebag)]
    except KeyError:
        value = False

    assert value == '-9'