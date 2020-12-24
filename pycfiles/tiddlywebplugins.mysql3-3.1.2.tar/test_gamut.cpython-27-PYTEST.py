# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlywebplugins.mysql/test/test_gamut.py
# Compiled at: 2014-02-23 07:54:53
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, py.test
from tiddlyweb.config import config
from tiddlyweb.store import Store, NoBagError, NoUserError, NoRecipeError, NoTiddlerError
from tiddlyweb.model.bag import Bag
from tiddlyweb.model.recipe import Recipe
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.model.user import User
from tiddlywebplugins.mysql3 import Base
from base64 import b64encode
RANGE = 10

def setup_module(module):
    module.store = Store(config['server_store'][0], config['server_store'][1], {'tiddlyweb.config': config})
    Base.metadata.drop_all()
    Base.metadata.create_all()
    import warnings
    warnings.simplefilter('error')


def test_make_a_bunch():
    for x in xrange(RANGE):
        bag_name = 'bag%s' % x
        recipe_name = 'recipe%s' % x
        tiddler_name = 'tiddler%s' % x
        recipe_list = [(bag_name, '')]
        tiddler_text = 'hey ho %s' % x
        field_name = 'field%s' % x
        field_name2 = 'fieldone%s' % x
        tag_name = 'tag%s' % x
        user_name = 'user%s' % x
        user_pass = 'pass%s' % x
        user_note = 'note%s' % x
        user_roles = ['rolehold', 'role%s' % x]
        bag = Bag(bag_name)
        bag.policy.owner = 'owner%s' % x
        bag.policy.read = ['hi%s' % x, 'andextra']
        bag.policy.manage = ['R:hi%s' % x, 'andmanage']
        store.put(bag)
        recipe = Recipe(recipe_name)
        recipe.policy.owner = 'owner%s' % x
        recipe.policy.read = ['hi%s' % x, 'andextra']
        recipe.policy.manage = ['R:hi%s' % x, 'andmanage']
        recipe.set_recipe(recipe_list)
        store.put(recipe)
        tiddler = Tiddler(tiddler_name, bag_name)
        tiddler.text = tiddler_text
        tiddler.fields[field_name] = field_name
        tiddler.fields[field_name2] = field_name2
        tiddler.fields['server.host'] = 'gunky'
        tiddler.tags = [tag_name]
        store.put(tiddler)
        store.put(tiddler)
        user = User(user_name)
        user.set_password(user_pass)
        user.note = user_note
        for role in user_roles:
            user.add_role(role)

        store.put(user)

    bags = [ bag.name for bag in store.list_bags() ]
    recipes = [ recipe.name for recipe in store.list_recipes() ]
    users = [ user.usersign for user in store.list_users() ]
    @py_assert2 = len(bags)
    @py_assert4 = @py_assert2 == RANGE
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, RANGE)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(bags) if 'bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bags) else 'bags', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(RANGE) if 'RANGE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(RANGE) else 'RANGE'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = len(recipes)
    @py_assert4 = @py_assert2 == RANGE
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, RANGE)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(recipes) if 'recipes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipes) else 'recipes', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(RANGE) if 'RANGE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(RANGE) else 'RANGE'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = len(users)
    @py_assert4 = @py_assert2 == RANGE
    if not @py_assert4:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py5)s', ), (@py_assert2, RANGE)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(users) if 'users' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(users) else 'users', 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(RANGE) if 'RANGE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(RANGE) else 'RANGE'}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert2 = @py_assert4 = None
    for x in xrange(RANGE):
        bname = 'bag%s' % x
        rname = 'recipe%s' % x
        uname = 'user%s' % x
        @py_assert1 = bname in bags
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (bname, bags)) % {'py0': @pytest_ar._saferepr(bname) if 'bname' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bname) else 'bname', 'py2': @pytest_ar._saferepr(bags) if 'bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bags) else 'bags'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = rname in recipes
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (rname, recipes)) % {'py0': @pytest_ar._saferepr(rname) if 'rname' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(rname) else 'rname', 'py2': @pytest_ar._saferepr(recipes) if 'recipes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipes) else 'recipes'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert1 = uname in users
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('in', ), (@py_assert1,), ('%(py0)s in %(py2)s', ), (uname, users)) % {'py0': @pytest_ar._saferepr(uname) if 'uname' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(uname) else 'uname', 'py2': @pytest_ar._saferepr(users) if 'users' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(users) else 'users'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    tiddler = store.get(Tiddler('tiddler0', 'bag0'))
    @py_assert0 = tiddler.fields['field0']
    @py_assert3 = 'field0'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = tiddler.fields['fieldone0']
    @py_assert3 = 'fieldone0'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    bag = Bag('bag0')
    bag = store.get(bag)
    tiddlers = []
    for tiddler in store.list_bag_tiddlers(bag):
        tiddlers.append(store.get(tiddler))

    @py_assert2 = len(tiddlers)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.title
    @py_assert5 = 'tiddler0'
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.title\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = tiddlers[0].fields['field0']
    @py_assert3 = 'field0'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = tiddlers[0].fields['fieldone0']
    @py_assert3 = 'fieldone0'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = tiddlers[0]
    @py_assert2 = @py_assert0.tags
    @py_assert5 = ['tag0']
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.tags\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert2 = bag.policy
    @py_assert4 = @py_assert2.read
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['andextra', 'hi0']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.read\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = bag.policy
    @py_assert4 = @py_assert2.manage
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['R:hi0', 'andmanage']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.manage\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = bag.policy
    @py_assert3 = @py_assert1.owner
    @py_assert6 = 'owner0'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(bag) if 'bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bag) else 'bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    user = User('user1')
    user = store.get(user)
    @py_assert1 = user.usersign
    @py_assert4 = 'user1'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.usersign\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(user) if 'user' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user) else 'user', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = user.check_password
    @py_assert3 = 'pass1'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.check_password\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(user) if 'user' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user) else 'user', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = user.note
    @py_assert4 = 'note1'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.note\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(user) if 'user' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user) else 'user', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = 'role1'
    @py_assert4 = user.list_roles
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.list_roles\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(user) if 'user' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user) else 'user', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'rolehold'
    @py_assert4 = user.list_roles
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 in @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.list_roles\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(user) if 'user' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user) else 'user', 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    recipe = Recipe('recipe2')
    recipe = store.get(recipe)
    @py_assert1 = recipe.name
    @py_assert4 = 'recipe2'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    bags = [ bag_name for bag_name, filter in recipe.get_recipe() ]
    @py_assert2 = len(bags)
    @py_assert5 = 1
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(bags) if 'bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bags) else 'bags', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = 'bag2'
    @py_assert2 = @py_assert0 in bags
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, bags)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(bags) if 'bags' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bags) else 'bags'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert2 = recipe.policy
    @py_assert4 = @py_assert2.read
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['andextra', 'hi2']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.read\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert2 = recipe.policy
    @py_assert4 = @py_assert2.manage
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['R:hi2', 'andmanage']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.manage\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = recipe.policy
    @py_assert3 = @py_assert1.owner
    @py_assert6 = 'owner2'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    recipe.policy.manage = [
     'andmanage']
    store.put(recipe)
    recipe = Recipe('recipe2')
    recipe = store.get(recipe)
    @py_assert1 = recipe.policy
    @py_assert3 = @py_assert1.manage
    @py_assert6 = ['andmanage']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(recipe) if 'recipe' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(recipe) else 'recipe', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    store.delete(bag)
    py.test.raises(NoBagError, 'store.delete(bag)')
    py.test.raises(NoBagError, 'store.get(bag)')
    store.delete(recipe)
    py.test.raises(NoRecipeError, 'store.delete(recipe)')
    py.test.raises(NoRecipeError, 'store.get(recipe)')
    store.delete(user)
    py.test.raises(NoUserError, 'store.delete(user)')
    py.test.raises(NoUserError, 'store.get(user)')
    tiddler = Tiddler('tiddler9', 'bag9')
    store.get(tiddler)
    @py_assert1 = tiddler.bag
    @py_assert4 = 'bag9'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.bag\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert4 = 'hey ho 9'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.tags
    @py_assert4 = ['tag9']
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.tags\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = tiddler.fields['field9']
    @py_assert3 = 'field9'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'server.host'
    @py_assert4 = tiddler.fields
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.fields\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    store.delete(tiddler)
    py.test.raises(NoTiddlerError, 'store.delete(tiddler)')
    py.test.raises(NoTiddlerError, 'store.get(tiddler)')
    return


