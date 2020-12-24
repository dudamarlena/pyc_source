# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 3795 bytes
"""
 for the visitors.diadefs module
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os, astroid, pytest
from astroid import bases, nodes
from pylint.pyreverse import inspector
from unittest_pyreverse_writer import get_project

@pytest.fixture
def project():
    project = get_project('data', 'data')
    linker = inspector.Linker(project)
    linker.visit(project)
    return project


def test_class_implements(project):
    klass = project.get_module('data.clientmodule_test')['Ancestor']
    @py_assert2 = 'implements'
    @py_assert4 = hasattr(klass, @py_assert2)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=30)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr',  'py1':@pytest_ar._saferepr(klass) if 'klass' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(klass) else 'klass',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = klass.implements
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 1
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=31)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.implements\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(klass) if 'klass' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(klass) else 'klass',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None
    @py_assert1 = klass.implements[0]
    @py_assert4 = nodes.ClassDef
    @py_assert6 = isinstance(@py_assert1, @py_assert4)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=32)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py0)s(%(py2)s, %(py5)s\n{%(py5)s = %(py3)s.ClassDef\n})\n}' % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(nodes) if 'nodes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(nodes) else 'nodes',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert0 = klass.implements[0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'Interface'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=33)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None


def test_class_implements_specialization(project):
    klass = project.get_module('data.clientmodule_test')['Specialization']
    @py_assert2 = 'implements'
    @py_assert4 = hasattr(klass, @py_assert2)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=38)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr',  'py1':@pytest_ar._saferepr(klass) if 'klass' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(klass) else 'klass',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    @py_assert2 = klass.implements
    @py_assert4 = len(@py_assert2)
    @py_assert7 = 0
    @py_assert6 = @py_assert4 == @py_assert7
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=39)
    if not @py_assert6:
        @py_format9 = @pytest_ar._call_reprcompare(('==', ), (@py_assert6,), ('%(py5)s\n{%(py5)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.implements\n})\n} == %(py8)s', ), (@py_assert4, @py_assert7)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(klass) if 'klass' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(klass) else 'klass',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py8':@pytest_ar._saferepr(@py_assert7)}
        @py_format11 = 'assert %(py10)s' % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert7 = None


def test_locals_assignment_resolution(project):
    klass = project.get_module('data.clientmodule_test')['Specialization']
    @py_assert2 = 'locals_type'
    @py_assert4 = hasattr(klass, @py_assert2)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=44)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr',  'py1':@pytest_ar._saferepr(klass) if 'klass' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(klass) else 'klass',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    type_dict = klass.locals_type
    @py_assert2 = len(type_dict)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=46)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(type_dict) if 'type_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type_dict) else 'type_dict',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    keys = sorted(type_dict.keys())
    @py_assert2 = ['TYPE', 'top']
    @py_assert1 = keys == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=48)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (keys, @py_assert2)) % {'py0':@pytest_ar._saferepr(keys) if 'keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(keys) else 'keys',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = type_dict['TYPE']
    @py_assert3 = len(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=49)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = type_dict['TYPE'][0]
    @py_assert2 = @py_assert0.value
    @py_assert5 = 'final class'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=50)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.value\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert1 = type_dict['top']
    @py_assert3 = len(@py_assert1)
    @py_assert6 = 1
    @py_assert5 = @py_assert3 == @py_assert6
    if @py_assert5 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=51)
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = type_dict['top'][0]
    @py_assert2 = @py_assert0.value
    @py_assert5 = 'class'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=52)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.value\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None


def test_instance_attrs_resolution(project):
    klass = project.get_module('data.clientmodule_test')['Specialization']
    @py_assert2 = 'instance_attrs_type'
    @py_assert4 = hasattr(klass, @py_assert2)
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=57)
    if not @py_assert4:
        @py_format6 = 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py1)s, %(py3)s)\n}' % {'py0':@pytest_ar._saferepr(hasattr) if 'hasattr' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hasattr) else 'hasattr',  'py1':@pytest_ar._saferepr(klass) if 'klass' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(klass) else 'klass',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert2 = @py_assert4 = None
    type_dict = klass.instance_attrs_type
    @py_assert2 = len(type_dict)
    @py_assert5 = 2
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=59)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(type_dict) if 'type_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(type_dict) else 'type_dict',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert2 = @py_assert4 = @py_assert5 = None
    keys = sorted(type_dict.keys())
    @py_assert2 = ['_id', 'relation']
    @py_assert1 = keys == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=61)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (keys, @py_assert2)) % {'py0':@pytest_ar._saferepr(keys) if 'keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(keys) else 'keys',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None
    @py_assert1 = type_dict['relation'][0]
    @py_assert4 = bases.Instance
    @py_assert6 = isinstance(@py_assert1, @py_assert4)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=62)
    if not @py_assert6:
        @py_format8 = (@pytest_ar._format_assertmsg(type_dict['relation']) + '\n>assert %(py7)s\n{%(py7)s = %(py0)s(%(py2)s, %(py5)s\n{%(py5)s = %(py3)s.Instance\n})\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(bases) if 'bases' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(bases) else 'bases',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert4 = @py_assert6 = None
    @py_assert0 = type_dict['relation'][0]
    @py_assert2 = @py_assert0.name
    @py_assert5 = 'DoNothing'
    @py_assert4 = @py_assert2 == @py_assert5
    if @py_assert4 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=63)
    if not @py_assert4:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py1)s.name\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert5 = None
    @py_assert0 = type_dict['_id'][0]
    @py_assert4 = astroid.Uninferable
    @py_assert2 = @py_assert0 is @py_assert4
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=64)
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('is', ), (@py_assert2,), ('%(py1)s is %(py5)s\n{%(py5)s = %(py3)s.Uninferable\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(astroid) if 'astroid' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(astroid) else 'astroid',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None


def test_concat_interfaces():
    cls = astroid.extract_node('\n        class IMachin: pass\n\n        class Correct2:\n            """docstring"""\n            __implements__ = (IMachin,)\n\n        class BadArgument:\n            """docstring"""\n            __implements__ = (IMachin,)\n\n        class InterfaceCanNowBeFound: #@\n            """docstring"""\n            __implements__ = BadArgument.__implements__ + Correct2.__implements__\n    ')
    interfaces = inspector.interfaces(cls)
    @py_assert0 = [i.name for i in interfaces]
    @py_assert3 = [
     'IMachin']
    @py_assert2 = @py_assert0 == @py_assert3
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=86)
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_interfaces():
    module = astroid.parse('\n    class Interface(object): pass\n    class MyIFace(Interface): pass\n    class AnotherIFace(Interface): pass\n    class Concrete0(object):\n        __implements__ = MyIFace\n    class Concrete1:\n        __implements__ = (MyIFace, AnotherIFace)\n    class Concrete2:\n        __implements__ = (MyIFace, AnotherIFace)\n    class Concrete23(Concrete1): pass\n    ')
    for klass, interfaces in (
     (
      'Concrete0', ['MyIFace']),
     (
      'Concrete1', ['MyIFace', 'AnotherIFace']),
     (
      'Concrete2', ['MyIFace', 'AnotherIFace']),
     (
      'Concrete23', ['MyIFace', 'AnotherIFace'])):
        klass = module[klass]
        @py_assert0 = [i.name for i in inspector.interfaces(klass)]
        @py_assert2 = @py_assert0 == interfaces
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=112)
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py3)s', ), (@py_assert0, interfaces)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(interfaces) if 'interfaces' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(interfaces) else 'interfaces'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None


def test_from_directory(project):
    expected = os.path.join('pylint', 'test', 'data', '__init__.py')
    @py_assert1 = project.name
    @py_assert4 = 'data'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=117)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.name\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(project) if 'project' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(project) else 'project',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert1 = project.path
    @py_assert3 = @py_assert1.endswith
    @py_assert6 = @py_assert3(expected)
    if @py_assert6 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=118)
    if not @py_assert6:
        @py_format8 = 'assert %(py7)s\n{%(py7)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.path\n}.endswith\n}(%(py5)s)\n}' % {'py0':@pytest_ar._saferepr(project) if 'project' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(project) else 'project',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py5':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected',  'py7':@pytest_ar._saferepr(@py_assert6)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert6 = None


def test_project_node(project):
    expected = [
     'data', 'data.clientmodule_test', 'data.suppliermodule_test']
    @py_assert2 = project.keys
    @py_assert4 = @py_assert2()
    @py_assert6 = sorted(@py_assert4)
    @py_assert8 = @py_assert6 == expected
    if @py_assert8 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_inspector.py', lineno=123)
    if not @py_assert8:
        @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py9)s', ), (@py_assert6, expected)) % {'py0':@pytest_ar._saferepr(sorted) if 'sorted' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(sorted) else 'sorted',  'py1':@pytest_ar._saferepr(project) if 'project' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(project) else 'project',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None