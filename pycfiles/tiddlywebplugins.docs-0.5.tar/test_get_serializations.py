# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.docs/test/test_get_serializations.py
# Compiled at: 2011-11-02 16:03:35
from tiddlyweb.config import config
from tiddlyweb.model.recipe import Recipe
from tiddlywebplugins.docs import Serialization

def setup_module(module):
    module.environ = {'tiddlyweb.config': config}
    module.serialization = Serialization(environ=module.environ)


def test_get_serializations():
    assert len(serialization.serializations) == 3


def test_get_serializations_recipe():
    assert len(serialization._matches('recipe_as')) == 3
    recipe = Recipe('hello')
    recipe.set_recipe([('barney', '')])
    output = serialization.recipe_as(recipe)
    assert 'tiddlyweb.serializations.json' in ('').join(list(output))