def test_binary_tiddler():
    tiddler = Tiddler('binary', 'bag8')
    tiddler.type = 'application/binary'
    tiddler.text = 'not really binary'
    store.put(tiddler)
    new_tiddler = Tiddler('binary', 'bag8')
    new_tiddler = store.get(new_tiddler)
    @py_assert1 = new_tiddler.title
    @py_assert4 = 'binary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(new_tiddler) if 'new_tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_tiddler) else 'new_tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = new_tiddler.type
    @py_assert4 = 'application/binary'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.type\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(new_tiddler) if 'new_tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_tiddler) else 'new_tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert5 = 'not really binary'
    @py_assert7 = b64encode(@py_assert5)
    @py_assert3 = @py_assert1 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py8)s\n{%(py8)s = %(py4)s(%(py6)s)\n}', ), (@py_assert1, @py_assert7)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py8': @pytest_ar._saferepr(@py_assert7), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(b64encode) if 'b64encode' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(b64encode) else 'b64encode', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_handle_empty_policy():
    bag = Bag('empty')
    store.put(bag)
    new_bag = store.get(Bag('empty'))
    @py_assert1 = new_bag.policy
    @py_assert3 = @py_assert1.read
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(new_bag) if 'new_bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_bag) else 'new_bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = new_bag.policy
    @py_assert3 = @py_assert1.manage
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.manage\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(new_bag) if 'new_bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_bag) else 'new_bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = new_bag.policy
    @py_assert3 = @py_assert1.create
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.create\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(new_bag) if 'new_bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_bag) else 'new_bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = new_bag.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(new_bag) if 'new_bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_bag) else 'new_bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = new_bag.policy
    @py_assert3 = @py_assert1.accept
    @py_assert6 = []
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.accept\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(new_bag) if 'new_bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_bag) else 'new_bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = new_bag.policy
    @py_assert3 = @py_assert1.owner
    @py_assert5 = @py_assert3 == None
    if not @py_assert5:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.owner\n} == %(py6)s', ), (@py_assert3, None)) % {'py0': @pytest_ar._saferepr(new_bag) if 'new_bag' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(new_bag) else 'new_bag', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(None) if 'None' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(None) else 'None'}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    return


