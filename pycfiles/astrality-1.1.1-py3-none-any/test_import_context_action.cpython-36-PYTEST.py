# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/actions/test_import_context_action.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 4247 bytes
"""Tests for ImportContextAction class."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.actions import ImportContextAction
from astrality.context import Context
from astrality.persistence import CreatedFiles

def test_null_object_pattern():
    """Test initializing action with no behaviour."""
    import_context_action = ImportContextAction(options={}, directory=(Path('/')),
      replacer=(lambda x: x),
      context_store=(Context()),
      creation_store=CreatedFiles().wrapper_for(module='test'))
    import_context_action.execute()


def test_importing_entire_file(context_directory):
    """
    Test importing all sections from context file.

    All context sections should be imported in the absence of `from_section`.
    """
    context_import_dict = {'from_path': 'several_sections.yml'}
    context_store = Context()
    import_context_action = ImportContextAction(options=context_import_dict,
      directory=context_directory,
      replacer=(lambda x: x),
      context_store=context_store,
      creation_store=CreatedFiles().wrapper_for(module='test'))
    import_context_action.execute()
    expected_context = {'section1':{'k1_1':'v1_1', 
      'k1_2':'v1_2'}, 
     'section2':{'k2_1':'v2_1', 
      'k2_2':'v2_2'}}
    @py_assert1 = context_store == expected_context
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (context_store, expected_context)) % {'py0':@pytest_ar._saferepr(context_store) if 'context_store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context_store) else 'context_store',  'py2':@pytest_ar._saferepr(expected_context) if 'expected_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_context) else 'expected_context'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_importing_specific_section(context_directory):
    """Test importing specific sections from context file."""
    context_import_dict = {'from_path':'several_sections.yml', 
     'from_section':'section1'}
    context_store = Context({'original': 'value'})
    import_context_action = ImportContextAction(options=context_import_dict,
      directory=context_directory,
      replacer=(lambda x: x),
      context_store=context_store,
      creation_store=CreatedFiles().wrapper_for(module='test'))
    import_context_action.execute()
    expected_context = Context({'original':'value', 
     'section1':{'k1_1':'v1_1', 
      'k1_2':'v1_2'}})
    @py_assert1 = context_store == expected_context
    if not @py_assert1:
        @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (context_store, expected_context)) % {'py0':@pytest_ar._saferepr(context_store) if 'context_store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context_store) else 'context_store',  'py2':@pytest_ar._saferepr(expected_context) if 'expected_context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_context) else 'expected_context'}
        @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
        raise AssertionError(@pytest_ar._format_explanation(@py_format5))
    @py_assert1 = None


def test_replacer_function_being_used(context_directory):
    """
    Test use of replacement function in option retrieval.

    The function should be used when querying values from `options`.
    """
    context_import_dict = {'from_path':'path', 
     'from_section':'from', 
     'to_section':'to'}
    context_store = Context()

    def replacer(option: str) -> str:
        if option == 'path':
            return 'several_sections.yml'
        else:
            if option == 'from':
                return 'section1'
            if option == 'to':
                return 'new_section'
        raise AssertionError

    import_context_action = ImportContextAction(options=context_import_dict,
      directory=context_directory,
      replacer=replacer,
      context_store=context_store,
      creation_store=CreatedFiles().wrapper_for(module='test'))
    import_context_action.execute()
    @py_assert2 = {'new_section': {'k1_1':'v1_1',  'k1_2':'v1_2'}}
    @py_assert1 = context_store == @py_assert2
    if not @py_assert1:
        @py_format4 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py3)s', ), (context_store, @py_assert2)) % {'py0':@pytest_ar._saferepr(context_store) if 'context_store' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context_store) else 'context_store',  'py3':@pytest_ar._saferepr(@py_assert2)}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert1 = @py_assert2 = None


def test_that_replacer_is_run_every_time(context_directory):
    """
    The replacer should be run a new every time self.execute() is invoked.
    """
    context_import_dict = {'from_path':'several_sections.yml', 
     'from_section':'section1', 
     'to_section':'whatever'}
    context_store = Context()

    class Replacer:

        def __init__(self) -> None:
            self.invoke_number = 0

        def __call__(self, option: str) -> str:
            self.invoke_number += 1
            return option

    replacer = Replacer()
    import_context_action = ImportContextAction(options=context_import_dict,
      directory=context_directory,
      replacer=replacer,
      context_store=context_store,
      creation_store=CreatedFiles().wrapper_for(module='test'))
    import_context_action.execute()
    @py_assert1 = replacer.invoke_number
    @py_assert4 = 3
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.invoke_number\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(replacer) if 'replacer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(replacer) else 'replacer',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    import_context_action.execute()
    @py_assert1 = replacer.invoke_number
    @py_assert4 = 6
    @py_assert3 = @py_assert1 == @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.invoke_number\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(replacer) if 'replacer' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(replacer) else 'replacer',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
        @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None