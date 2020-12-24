# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 6339 bytes
"""
unit test for the extensions.diadefslib modules
"""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid, pytest
from pylint.pyreverse.diadefslib import *
from pylint.pyreverse.inspector import Linker
from unittest_pyreverse_writer import Config, get_project

def _process_classes(classes):
    """extract class names of a list"""
    return sorted([(isinstance(c.node, astroid.ClassDef), c.title) for c in classes])


def _process_relations(relations):
    """extract relation indices from a relation list"""
    result = []
    for rel_type, rels in relations.items():
        for rel in rels:
            result.append((rel_type, rel.from_object.title, rel.to_object.title))

    result.sort()
    return result


@pytest.fixture
def HANDLER():
    return DiadefsHandler(Config())


@pytest.fixture(scope='module')
def PROJECT():
    return get_project('data')


def test_option_values(HANDLER, PROJECT):
    """test for ancestor, associated and module options"""
    df_h = DiaDefGenerator(Linker(PROJECT), HANDLER)
    cl_config = Config()
    cl_config.classes = ['Specialization']
    cl_h = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(cl_config))
    @py_assert0 = (0, 0)
    @py_assert4 = df_h._get_levels
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 == @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=55)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s._get_levels\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(df_h) if 'df_h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(df_h) else 'df_h',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = False
    @py_assert4 = df_h.module_names
    @py_assert2 = @py_assert0 == @py_assert4
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=56)
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.module_names\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(df_h) if 'df_h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(df_h) else 'df_h',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = (-1, -1)
    @py_assert4 = cl_h._get_levels
    @py_assert6 = @py_assert4()
    @py_assert2 = @py_assert0 == @py_assert6
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=57)
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s._get_levels\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(cl_h) if 'cl_h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cl_h) else 'cl_h',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = True
    @py_assert4 = cl_h.module_names
    @py_assert2 = @py_assert0 == @py_assert4
    if @py_assert2 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=58)
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.module_names\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(cl_h) if 'cl_h' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cl_h) else 'cl_h',  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    for hndl in [df_h, cl_h]:
        hndl.config.all_ancestors = True
        hndl.config.all_associated = True
        hndl.config.module_names = True
        hndl._set_default_options()
        @py_assert0 = (-1, -1)
        @py_assert4 = hndl._get_levels
        @py_assert6 = @py_assert4()
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=64)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s._get_levels\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(hndl) if 'hndl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hndl) else 'hndl',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = True
        @py_assert4 = hndl.module_names
        @py_assert2 = @py_assert0 == @py_assert4
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=65)
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.module_names\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(hndl) if 'hndl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hndl) else 'hndl',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None

    handler = DiadefsHandler(Config())
    df_h = DiaDefGenerator(Linker(PROJECT), handler)
    cl_config = Config()
    cl_config.classes = ['Specialization']
    cl_h = DiaDefGenerator(Linker(PROJECT), DiadefsHandler(cl_config))
    for hndl in [df_h, cl_h]:
        hndl.config.show_ancestors = 2
        hndl.config.show_associated = 1
        hndl.config.module_names = False
        hndl._set_default_options()
        @py_assert0 = (2, 1)
        @py_assert4 = hndl._get_levels
        @py_assert6 = @py_assert4()
        @py_assert2 = @py_assert0 == @py_assert6
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=76)
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s._get_levels\n}()\n}', ), (@py_assert0, @py_assert6)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(hndl) if 'hndl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hndl) else 'hndl',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = False
        @py_assert4 = hndl.module_names
        @py_assert2 = @py_assert0 == @py_assert4
        if @py_assert2 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=77)
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.module_names\n}', ), (@py_assert0, @py_assert4)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py3':@pytest_ar._saferepr(hndl) if 'hndl' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(hndl) else 'hndl',  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None