def test_tiddler_revisions():
    bag_name = 'bag8'
    for i in xrange(20):
        tiddler = Tiddler('oh hi', bag_name)
        tiddler.text = '%s times we go' % i
        tiddler.fields['%s' % i] = '%s' % i
        tiddler.fields['other%s' % i] = '%s' % i
        tiddler.fields['carutther%s' % i] = 'x%s' % i
        store.put(tiddler)

    revisions = store.list_tiddler_revisions(Tiddler('oh hi', bag_name))
    @py_assert2 = len(revisions)
    @py_assert5 = 20
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(revisions) if 'revisions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(revisions) else 'revisions', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    first_revision = revisions[(-1)]
    tiddler = Tiddler('oh hi', bag_name)
    tiddler.revision = first_revision + 13
    tiddler = store.get(tiddler)
    @py_assert1 = tiddler.title
    @py_assert4 = 'oh hi'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert4 = '13 times we go'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = tiddler.fields['13']
    @py_assert3 = '13'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = tiddler.fields['other13']
    @py_assert3 = '13'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = tiddler.fields['carutther13']
    @py_assert3 = 'x13'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '12'
    @py_assert4 = tiddler.fields
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.fields\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tiddler.revision = 90
    py.test.raises(NoTiddlerError, 'store.get(tiddler)')
    py.test.raises(NoTiddlerError, 'store.list_tiddler_revisions(Tiddler(u"sleepy", u"cow"))')
    return


