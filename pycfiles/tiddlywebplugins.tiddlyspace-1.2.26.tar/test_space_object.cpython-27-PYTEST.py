# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cdent/src/tiddlyspace/test/test_space_object.py
# Compiled at: 2012-11-06 08:06:18
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, py.test
from tiddlywebplugins.tiddlyspace.space import Space

def test_private_bag():
    space = Space('cat')
    @py_assert1 = space.private_bag
    @py_assert3 = @py_assert1()
    @py_assert6 = 'cat_private'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.private_bag\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(space) if 'space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space) else 'space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_public_bag():
    space = Space('cat')
    @py_assert1 = space.public_bag
    @py_assert3 = @py_assert1()
    @py_assert6 = 'cat_public'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.public_bag\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(space) if 'space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space) else 'space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_private_recipe():
    space = Space('cat')
    @py_assert1 = space.private_recipe
    @py_assert3 = @py_assert1()
    @py_assert6 = 'cat_private'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.private_recipe\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(space) if 'space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space) else 'space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_public_recipe():
    space = Space('cat')
    @py_assert1 = space.public_recipe
    @py_assert3 = @py_assert1()
    @py_assert6 = 'cat_public'
    @py_assert5 = @py_assert3 == @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.public_recipe\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0': @pytest_ar._saferepr(space) if 'space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space) else 'space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    return


def test_list_bags():
    space = Space('cat')
    @py_assert2 = space.list_bags
    @py_assert4 = @py_assert2()
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['cat_archive', 'cat_private', 'cat_public']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.list_bags\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(space) if 'space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space) else 'space', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    return


def test_list_recipes():
    space = Space('cat')
    @py_assert2 = space.list_recipes
    @py_assert4 = @py_assert2()
    @py_assert6 = sorted(@py_assert4)
    @py_assert9 = ['cat_private', 'cat_public']
    @py_assert8 = @py_assert6 == @py_assert9
    if not @py_assert8:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.list_recipes\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0': @pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted', 'py1': @pytest_ar._saferepr(space) if 'space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(space) else 'space', 'py10': @pytest_ar._saferepr(@py_assert9), 'py3': @pytest_ar._saferepr(@py_assert2), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None
    return


def test_name_from_recipe():
    @py_assert1 = Space.name_from_recipe
    @py_assert3 = 'cat_private'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'cat'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.name_from_recipe\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    py.test.raises(ValueError, 'Space.name_from_recipe("cat_ball")')
    return


def test_name_from_bag():
    @py_assert1 = Space.name_from_bag
    @py_assert3 = 'cat_private'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert8 = 'cat'
    @py_assert7 = @py_assert5 == @py_assert8
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.name_from_bag\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py9': @pytest_ar._saferepr(@py_assert8), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
    py.test.raises(ValueError, 'Space.name_from_bag("cat_ball")')
    return


def test_bag_is():
    @py_assert1 = Space.bag_is_public
    @py_assert3 = 'cat_public'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_public\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = Space.bag_is_public
    @py_assert3 = 'cat_private'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_public\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = Space.bag_is_public
    @py_assert3 = '_public'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_public\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = Space.bag_is_private
    @py_assert3 = 'cat_private'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_private\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = Space.bag_is_private
    @py_assert3 = 'cat_public'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_private\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = Space.bag_is_private
    @py_assert3 = '_private'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_private\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_recipe_is():
    @py_assert1 = Space.recipe_is_public
    @py_assert3 = 'cat_public'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.recipe_is_public\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = Space.recipe_is_public
    @py_assert3 = 'cat_private'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.recipe_is_public\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = Space.recipe_is_private
    @py_assert3 = 'cat_private'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.recipe_is_private\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = Space.recipe_is_private
    @py_assert3 = 'cat_public'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.recipe_is_private\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return


def test_bag_is_associate():
    @py_assert1 = Space.bag_is_associate
    @py_assert3 = 'cat_archive'
    @py_assert5 = @py_assert1(@py_assert3)
    if not @py_assert5:
        @py_format7 = 'assert %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_associate\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    @py_assert1 = Space.bag_is_associate
    @py_assert3 = 'cat_poo'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_associate\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = Space.bag_is_associate
    @py_assert3 = '_archive'
    @py_assert5 = @py_assert1(@py_assert3)
    @py_assert7 = not @py_assert5
    if not @py_assert7:
        @py_format8 = 'assert not %(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.bag_is_associate\n}(%(py4)s)\n}' % {'py0': @pytest_ar._saferepr(Space) if 'Space' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Space) else 'Space', 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    return