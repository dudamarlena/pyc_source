# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jon/Documents/TiddlyWiki/Trunk/contributors/JonRobson/TiddlyWeb/plugins/voting/test/test_rate.py
# Compiled at: 2010-04-17 06:35:26
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


def test_badvalues():
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'GUEST'}
    config['tiddlyweb.query'] = {'bag': ['films'], 'tiddler': ['Kill Bill']}
    config['tiddlyweb.query']['value'] = ['bad bad']
    (status, code) = voting.perform_action(config)
    assert code is 5
    assert status is False
    config['tiddlyweb.query'] = {'bag': ['filmz'], 'tiddler': ['Kill Bill']}
    config['tiddlyweb.query']['value'] = [
     '4']
    (status, code) = voting.perform_action(config)
    assert code is 2
    assert status is False
    config['tiddlyweb.query'] = {'bag': ['films'], 'tiddler': ['Kilsl Bill']}
    (status, code) = voting.perform_action(config)
    assert code is 6
    assert status is False


def test_rate_with_floats():
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'GUEST'}
    config['tiddlyweb.query'] = {'bag': ['films'], 'tiddler': ['Kill Bill']}
    config['tiddlyweb.query']['value'] = ['1.4']
    voting.perform_action(config)
    config['tiddlyweb.query']['value'][0] = '5.2'
    voting.perform_action(config)
    config['tiddlyweb.query']['value'][0] = '4.9'
    voting.perform_action(config)
    config['tiddlyweb.query']['value'][0] = '3.2'
    voting.perform_action(config)
    voting.perform_action(config)
    voting.perform_action(config)
    result = store.get(Tiddler('Kill Bill', 'films'))
    assert result.fields['tiddlyvoting.total'] == '20'
    assert result.fields['tiddlyvoting.average'] == '3.33'
    assert result.fields['tiddlyvoting.mode'] == '3'
    datalog = store.get(Tiddler('data::Kill Bill in films', 'tiddlyvoting'))
    assert 'tiddlyvotingdata' in datalog.tags
    textLines = datalog.text.split('\n')
    for i in ['1::1', '5::2', '3::3', 'tiddlyvoting.frequency::6', 'tiddlyvoting.total::20']:
        assert i in textLines


def test_rate():
    setup(store)
    config['tiddlyweb.usersign'] = {'name': 'jon'}
    config['tiddlyweb.query'] = {'bag': ['films'], 'tiddler': ['Jackie Brown']}
    config['tiddlyweb.query']['value'] = ['1']
    voting.perform_action(config)
    config['tiddlyweb.query']['value'][0] = '5'
    voting.perform_action(config)
    config['tiddlyweb.query']['value'][0] = '4'
    voting.perform_action(config)
    config['tiddlyweb.query']['value'][0] = '3'
    voting.perform_action(config)
    voting.perform_action(config)
    voting.perform_action(config)
    jackiebrown = store.get(Tiddler('Jackie Brown', 'films'))
    assert jackiebrown.fields['tiddlyvoting.total'] == '19'
    assert jackiebrown.fields['tiddlyvoting.average'] == '3.17'
    assert jackiebrown.fields['tiddlyvoting.mode'] == '3'
    assert jackiebrown.modifier == 'Ben'
    newtext = 'new information about jackie brown'
    jackiebrown.fields['tiddlyvoting.total'] = '3040'
    jackiebrown.fields['tiddlyvoting.average'] = '20'
    jackiebrown.text = newtext
    voting.tiddlyvoting_validator(jackiebrown, config)
    assert jackiebrown.text == newtext
    assert jackiebrown.fields['tiddlyvoting.total'] == '19'
    assert jackiebrown.fields['tiddlyvoting.average'] == '3.17'
    user_rate_log = store.get(Tiddler('jon increment Jackie Brown in films', 'tiddlyvoting'))
    assert 'tiddlyvotingrecord' in user_rate_log.tags
    assert 'tiddlyvotingdata' not in user_rate_log.tags
    datalog = store.get(Tiddler('data::Jackie Brown in films', 'tiddlyvoting'))
    textLines = datalog.text.split('\n')
    for i in textLines:
        assert i in ('1::1', '5::1', '3::3', '4::1', 'tiddlyvoting.frequency::6', 'tiddlyvoting.total::19',
                     'tiddlyvoting.mode::3', 'tiddlyvoting.average::3.17')