# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.oom/test/test_union_filter.py
# Compiled at: 2012-05-02 16:21:14
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.config import config
from tiddlywebplugins.oom import init
tiddlers = [
 Tiddler('1'), Tiddler('c'), Tiddler('a'), Tiddler('b')]
bags = [Bag('hello'), Bag('goodbye'), Bag('not')]

def setup_module(module):
    init(config)
    from tiddlywebplugins.oom import test_oom as tm
    module.test_oom = tm


def test_simple_oom():
    selected_tiddlers = test_oom('title', '1,c', tiddlers)
    assert ['1', 'c'] == [ tiddler.title for tiddler in selected_tiddlers ]


def test_simple_bags():
    selected_bags = test_oom('name', 'hello,goodbye', bags)
    assert ['hello', 'goodbye'] == [ bag.name for bag in selected_bags ]


def test_oom_separator():
    selected_tiddlers = test_oom('title', '1|c', tiddlers)
    assert [] == [ tiddler.title for tiddler in selected_tiddlers ]
    selected_tiddlers = test_oom('title', '1|c', tiddlers, {'tiddlyweb.config': {'oom.separator': '|'}})
    assert [
     '1', 'c'] == [ tiddler.title for tiddler in selected_tiddlers ]
    selected_tiddlers = test_oom('title', '1,c', tiddlers, {'tiddlyweb.config': {'oom.separator': '|'}})
    assert [] == [ tiddler.title for tiddler in selected_tiddlers ]