def test_interleaved_tiddler_revisions():
    bag_name = 'bag8'
    for i in xrange(20):
        tiddler1 = Tiddler('oh yes', bag_name)
        tiddler2 = Tiddler('oh no', bag_name)
        tiddler1.text = '%s times we yes' % i
        tiddler2.text = '%s times we no' % i
        tiddler1.fields['%s' % i] = '%s' % i
        tiddler2.fields['%s' % i] = '%s' % i
        store.put(tiddler1)
        store.put(tiddler2)

    revisions = store.list_tiddler_revisions(Tiddler('oh yes', bag_name))
    @py_assert2 = len(revisions)
    @py_assert5 = 20
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(revisions) if 'revisions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(revisions) else 'revisions', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    first_revision = revisions[(-1)]
    tiddler = Tiddler('oh yes', bag_name)
    tiddler.revision = first_revision + 26
    tiddler = store.get(tiddler)
    @py_assert1 = tiddler.title
    @py_assert4 = 'oh yes'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = tiddler.text
    @py_assert4 = '13 times we yes'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = tiddler.fields['13']
    @py_assert3 = '13'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = '12'
    @py_assert4 = tiddler.fields
    @py_assert2 = @py_assert0 not in @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py5)s\n{%(py5)s = %(py3)s.fields\n}', ), (@py_assert0, @py_assert4)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    tiddler.revision = 9999999
    py.test.raises(NoTiddlerError, 'store.get(tiddler)')
    py.test.raises(NoTiddlerError, 'store.list_tiddler_revisions(Tiddler(u"sleepy", u"cow"))')
    return


def test_tiddler_no_bag():
    tiddler = Tiddler('hi')
    py.test.raises(NoBagError, 'store.put(tiddler)')


def test_list_tiddlers_no_bag():
    bag = Bag('carne')
    try:
        py.test.raises(NoBagError, 'store.list_bag_tiddlers(bag).next()')
    except AttributeError:
        if not True:
            @py_format1 = 'assert %(py0)s' % {'py0': @pytest_ar._saferepr(True) if 'True' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(True) else 'True'}
            raise AssertionError(@pytest_ar._format_explanation(@py_format1))


def xtest_case_sensitive():
    bag = Bag('testcs')
    store.put(bag)
    tiddlera = Tiddler('testtiddler', 'testcs')
    tiddlera.text = 'a'
    store.put(tiddlera)
    tiddlerb = Tiddler('TestTiddler', 'testcs')
    tiddlerb.text = 'b'
    store.put(tiddlerb)
    tiddlerc = Tiddler('TestTiddler', 'testcs')
    tiddlerc = store.get(tiddlerc)
    @py_assert1 = tiddlerc.text
    @py_assert4 = 'b'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddlerc) if 'tiddlerc' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlerc) else 'tiddlerc', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    tiddlerd = Tiddler('testtiddler', 'testcs')
    tiddlerd = store.get(tiddlerd)
    @py_assert1 = tiddlerd.text
    @py_assert4 = 'a'
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0': @pytest_ar._saferepr(tiddlerd) if 'tiddlerd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlerd) else 'tiddlerd', 'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    return


def test_2bag_policy():
    bag = Bag('pone')
    bag.policy.read = ['cdent']
    bag.policy.write = ['cdent']
    store.put(bag)
    bag = Bag('ptwo')
    bag.policy.read = ['cdent', 'fnd']
    bag.policy.write = ['cdent']
    store.put(bag)
    pone = store.get(Bag('pone'))
    ptwo = store.get(Bag('ptwo'))
    @py_assert1 = pone.policy
    @py_assert3 = @py_assert1.read
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = pone.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = ptwo.policy
    @py_assert4 = @py_assert2.read
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['cdent', 'fnd']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.read\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(ptwo) if 'ptwo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptwo) else 'ptwo', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = ptwo.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(ptwo) if 'ptwo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptwo) else 'ptwo', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    store.delete(pone)
    ptwo = store.get(Bag('ptwo'))
    @py_assert2 = ptwo.policy
    @py_assert4 = @py_assert2.read
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['cdent', 'fnd']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.read\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(ptwo) if 'ptwo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptwo) else 'ptwo', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = ptwo.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(ptwo) if 'ptwo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptwo) else 'ptwo', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    bag = Bag('pone')
    bag.policy.read = ['cdent']
    bag.policy.write = ['cdent']
    store.put(bag)
    pone = store.get(Bag('pone'))
    @py_assert1 = pone.policy
    @py_assert3 = @py_assert1.read
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = pone.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    pone.policy.read.append('fnd')
    store.put(pone)
    pone = store.get(Bag('pone'))
    @py_assert2 = pone.policy
    @py_assert4 = @py_assert2.read
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['cdent', 'fnd']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.read\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    return


