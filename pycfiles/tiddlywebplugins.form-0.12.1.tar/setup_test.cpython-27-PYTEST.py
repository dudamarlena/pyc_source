# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.form/test/setup_test.py
# Compiled at: 2014-05-21 17:45:45
"""
some initialisation stuff needed for each test
"""
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from tiddlyweb.config import config
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.store import NoBagError, NoRecipeError
from tiddlyweb.web import serve
from tiddlywebplugins.utils import get_store
from wsgi_intercept import httplib2_intercept
import wsgi_intercept, httplib2
BAGS = [
 'foo',
 'bar']
RECIPES = {'foobar': [
            ('foo', ''), ('bar', '')]}

def setup_store():
    """
    initialise a blank store, and fill it with some data
    """
    store = get_store(config)
    for bag in store.list_bags():
        store.delete(bag)

    for bag in BAGS:
        bag = Bag(bag)
        store.put(bag)

    for recipe in store.list_recipes():
        store.delete(recipe)

    for recipe, contents in RECIPES.iteritems():
        recipe = Recipe(recipe)
        recipe.set_recipe(contents)
        store.put(recipe)

    return store


def setup_web():
    """
    set up TiddlyWeb to run as a mock server
    This is required to get selector loaded
    """

    def app_fn():
        return serve.load_app()

    httplib2_intercept.install()
    wsgi_intercept.add_wsgi_intercept('test_domain', 8001, app_fn)