class TestDefaultDiadefGenerator(object):

    def test_known_values1(self, HANDLER, PROJECT):
        dd = DefaultDiadefGenerator(Linker(PROJECT), HANDLER).visit(PROJECT)
        @py_assert2 = len(dd)
        @py_assert5 = 2
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=88)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(dd) if 'dd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dd) else 'dd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        keys = [d.TYPE for d in dd]
        @py_assert2 = ['package', 'class']
        @py_assert1 = keys == @py_assert2
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=90)
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (keys, @py_assert2)) % {'py0':@pytest_ar._saferepr(keys) if 'keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(keys) else 'keys',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        pd = dd[0]
        @py_assert1 = pd.title
        @py_assert4 = 'packages No Name'
        @py_assert3 = @py_assert1 == @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=92)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(pd) if 'pd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(pd) else 'pd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        modules = sorted([(isinstance(m.node, astroid.Module), m.title) for m in pd.objects])
        @py_assert2 = [
         (True, 'data'), (True, 'data.clientmodule_test'), (True, 'data.suppliermodule_test')]
        @py_assert1 = modules == @py_assert2
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=96)
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (modules, @py_assert2)) % {'py0':@pytest_ar._saferepr(modules) if 'modules' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(modules) else 'modules',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        cd = dd[1]
        @py_assert1 = cd.title
        @py_assert4 = 'classes No Name'
        @py_assert3 = @py_assert1 == @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=102)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(cd) if 'cd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cd) else 'cd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        classes = _process_classes(cd.objects)
        @py_assert2 = [(True, 'Ancestor'), (True, 'DoNothing'), (True, 'Interface'), (True, 'Specialization')]
        @py_assert1 = classes == @py_assert2
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=104)
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (classes, @py_assert2)) % {'py0':@pytest_ar._saferepr(classes) if 'classes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(classes) else 'classes',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None

    _should_rels = [
     ('association', 'DoNothing', 'Ancestor'),
     ('association', 'DoNothing', 'Specialization'),
     ('implements', 'Ancestor', 'Interface'),
     ('specialization', 'Specialization', 'Ancestor')]

    def test_exctract_relations(self, HANDLER, PROJECT):
        """test extract_relations between classes"""
        cd = DefaultDiadefGenerator(Linker(PROJECT), HANDLER).visit(PROJECT)[1]
        cd.extract_relationships()
        relations = _process_relations(cd.relationships)
        @py_assert3 = self._should_rels
        @py_assert1 = relations == @py_assert3
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=123)
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s._should_rels\n}', ), (relations, @py_assert3)) % {'py0':@pytest_ar._saferepr(relations) if 'relations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(relations) else 'relations',  'py2':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None

    def test_functional_relation_extraction(self):
        """functional test of relations extraction;
        different classes possibly in different modules"""
        project = get_project('data')
        handler = DiadefsHandler(Config())
        diadefs = handler.get_diadefs(project, Linker(project, tag=True))
        cd = diadefs[1]
        relations = _process_relations(cd.relationships)
        @py_assert3 = self._should_rels
        @py_assert1 = relations == @py_assert3
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=135)
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s._should_rels\n}', ), (relations, @py_assert3)) % {'py0':@pytest_ar._saferepr(relations) if 'relations' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(relations) else 'relations',  'py2':@pytest_ar._saferepr(self) if 'self' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(self) else 'self',  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None

    def test_known_values2(self, HANDLER):
        project = get_project('data.clientmodule_test')
        dd = DefaultDiadefGenerator(Linker(project), HANDLER).visit(project)
        @py_assert2 = len(dd)
        @py_assert5 = 1
        @py_assert4 = @py_assert2 == @py_assert5
        if @py_assert4 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=140)
        if not @py_assert4:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert4,), ('%(py3)s\n{%(py3)s = %(py0)s(%(py1)s)\n} == %(py6)s', ), (@py_assert2, @py_assert5)) % {'py0':@pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len',  'py1':@pytest_ar._saferepr(dd) if 'dd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dd) else 'dd',  'py3':@pytest_ar._saferepr(@py_assert2),  'py6':@pytest_ar._saferepr(@py_assert5)}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert2 = @py_assert4 = @py_assert5 = None
        keys = [d.TYPE for d in dd]
        @py_assert2 = ['class']
        @py_assert1 = keys == @py_assert2
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=142)
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (keys, @py_assert2)) % {'py0':@pytest_ar._saferepr(keys) if 'keys' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(keys) else 'keys',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
        cd = dd[0]
        @py_assert1 = cd.title
        @py_assert4 = 'classes No Name'
        @py_assert3 = @py_assert1 == @py_assert4
        if @py_assert3 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=144)
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(cd) if 'cd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cd) else 'cd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        classes = _process_classes(cd.objects)
        @py_assert2 = [(True, 'Ancestor'), (True, 'Specialization')]
        @py_assert1 = classes == @py_assert2
        if @py_assert1 is None:
            from _pytest.warning_types import PytestWarning
            from warnings import warn_explicit
            warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=146)
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (classes, @py_assert2)) % {'py0':@pytest_ar._saferepr(classes) if 'classes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(classes) else 'classes',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None


def test_known_values1(HANDLER, PROJECT):
    HANDLER.config.classes = [
     'Specialization']
    cdg = ClassDiadefGenerator(Linker(PROJECT), HANDLER)
    special = 'data.clientmodule_test.Specialization'
    cd = cdg.class_diagram(PROJECT, special)
    @py_assert1 = cd.title
    @py_assert3 = @py_assert1 == special
    if @py_assert3 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=154)
    if not @py_assert3:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py4)s', ), (@py_assert1, special)) % {'py0':@pytest_ar._saferepr(cd) if 'cd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cd) else 'cd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(special) if 'special' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(special) else 'special'}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    classes = _process_classes(cd.objects)
    @py_assert2 = [(True, 'data.clientmodule_test.Ancestor'), (True, special), (True, 'data.suppliermodule_test.DoNothing')]
    @py_assert1 = classes == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=156)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (classes, @py_assert2)) % {'py0':@pytest_ar._saferepr(classes) if 'classes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(classes) else 'classes',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_known_values2(HANDLER, PROJECT):
    HANDLER.config.classes = [
     'Specialization']
    HANDLER.config.module_names = False
    cd = ClassDiadefGenerator(Linker(PROJECT), HANDLER).class_diagram(PROJECT, 'data.clientmodule_test.Specialization')
    @py_assert1 = cd.title
    @py_assert4 = 'data.clientmodule_test.Specialization'
    @py_assert3 = @py_assert1 == @py_assert4
    if @py_assert3 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=169)
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.title\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(cd) if 'cd' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(cd) else 'cd',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    classes = _process_classes(cd.objects)
    @py_assert2 = [(True, 'Ancestor'), (True, 'DoNothing'), (True, 'Specialization')]
    @py_assert1 = classes == @py_assert2
    if @py_assert1 is None:
        from _pytest.warning_types import PytestWarning
        from warnings import warn_explicit
        warn_explicit((PytestWarning('asserting the value None, please use "assert is None"')), category=None, filename='/home/moser/code/pylint/pylint/test/unittest_pyreverse_diadefs.py', lineno=171)
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (classes, @py_assert2)) % {'py0':@pytest_ar._saferepr(classes) if 'classes' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(classes) else 'classes',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None