def test_2recipe_policy():
    recipe = Recipe('pone')
    recipe.policy.read = ['cdent']
    recipe.policy.write = ['cdent']
    store.put(recipe)
    recipe = Recipe('ptwo')
    recipe.policy.read = ['cdent', 'fnd']
    recipe.policy.write = ['cdent']
    store.put(recipe)
    pone = store.get(Recipe('pone'))
    ptwo = store.get(Recipe('ptwo'))
    @py_assert1 = pone.policy
    @py_assert3 = @py_assert1.read
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = pone.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert2 = ptwo.policy
    @py_assert4 = @py_assert2.read
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['cdent', 'fnd']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.read\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(ptwo) if 'ptwo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptwo) else 'ptwo', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = ptwo.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(ptwo) if 'ptwo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptwo) else 'ptwo', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    store.delete(pone)
    ptwo = store.get(Recipe('ptwo'))
    @py_assert2 = ptwo.policy
    @py_assert4 = @py_assert2.read
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['cdent', 'fnd']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.read\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(ptwo) if 'ptwo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptwo) else 'ptwo', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    @py_assert1 = ptwo.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(ptwo) if 'ptwo' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ptwo) else 'ptwo', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    recipe = Recipe('pone')
    recipe.policy.read = ['cdent']
    recipe.policy.write = ['cdent']
    store.put(recipe)
    pone = store.get(Recipe('pone'))
    @py_assert1 = pone.policy
    @py_assert3 = @py_assert1.read
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.read\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert1 = pone.policy
    @py_assert3 = @py_assert1.write
    @py_assert6 = ['cdent']
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.policy\n}.write\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    pone.policy.read.append('fnd')
    store.put(pone)
    pone = store.get(Recipe('pone'))
    @py_assert2 = pone.policy
    @py_assert4 = @py_assert2.read
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['cdent', 'fnd']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.policy\n}.read\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(pone) if 'pone' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pone) else 'pone', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    return


def test_revisions_deletions():
    tiddler = Tiddler('tone', 'pone')
    tiddler.text = 'revision1'
    tiddler.tags = ['1', '2']
    store.put(tiddler)
    tiddler.text = 'revision2'
    tiddler.tags = ['3', '4']
    store.put(tiddler)
    revisions = store.list_tiddler_revisions(tiddler)
    @py_assert2 = len(revisions)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(revisions) if 'revisions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(revisions) else 'revisions', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    store.delete(tiddler)
    py.test.raises(NoTiddlerError, 'store.list_tiddler_revisions(tiddler)')
    return


def test_bag_deletes_tiddlers():
    tiddler = Tiddler('tone', 'pone')
    tiddler.text = ''
    store.put(tiddler)
    tiddler = Tiddler('uone', 'pone')
    tiddler.text = ''
    store.put(tiddler)
    bag = Bag('pone')
    tiddlers = list(store.list_bag_tiddlers(bag))
    @py_assert2 = len(tiddlers)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(tiddlers) if 'tiddlers' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddlers) else 'tiddlers', 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    store.delete(bag)
    bag = Bag('pone')
    py.test.raises(NoBagError, 'list(store.list_bag_tiddlers(bag))')
    py.test.raises(NoTiddlerError, 'store.list_tiddler_revisions(tiddler)')
    return


