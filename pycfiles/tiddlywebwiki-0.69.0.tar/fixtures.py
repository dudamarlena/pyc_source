# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebwiki/test/fixtures.py
# Compiled at: 2014-02-24 07:12:15
"""
Data structures required for our testing.
"""
import os, shutil
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.config import config
from tiddlyweb.store import Store

def _teststore():
    return Store(config['server_store'][0], config['server_store'][1], environ={'tiddlyweb.config': config})


def reset_textstore():
    if os.path.exists('store'):
        shutil.rmtree('store')


def muchdata(store):
    for bag_numeral in range(30):
        bag = _create_bag(store, bag_numeral)
        for tiddler_numeral in range(10):
            _create_tiddler(store, bag, tiddler_numeral)

    recipe = Recipe('long')
    recipe_list = [
     [
      'bag1', '']]
    for numeral in range(0, 30, 2):
        bag_name = 'bag%s' % numeral
        filter_string = 'select=title:tiddler%s' % (numeral % 10)
        if not numeral % 10 % 3:
            filter_string = filter_string + ';select=tag:tag three'
        recipe_list.append([bag_name, filter_string])

    recipe.set_recipe(recipe_list)
    store.put(recipe)


def _create_tiddler(store, bag, numeral):
    tiddler = Tiddler('tiddler%s' % numeral)
    tiddler.bag = bag.name
    tiddler.text = 'i am tiddler %s' % numeral
    tags = ['basic tag']
    if not numeral % 2:
        tags.append('tagtwo')
    if not numeral % 3:
        tags.append('tagthree')
    if not numeral % 4:
        tags.append('tagfour')
    tiddler.tags = tags
    if tiddler.title == 'tiddler8':
        tiddler.modified = '200805230303'
    store.put(tiddler)


def _create_bag(store, numeral):
    bag = Bag('bag%s' % numeral)
    store.put(bag)
    return bag