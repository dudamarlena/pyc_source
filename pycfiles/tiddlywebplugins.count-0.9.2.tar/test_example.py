# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /svn/TiddlyWiki/Trunk/contributors/JonRobson/TiddlyWeb/plugins/tiddlerfieldcounter/test/test_example.py
# Compiled at: 2010-09-15 04:11:51
from tiddlyweb.config import config
from tiddlywebplugins import count
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.store import Store, NoTiddlerError, NoBagError, NoRecipeError
from tiddlyweb import control

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1], environ={'tiddlyweb.config': config})
    module.environ = {'tiddlyweb.store': module.store, 'tiddlyweb.config': config}


def setup_testdata():
    testdata = [{'title': 'Whiskers', 'tags': ['kitty', 'pet', 'cat'], 'fields': {'read': 'no', 'favecolor': 'red', 'badfield': 'z'}}, {'title': 'Fred', 'tags': ['dog', 'pet'], 'fields': {'badfield': 'xt', 'favecolor': 'red'}}, {'title': 'Chris', 'tags': ['cat', 'animal', 'bogof'], 'fields': {'badfield': 'ks', 'favecolor': 'red'}}, {'title': 'Martin', 'tags': ['lion'], 'fields': {'badfield': 'zs', 'favecolor': 'green'}}, {'title': 'Jerm', 'tags': ['monkey', 'lolcat'], 'fields': {'badfield': 'z', 'favecolor': 'green'}}, {'title': 'Paul', 'tags': ['dinosaur', 'kitty', 'tiger'], 'fields': {'badfield': 'z', 'favecolor': 'red'}}, {'title': 'Ben', 'tags': ['cAt', 'pet'], 'fields': {'badfield': 'z'}}, {'title': 'Andrew', 'tags': ['pet', 'animal', 'kitty'], 'fields': {'badfield': 'z', 'favecolor': 'blue'}}]
    store.put(Bag('tmp'))
    tiddlers = []
    for tid in testdata:
        tiddler = Tiddler(tid['title'], 'tmp')
        tiddler.fields = tid['fields']
        tiddler.tags = tid['tags']
        tiddlers.append(tiddler)
        store.put(tiddler)

    return tiddlers


def test_tagcount():
    tiddlers = setup_testdata()
    summary = count.survey_field_values(environ, tiddlers, 'tags')
    assert len(summary) is 12
    expected = ['pet 4', 'kitty 3', 'cat 2', 'animal 2', 'bogof 1', 'lion 1', 'monkey 1', 'dinosaur 1', 'tiger 1', 'cAt 1', 'lolcat 1', 'dog 1']
    for i in summary:
        assert i in expected

    for j in expected:
        assert j in summary

    assert summary[0] == 'pet 4'
    assert summary[1] == 'kitty 3'


def test_fieldcount():
    tiddlers = setup_testdata()
    summary = count.survey_field_values(environ, tiddlers, 'favecolor')
    assert len(summary) is 3
    expected = ['red 4', 'green 2', 'blue 1']
    for i in summary:
        assert i in expected

    for j in expected:
        assert j in summary


def test_fieldcount_limit():
    tiddlers = setup_testdata()
    summary = count.survey_field_values(environ, tiddlers, 'favecolor', 2)
    assert len(summary) is 2
    expected = ['red 4', 'green 2']
    for i in summary:
        assert i in expected

    for j in expected:
        assert j in summary


def test_tagcount_limit():
    tiddlers = setup_testdata()
    summary = count.survey_field_values(environ, tiddlers, 'tags', 2)
    assert len(summary) is 2
    assert summary == ['pet 4', 'kitty 3']
    summary2 = count.survey_field_values(environ, tiddlers, 'tags', 1)
    assert len(summary2) is 1
    assert summary2 == ['pet 4']