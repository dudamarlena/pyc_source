# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_exit.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 1608 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from pathlib import Path
import pytest
from astrality.module import ModuleManager

@pytest.yield_fixture
def test_target(tmpdir):
    test_target = Path(tmpdir) / 'test_target.temp'
    yield test_target
    if test_target.is_file():
        os.remove(test_target)


@pytest.mark.slow
def test_that_all_exit_actions_are_correctly_performed(test_config_directory, test_target):
    modules = {'car': {'on_startup':{'import_context':{'from_path': 'context/mercedes.yml'}, 
              'compile':{'content':'templates/a_car.template', 
               'target':str(test_target)}}, 
             'on_exit':{'import_context':{'from_path': 'context/tesla.yml'}, 
              'compile':{'content':'templates/a_car.template', 
               'target':str(test_target)}}}}
    module_manager = ModuleManager(modules=modules)
    @py_assert1 = test_target.is_file
    @py_assert3 = @py_assert1()
    @py_assert5 = not @py_assert3
    if not @py_assert5:
        @py_format6 = ('' + 'assert not %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.is_file\n}()\n}') % {'py0':@pytest_ar._saferepr(test_target) if 'test_target' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(test_target) else 'test_target',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert3 = @py_assert5 = None
    module_manager.finish_tasks()
    with open(test_target) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = 'My car is a Mercedes'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    module_manager.exit()
    with open(test_target) as (file):
        @py_assert1 = file.read
        @py_assert3 = @py_assert1()
        @py_assert6 = 'My car is a Tesla'
        @py_assert5 = @py_assert3 == @py_assert6
        if not @py_assert5:
            @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.read\n}()\n} == %(py7)s', ), (@py_assert3, @py_assert6)) % {'py0':@pytest_ar._saferepr(file) if 'file' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(file) else 'file',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py7':@pytest_ar._saferepr(@py_assert6)}
            @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None