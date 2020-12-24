# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checkers_utils.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 9888 bytes
"""Tests for the pylint.checkers.utils module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid, pytest
from pylint.checkers import utils

@pytest.mark.parametrize('name,expected', [
 ('min', True),
 ('__builtins__', True),
 ('__path__', False),
 ('__file__', False),
 ('whatever', False),
 ('mybuiltin', False)])
def testIsBuiltin(name, expected):
    @py_assert1 = utils.is_builtin
    @py_assert4 = @py_assert1(name)
    @py_assert6 = @py_assert4 == expected
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=32)
    if not @py_assert6:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.is_builtin\n}(%(py3)s)\n} == %(py7)s', ), (@py_assert4, expected)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert4 = @py_assert6 = None


@pytest.mark.parametrize('fn,kw', [
 (
  'foo(3)', {'keyword': 'bar'}), ('foo(one=a, two=b, three=c)', {'position': 1})])
def testGetArgumentFromCallError(fn, kw):
    with pytest.raises(utils.NoSuchArgumentError):
        node = astroid.extract_node(fn)
        (utils.get_argument_from_call)(node, **kw)


@pytest.mark.parametrize('fn,kw', [('foo(bar=3)', {'keyword': 'bar'}), ('foo(a, b, c)', {'position': 1})])
def testGetArgumentFromCallExists(fn, kw):
    node = astroid.extract_node(fn)
    @py_assert1 = utils.get_argument_from_call
    @py_assert5 = @py_assert1(node, **kw)
    @py_assert8 = None
    @py_assert7 = @py_assert5 is not @py_assert8
    if @py_assert7 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=50)
    if not @py_assert7:
        @py_format10 = @pytest_ar._call_reprcompare(('is not', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get_argument_from_call\n}(%(py3)s, **%(py4)s)\n} is not %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py4':@pytest_ar._saferepr(kw) if 'kw' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kw) else 'kw',  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert5 = @py_assert7 = @py_assert8 = None


def testGetArgumentFromCall():
    node = astroid.extract_node('foo(a, not_this_one=1, this_one=2)')
    arg = utils.get_argument_from_call(node, position=2, keyword='this_one')
    @py_assert0 = 2
    @py_assert4 = arg.value
    @py_assert2 = @py_assert0 == @py_assert4
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=56)
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.value\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(arg) if 'arg' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(arg) else 'arg',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    node = astroid.extract_node('foo(a)')
    with pytest.raises(utils.NoSuchArgumentError):
        utils.get_argument_from_call(node, position=1)
    with pytest.raises(ValueError):
        utils.get_argument_from_call(node, None, None)
    name = utils.get_argument_from_call(node, position=0)
    @py_assert1 = name.name
    @py_assert4 = 'a'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=64)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(name) if 'name' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(name) else 'name',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None


def test_error_of_type():
    nodes = astroid.extract_node('\n    try: pass\n    except AttributeError: #@\n         pass\n    try: pass\n    except Exception: #@\n         pass\n    except: #@\n         pass\n    ')
    @py_assert1 = utils.error_of_type
    @py_assert3 = nodes[0]
    @py_assert6 = @py_assert1(@py_assert3, AttributeError)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=80)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.error_of_type\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(AttributeError) if 'AttributeError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(AttributeError) else 'AttributeError',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = utils.error_of_type
    @py_assert3 = nodes[0]
    @py_assert5 = (
     AttributeError,)
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=81)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.error_of_type\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None
    @py_assert1 = utils.error_of_type
    @py_assert3 = nodes[0]
    @py_assert6 = @py_assert1(@py_assert3, Exception)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=82)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.error_of_type\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(Exception) if 'Exception' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Exception) else 'Exception',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = utils.error_of_type
    @py_assert3 = nodes[1]
    @py_assert6 = @py_assert1(@py_assert3, Exception)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=83)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.error_of_type\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(Exception) if 'Exception' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Exception) else 'Exception',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = utils.error_of_type
    @py_assert3 = nodes[2]
    @py_assert6 = @py_assert1(@py_assert3, ImportError)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=84)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.error_of_type\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(ImportError) if 'ImportError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ImportError) else 'ImportError',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_node_ignores_exception():
    nodes = astroid.extract_node('\n    try:\n        1/0 #@\n    except ZeroDivisionError:\n        pass\n    try:\n        1/0 #@\n    except Exception:\n        pass\n    try:\n        2/0 #@\n    except:\n        pass\n    try:\n        1/0 #@\n    except ValueError:\n        pass\n    ')
    @py_assert1 = utils.node_ignores_exception
    @py_assert3 = nodes[0]
    @py_assert6 = @py_assert1(@py_assert3, ZeroDivisionError)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=108)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.node_ignores_exception\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(ZeroDivisionError) if 'ZeroDivisionError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ZeroDivisionError) else 'ZeroDivisionError',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = utils.node_ignores_exception
    @py_assert3 = nodes[1]
    @py_assert6 = @py_assert1(@py_assert3, ZeroDivisionError)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=109)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.node_ignores_exception\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(ZeroDivisionError) if 'ZeroDivisionError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ZeroDivisionError) else 'ZeroDivisionError',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = utils.node_ignores_exception
    @py_assert3 = nodes[2]
    @py_assert6 = @py_assert1(@py_assert3, ZeroDivisionError)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=110)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.node_ignores_exception\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(ZeroDivisionError) if 'ZeroDivisionError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ZeroDivisionError) else 'ZeroDivisionError',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None
    @py_assert1 = utils.node_ignores_exception
    @py_assert3 = nodes[3]
    @py_assert6 = @py_assert1(@py_assert3, ZeroDivisionError)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=111)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.node_ignores_exception\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(ZeroDivisionError) if 'ZeroDivisionError' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(ZeroDivisionError) else 'ZeroDivisionError',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None


def test_is_subclass_of_node_b_derived_from_node_a():
    nodes = astroid.extract_node('\n    class Superclass: #@\n        pass\n\n    class Subclass(Superclass): #@\n        pass\n    ')
    @py_assert1 = utils.is_subclass_of
    @py_assert3 = nodes[1]
    @py_assert5 = nodes[0]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    if @py_assert7 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=124)
    if not @py_assert7:
        @py_format9 = 'assert %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_subclass_of\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = None


def test_is_subclass_of_node_b_not_derived_from_node_a():
    nodes = astroid.extract_node('\n    class OneClass: #@\n        pass\n\n    class AnotherClass: #@\n        pass\n    ')
    @py_assert1 = utils.is_subclass_of
    @py_assert3 = nodes[1]
    @py_assert5 = nodes[0]
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=137)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_subclass_of\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_is_subclass_of_not_classdefs():
    node = astroid.extract_node('\n    class OneClass: #@\n        pass\n    ')
    @py_assert1 = utils.is_subclass_of
    @py_assert3 = None
    @py_assert6 = @py_assert1(@py_assert3, node)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=147)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.is_subclass_of\n}(%(py4)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert1 = utils.is_subclass_of
    @py_assert4 = None
    @py_assert6 = @py_assert1(node, @py_assert4)
    @py_assert8 = not @py_assert6
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=148)
    if not @py_assert8:
        @py_format9 = 'assert not %(py7)s\n{%(py7)s = %(py2)s\n{%(py2)s = %(py0)s.is_subclass_of\n}(%(py3)s, %(py5)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = None
    @py_assert1 = utils.is_subclass_of
    @py_assert3 = None
    @py_assert5 = None
    @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
    @py_assert9 = not @py_assert7
    if @py_assert9 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=149)
    if not @py_assert9:
        @py_format10 = 'assert not %(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.is_subclass_of\n}(%(py4)s, %(py6)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None


def test_parse_format_method_string():
    samples = [
     ('{}', 1),
     ('{}:{}', 2),
     ('{field}', 1),
     ('{:5}', 1),
     ('{:10}', 1),
     ('{field:10}', 1),
     ('{field:10}{{}}', 1),
     ('{:5}{!r:10}', 2),
     ('{:5}{}{{}}{}', 3),
     ('{0}{1}{0}', 2),
     ('Coordinates: {latitude}, {longitude}', 2),
     ('X: {0[0]};  Y: {0[1]}', 1),
     ('{:*^30}', 1),
     ('{!r:}', 1)]
    for fmt, count in samples:
        keys, num_args, pos_args = utils.parse_format_method_string(fmt)
        keyword_args = len(set(k for k, l in keys if not isinstance(k, int)))
        @py_assert2 = keyword_args + num_args
        @py_assert4 = @py_assert2 + pos_args
        @py_assert5 = @py_assert4 == count
        if @py_assert5 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=172)
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('((%(py0)s + %(py1)s) + %(py3)s) == %(py6)s', ), (@py_assert4, count)) % {'py0':@pytest_ar._saferepr(keyword_args) if 'keyword_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(keyword_args) else 'keyword_args',  'py1':@pytest_ar._saferepr(num_args) if 'num_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(num_args) else 'num_args',  'py3':@pytest_ar._saferepr(pos_args) if 'pos_args' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pos_args) else 'pos_args',  'py6':@pytest_ar._saferepr(count) if 'count' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(count) else 'count'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None


def test_inherit_from_std_ex_recursive_definition():
    node = astroid.extract_node('\n      import datetime\n      class First(datetime.datetime):\n        pass\n      class Second(datetime.datetime): #@\n        pass\n      datetime.datetime = First\n      datetime.datetime = Second\n      ')
    @py_assert1 = utils.inherit_from_std_ex
    @py_assert4 = @py_assert1(node)
    @py_assert6 = not @py_assert4
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=187)
    if not @py_assert6:
        @py_format7 = 'assert not %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.inherit_from_std_ex\n}(%(py3)s)\n}' % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert4 = @py_assert6 = None


class TestGetNodeLastLineno:

    def test_get_node_last_lineno_simple(self):
        node = astroid.extract_node('\n            pass\n        ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 2
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=197)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_if_simple(self):
        node = astroid.extract_node('\n            if True:\n                print(1)\n                pass\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 4
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=207)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_if_elseif_else(self):
        node = astroid.extract_node('\n            if True:\n                print(1)\n            elif False:\n                print(2)\n            else:\n                print(3)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 7
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=220)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_while(self):
        node = astroid.extract_node('\n            while True:\n                print(1)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 3
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=229)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_while_else(self):
        node = astroid.extract_node('\n            while True:\n                print(1)\n            else:\n                print(2)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 5
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=240)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_for(self):
        node = astroid.extract_node('\n            for x in range(0, 5):\n                print(1)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 3
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=249)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_for_else(self):
        node = astroid.extract_node('\n            for x in range(0, 5):\n                print(1)\n            else:\n                print(2)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 5
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=260)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_try(self):
        node = astroid.extract_node('\n            try:\n                print(1)\n            except ValueError:\n                print(2)\n            except Exception:\n                print(3)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 7
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=273)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_try_except_else(self):
        node = astroid.extract_node('\n            try:\n                print(1)\n            except Exception:\n                print(2)\n                print(3)\n            else:\n                print(4)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 8
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=287)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_try_except_finally(self):
        node = astroid.extract_node('\n            try:\n                print(1)\n            except Exception:\n                print(2)\n            finally:\n                print(4)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 7
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=300)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_try_except_else_finally(self):
        node = astroid.extract_node('\n            try:\n                print(1)\n            except Exception:\n                print(2)\n            else:\n                print(3)\n            finally:\n                print(4)\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 9
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=315)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_with(self):
        node = astroid.extract_node('\n            with x as y:\n                print(1)\n                pass\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 4
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=325)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_method(self):
        node = astroid.extract_node('\n            def x(a, b):\n                print(a, b)\n                pass\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 4
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=335)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_decorator(self):
        node = astroid.extract_node('\n            @decor()\n            def x(a, b):\n                print(a, b)\n                pass\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 5
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=346)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_class(self):
        node = astroid.extract_node('\n            class C(object):\n                CONST = True\n\n                def x(self, b):\n                    print(b)\n\n                def y(self):\n                    pass\n                    pass\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 10
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=362)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None

    def test_get_node_last_lineno_combined(self):
        node = astroid.extract_node('\n            class C(object):\n                CONST = True\n\n                def y(self):\n                    try:\n                        pass\n                    except:\n                        pass\n                    finally:\n                        pass\n            ')
        @py_assert1 = utils.get_node_last_lineno
        @py_assert4 = @py_assert1(node)
        @py_assert7 = 11
        @py_assert6 = @py_assert4 == @py_assert7
        if @py_assert6 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_checkers_utils.py', lineno=379)
        if not @py_assert6:
            @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.get_node_last_lineno\n}(%(py3)s)\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(utils) if 'utils' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(utils) else 'utils',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(node) if 'node' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(node) else 'node',  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
            @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert7 = None