def test_multi_same_tag_tiddler():
    bag = Bag('holder')
    store.put(bag)
    tiddler = Tiddler('me', 'holder')
    tiddler.text = 'hi'
    tiddler.tags = ['foo']
    store.put(tiddler)
    tiddler2 = Tiddler('me', 'holder')
    tiddler2 = store.get(tiddler2)
    tiddler2.tags.append('bar')
    tiddler2.tags.append('bar')
    store.put(tiddler2)
    tiddler3 = store.get(Tiddler('me', 'holder'))
    @py_assert2 = tiddler3.tags
    @py_assert4 = sorted(@py_assert2)
    @py_assert7 = ['bar', 'foo']
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.tags\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(tiddler3) if 'tiddler3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler3) else 'tiddler3', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    return


def test_multi_role_user():
    user = User('cdent')
    user.add_role('cow')
    user.add_role('cow')
    store.put(user)
    user2 = store.get(User('cdent'))
    @py_assert2 = user2.roles
    @py_assert4 = list(@py_assert2)
    @py_assert7 = ['cow']
    @py_assert6 = @py_assert4 == @py_assert7
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.roles\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0': @pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list', 'py1': @pytest_ar._saferepr(user2) if 'user2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(user2) else 'user2', 'py8': @pytest_ar._saferepr(@py_assert7), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    return


def test_long_tiddler_title():
    long_title = 'I would not do that if I were you, it might have consequences more than dire than you could possibly imagine. So dire you might have an oh no moment something severe.'
    tiddler1 = Tiddler(long_title + '1', 'holder')
    tiddler1.text = 'tiddler1'
    tiddler2 = Tiddler(long_title + '1', 'holder')
    tiddler2.text = 'tiddler2'
    py.test.raises(TypeError, 'store.put(tiddler1)')
    py.test.raises(TypeError, 'store.put(tiddler2)')
    py.test.raises(NoTiddlerError, 'store.get(tiddler1)')
    py.test.raises(NoTiddlerError, 'store.get(tiddler2)')


@py.test.mark.xfail
def test_emoji_title():
    """
    We expect this to fail because we're using a) old mysql
    b) without the utf8mb4 encoding type.
    See: https://github.com/TiddlySpace/tiddlyspace/issues/1033

    The fix is to use mysql 5.5 or beyond.
    """
    title = ('😗').decode('utf-8')
    store.put(Bag(title))
    tiddler = Tiddler(title, title)
    tiddler.text = 'some stuff and zomg %s' % title
    tiddler.tags = [title]
    tiddler.fields[title] = title
    store.put(tiddler)
    tiddler2 = store.get(Tiddler(title, title))
    @py_assert1 = tiddler2.title
    @py_assert3 = @py_assert1 == title
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py4)s', ), (@py_assert1, title)) % {'py0': @pytest_ar._saferepr(tiddler2) if 'tiddler2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler2) else 'tiddler2', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(title) if 'title' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(title) else 'title'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert1 = tiddler2.text
    @py_assert5 = tiddler.text
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.text\n} == %(py6)s\n{%(py6)s = %(py4)s.text\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(tiddler2) if 'tiddler2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler2) else 'tiddler2', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = tiddler2.tags
    @py_assert5 = tiddler.tags
    @py_assert3 = @py_assert1 == @py_assert5
    if not @py_assert3:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.tags\n} == %(py6)s\n{%(py6)s = %(py4)s.tags\n}', ), (@py_assert1, @py_assert5)) % {'py0': @pytest_ar._saferepr(tiddler2) if 'tiddler2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler2) else 'tiddler2', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(tiddler) if 'tiddler' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tiddler) else 'tiddler', 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert0 = tiddler2.tags[0]
    @py_assert2 = @py_assert0 == title
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, title)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(title) if 'title' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(title) else 'title'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = tiddler2.fields[title]
    @py_assert3 = tiddler.fields[title]
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = tiddler2.fields[title]
    @py_assert2 = @py_assert0 == title
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, title)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(title) if 'title' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(title) else 'title'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    return