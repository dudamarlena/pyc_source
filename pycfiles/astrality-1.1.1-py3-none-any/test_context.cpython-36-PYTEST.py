# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/test_context.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 8214 bytes
"""Tests for Context class."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from math import inf
from pathlib import Path
import shutil, pytest
from astrality.context import Context

class TestContextClass:

    def test_initialization_of_config_class_with_no_config_parser(self):
        Context()

    def test_invocation_of_class_with_application_config(self, conf):
        Context(conf)

    def test_initialization_of_config_class_with_dict(self):
        conf_dict = {'key1':'value1', 
         'key2':'value2', 
         'key3':('one', 'two', 'three'), 
         'key4':{'key4-1':'uno', 
          'key4-2':'dos'}}
        config = Context(conf_dict)
        @py_assert1 = config == conf_dict
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (config, conf_dict)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(conf_dict) if 'conf_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf_dict) else 'conf_dict'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_values_for_max_key_property(self):
        config = Context()
        @py_assert1 = config._max_key
        @py_assert5 = -inf
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._max_key\n} == -%(py4)s', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(inf) if 'inf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inf) else 'inf'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        config['string_key'] = 1
        @py_assert1 = config._max_key
        @py_assert5 = -inf
        @py_assert3 = @py_assert1 == @py_assert5
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._max_key\n} == -%(py4)s', ), (@py_assert1, @py_assert5)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(inf) if 'inf' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(inf) else 'inf'}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert5 = None
        config[2] = 'string_value'
        @py_assert1 = config._max_key
        @py_assert4 = 2
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._max_key\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        config[1] = 'string_value'
        @py_assert1 = config._max_key
        @py_assert4 = 2
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._max_key\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        config[3] = 'string_value'
        @py_assert1 = config._max_key
        @py_assert4 = 3
        @py_assert3 = @py_assert1 == @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s._max_key\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
            @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None

    def test_getting_item_from_empty_config(self):
        config = Context()
        with pytest.raises(KeyError):
            config['empty_config_with_no_key']

    def test_accessing_existing_key(self):
        config = Context()
        config['some_key'] = 'some_value'
        @py_assert0 = config['some_key']
        @py_assert3 = 'some_value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        config[-2] = 'some_other_value'
        @py_assert0 = config[(-2)]
        @py_assert3 = 'some_other_value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_integer_index_resolution(self):
        config = Context()
        config['some_key'] = 'some_value'
        config[1] = 'FureCode Nerd Font'
        @py_assert0 = config[2]
        @py_assert3 = 'FureCode Nerd Font'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_integer_index_resolution_without_earlier_index_key(self):
        config = Context()
        config['some_key'] = 'some_value'
        with pytest.raises(KeyError) as (exception):
            config[2]
        @py_assert0 = exception.value.args[0]
        @py_assert3 = 'Integer index "2" is non-existent and had no lower index to be substituted for'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_index_resolution_with_string_key(self):
        config = Context()
        config[2] = 'some_value'
        with pytest.raises(KeyError) as (exception):
            config['test']
        @py_assert0 = exception.value.args[0]
        @py_assert3 = 'test'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_use_of_recursive_config_objects_created_by_dicts(self):
        conf_dict = {'key1':'value1', 
         1:'value2', 
         2:{1: 'some_value'}, 
         'key3':('one', 'two', 'three'), 
         'key4':{1:'uno', 
          'key4-2':'dos'}}
        config = Context(conf_dict)
        @py_assert1 = config == conf_dict
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (config, conf_dict)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(conf_dict) if 'conf_dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(conf_dict) else 'conf_dict'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None
        @py_assert0 = config[3][2]
        @py_assert3 = 'some_value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = config[2]
        @py_assert3 = {1: 'some_value'}
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = config[3]
        @py_assert3 = {1: 'some_value'}
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert1 = config['key4']
        @py_assert4 = isinstance(@py_assert1, Context)
        if not @py_assert4:
            @py_format6 = ('' + 'assert %(py5)s\n{%(py5)s = %(py0)s(%(py2)s, %(py3)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(Context) if 'Context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Context) else 'Context',  'py5':@pytest_ar._saferepr(@py_assert4)}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert4 = None
        @py_assert0 = config['key4']
        @py_assert3 = {1:'uno', 
         'key4-2':'dos'}
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = config['key4'][1]
        @py_assert3 = 'uno'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = config['key4'][2]
        @py_assert3 = 'uno'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_getter(self):
        config = Context()
        @py_assert1 = config.get
        @py_assert3 = 'from_empty_config'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = None
        @py_assert7 = @py_assert5 is @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        config['test'] = 'something'
        @py_assert1 = config.get
        @py_assert3 = 'test'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = 'something'
        @py_assert7 = @py_assert5 == @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('==', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get\n}(%(py4)s)\n} == %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = config.get
        @py_assert3 = 'test'
        @py_assert5 = '4'
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert10 = 'something'
        @py_assert9 = @py_assert7 == @py_assert10
        if not @py_assert9:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
        @py_assert1 = config.get
        @py_assert3 = 'non_existent_key'
        @py_assert5 = @py_assert1(@py_assert3)
        @py_assert8 = None
        @py_assert7 = @py_assert5 is @py_assert8
        if not @py_assert7:
            @py_format10 = @pytest_ar._call_reprcompare(('is', ), (@py_assert7,), ('%(py6)s\n{%(py6)s = %(py2)s\n{%(py2)s = %(py0)s.get\n}(%(py4)s)\n} is %(py9)s', ), (@py_assert5, @py_assert8)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py9':@pytest_ar._saferepr(@py_assert8)}
            @py_format12 = 'assert %(py11)s' % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert8 = None
        @py_assert1 = config.get
        @py_assert3 = 'non_existent_key'
        @py_assert5 = '4'
        @py_assert7 = @py_assert1(@py_assert3, @py_assert5)
        @py_assert10 = '4'
        @py_assert9 = @py_assert7 == @py_assert10
        if not @py_assert9:
            @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.get\n}(%(py4)s, %(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
            @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
            raise AssertionError(@pytest_ar._format_explanation(@py_format14))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None

    def test_items(self):
        config = Context()
        config['4'] = 'test'
        config['font'] = 'Comic Sans'
        config['5'] = '8'
        @py_assert2 = config.items
        @py_assert4 = @py_assert2()
        @py_assert6 = list(@py_assert4)
        @py_assert9 = [
         ('4', 'test'), ('font', 'Comic Sans'), ('5', '8')]
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.items\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None

    def test_keys(self):
        config = Context()
        config['4'] = 'test'
        config['font'] = 'Comic Sans'
        config['5'] = '8'
        @py_assert2 = config.keys
        @py_assert4 = @py_assert2()
        @py_assert6 = list(@py_assert4)
        @py_assert9 = [
         '4', 'font', '5']
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.keys\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None

    def test_values(self):
        config = Context()
        config['4'] = 'test'
        config['font'] = 'Comic Sans'
        config['5'] = '8'
        @py_assert2 = config.values
        @py_assert4 = @py_assert2()
        @py_assert6 = list(@py_assert4)
        @py_assert9 = [
         'test', 'Comic Sans', '8']
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py0)s(%(py5)s\n{%(py5)s = %(py3)s\n{%(py3)s = %(py1)s.values\n}()\n})\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(list) if 'list' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(list) else 'list',  'py1':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None

    def test_update(self):
        one_conf_dict = {'key1':'value1', 
         1:'value2', 
         2:{1: 'some_value'}}
        another_conf_dict = {'key3':('one', 'two', 'three'), 
         'key4':{1:'uno', 
          'key4-2':'dos'}}
        merged_conf_dicts = {'key1':'value1', 
         1:'value2', 
         2:{1: 'some_value'}, 
         'key3':('one', 'two', 'three'), 
         'key4':{1:'uno', 
          'key4-2':'dos'}}
        config = Context(one_conf_dict)
        config.update(another_conf_dict)
        @py_assert1 = config == merged_conf_dicts
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (config, merged_conf_dicts)) % {'py0':@pytest_ar._saferepr(config) if 'config' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(config) else 'config',  'py2':@pytest_ar._saferepr(merged_conf_dicts) if 'merged_conf_dicts' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(merged_conf_dicts) else 'merged_conf_dicts'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_context_class(self):
        context = Context()
        context[1] = 'firs_value'
        context[2] = 'second_value'
        context['string_key'] = 'string_value'
        @py_assert0 = context[1]
        @py_assert3 = 'firs_value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = context[2]
        @py_assert3 = 'second_value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = context[3]
        @py_assert3 = 'second_value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
        @py_assert0 = context['string_key']
        @py_assert3 = 'string_value'
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
            @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None

    def test_initializing_context_with_context(self):
        context1 = Context({'key1': 1})
        context2 = Context(context1)
        @py_assert1 = context1 == context2
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (context1, context2)) % {'py0':@pytest_ar._saferepr(context1) if 'context1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context1) else 'context1',  'py2':@pytest_ar._saferepr(context2) if 'context2' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context2) else 'context2'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_updating_context_with_context(self):
        context1 = Context({'key1': 1})
        context2 = Context({'key2': 2})
        context1.update(context2)
        expected_result = Context({'key1':1,  'key2':2})
        @py_assert1 = context1 == expected_result
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (context1, expected_result)) % {'py0':@pytest_ar._saferepr(context1) if 'context1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context1) else 'context1',  'py2':@pytest_ar._saferepr(expected_result) if 'expected_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_result) else 'expected_result'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None

    def test_reverse_updating_context(self):
        """Reverse update should not overwrite existing keys."""
        context1 = Context({'key1':1, 
         'key2':2})
        context2 = Context({'key2':0, 
         'key3':0})
        context1.reverse_update(context2)
        expected_result = Context({'key1':1,  'key2':2,  'key3':0})
        @py_assert1 = context1 == expected_result
        if not @py_assert1:
            @py_format3 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py2)s', ), (context1, expected_result)) % {'py0':@pytest_ar._saferepr(context1) if 'context1' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context1) else 'context1',  'py2':@pytest_ar._saferepr(expected_result) if 'expected_result' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected_result) else 'expected_result'}
            @py_format5 = 'assert %(py4)s' % {'py4': @py_format3}
            raise AssertionError(@pytest_ar._format_explanation(@py_format5))
        @py_assert1 = None


def test_importing_context_from_compiled_yml_file():
    """YAML files should be importable into the context."""
    context = Context({'section1': {'key_one': 'value_one'}})
    @py_assert0 = context['section1']['key_one']
    @py_assert3 = 'value_one'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    test_config_file = Path(__file__).parent / 'test_config' / 'test.yml'
    context.import_context(from_path=test_config_file,
      from_section='section2',
      to_section='new_section')
    @py_assert0 = context['section1']['key_one']
    @py_assert3 = 'value_one'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = context['new_section']['var3']
    @py_assert3 = 'value1'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    context.import_context(from_path=test_config_file,
      from_section='section3',
      to_section='section3')
    @py_assert0 = context['section3']['env_variable']
    @py_assert3 = 'test_value, hello'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    context.import_context(from_path=test_config_file,
      from_section='section1',
      to_section='section1')
    @py_assert0 = context['section1']['var2']
    @py_assert3 = 'value1/value2'
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert0 = 'key_one'
    @py_assert3 = context['section1']
    @py_assert2 = @py_assert0 not in @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('not in', ), (@py_assert2,), ('%(py1)s not in %(py4)s', ), (@py_assert0, @py_assert3)) % {'py1':@pytest_ar._saferepr(@py_assert0),  'py4':@pytest_ar._saferepr(@py_assert3)}
        @py_format7 = 'assert %(py6)s' % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None


def test_instantiating_context_object_with_path():
    """Paths should be read into the context object."""
    test_context = Path(__file__).parent / 'test_config' / 'test.yml'
    context = Context(test_context)
    @py_assert3 = {'section1':{'var1':'value1',  'var2':'value1/value2'},  'section2':{'var3':'value1',  'empty_string_var':''},  'section3':{'env_variable': 'test_value, hello'},  'section4':{1: 'primary_value'}}
    @py_assert5 = Context(@py_assert3)
    @py_assert1 = context == @py_assert5
    if not @py_assert1:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n}', ), (context, @py_assert5)) % {'py0':@pytest_ar._saferepr(context) if 'context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context) else 'context',  'py2':@pytest_ar._saferepr(Context) if 'Context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Context) else 'Context',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None


def test_instantiating_with_directory_path(tmpdir):
    """Path directory should load context.yml."""
    test_context = Path(__file__).parent / 'test_config' / 'test.yml'
    shutil.copy(str(test_context), str(Path(tmpdir, 'context.yml')))
    context = Context(Path(tmpdir))
    @py_assert3 = {'section1':{'var1':'value1',  'var2':'value1/value2'},  'section2':{'var3':'value1',  'empty_string_var':''},  'section3':{'env_variable': 'test_value, hello'},  'section4':{1: 'primary_value'}}
    @py_assert5 = Context(@py_assert3)
    @py_assert1 = context == @py_assert5
    if not @py_assert1:
        @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert1,), ('%(py0)s == %(py6)s\n{%(py6)s = %(py2)s(%(py4)s)\n}', ), (context, @py_assert5)) % {'py0':@pytest_ar._saferepr(context) if 'context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(context) else 'context',  'py2':@pytest_ar._saferepr(Context) if 'Context' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(Context) else 'Context',  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5)}
        @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
        raise AssertionError(@pytest_ar._format_explanation(@py_format9))
    @py_assert1 = @py_assert3 = @py_assert5 = None