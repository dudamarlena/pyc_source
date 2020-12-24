# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/cosmin/workspace/github/cleanmymac/build/lib/cleanmymac/test/test_schema.py
# Compiled at: 2016-02-14 16:40:25
# Size of source mod 2**32: 2481 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest
from voluptuous import MultipleInvalid
from yaml import load
from cleanmymac.schema import _cmd_spec_schema, _dir_spec_schema

def test_cmd_spec_schema():
    spec = "\nupdate_commands: [\n    'cmd1',\n    'cmd1'\n]\nclean_commands: [\n    'cmd3'\n]\n        ".strip()
    obj_spec = load(spec)
    validated_spec = _cmd_spec_schema(strict=False)(obj_spec)
    @py_assert0 = 'update_commands'
    @py_assert2 = @py_assert0 in validated_spec
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, validated_spec)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(validated_spec) if 'validated_spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validated_spec) else 'validated_spec'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'clean_commands'
    @py_assert2 = @py_assert0 in validated_spec
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, validated_spec)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(validated_spec) if 'validated_spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validated_spec) else 'validated_spec'}
        @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert1 = validated_spec['update_commands']
    @py_assert3 = set(@py_assert1)
    @py_assert7 = obj_spec['update_commands']
    @py_assert9 = set(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    @py_assert1 = validated_spec['clean_commands']
    @py_assert3 = set(@py_assert1)
    @py_assert7 = obj_spec['clean_commands']
    @py_assert9 = set(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}', ), (@py_assert3, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set'}
        @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    obj_spec['extra_key'] = [
     'val1', 'val2']
    with pytest.raises(MultipleInvalid):
        _cmd_spec_schema(strict=False)(obj_spec)
    del obj_spec['extra_key']


def test_dir_spec_schema():
    spec = "\nupdate_message: 'a message'\nentries: [\n    {\n        dir: '~',\n        pattern: '\\d+'\n    },\n]\n        ".strip()
    obj_spec = load(spec)
    validated_spec = _dir_spec_schema(strict=False)(obj_spec)
    @py_assert0 = 'update_message'
    @py_assert2 = @py_assert0 in validated_spec
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, validated_spec)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(validated_spec) if 'validated_spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validated_spec) else 'validated_spec'}
        @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = 'entries'
    @py_assert2 = @py_assert0 in validated_spec
    if not @py_assert2:
        @py_format4 = @pytest_ar._call_reprcompare(('in',), (@py_assert2,), ('%(py1)s in %(py3)s',), (@py_assert0, validated_spec)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(validated_spec) if 'validated_spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(validated_spec) else 'validated_spec'}
        @py_format6 = ('' + 'assert %(py5)s') % {'py5': @py_format4}
        raise AssertionError(@pytest_ar._format_explanation(@py_format6))
    @py_assert0 = @py_assert2 = None
    @py_assert0 = validated_spec['update_message']
    @py_assert3 = obj_spec['update_message']
    @py_assert2 = @py_assert0 == @py_assert3
    if not @py_assert2:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = validated_spec['entries']
    @py_assert3 = len(@py_assert1)
    @py_assert7 = obj_spec['entries']
    @py_assert9 = len(@py_assert7)
    @py_assert5 = @py_assert3 == @py_assert9
    if not @py_assert5:
        @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py10)s\n{%(py10)s = %(py6)s(%(py8)s)\n}',), (@py_assert3, @py_assert9)) % {'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py2': @pytest_ar._saferepr(@py_assert1), 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len'}
        @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
        raise AssertionError(@pytest_ar._format_explanation(@py_format13))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
    obj_spec['extra_key'] = [
     'val1', 'val2']
    with pytest.raises(MultipleInvalid):
        _dir_spec_schema(strict=False)(obj_spec)
    del obj_spec['extra_key']
    @py_assert2 = True
    @py_assert4 = _dir_spec_schema(strict=@py_assert2)
    @py_assert7 = @py_assert4(obj_spec)
    @py_assert10 = isinstance(@py_assert7, dict)
    if not @py_assert10:
        @py_format12 = ('' + 'assert %(py11)s\n{%(py11)s = %(py0)s(%(py8)s\n{%(py8)s = %(py5)s\n{%(py5)s = %(py1)s(strict=%(py3)s)\n}(%(py6)s)\n}, %(py9)s)\n}') % {'py1': @pytest_ar._saferepr(_dir_spec_schema) if '_dir_spec_schema' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(_dir_spec_schema) else '_dir_spec_schema', 'py11': @pytest_ar._saferepr(@py_assert10), 'py9': @pytest_ar._saferepr(dict) if 'dict' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(dict) else 'dict', 'py8': @pytest_ar._saferepr(@py_assert7), 'py0': @pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance', 'py5': @pytest_ar._saferepr(@py_assert4), 'py3': @pytest_ar._saferepr(@py_assert2), 'py6': @pytest_ar._saferepr(obj_spec) if 'obj_spec' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(obj_spec) else 'obj_spec'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert2 = @py_assert4 = @py_assert7 = @py_assert10 = None
    spec = "\nupdate_message: 'a message'\nentries: [\n    {\n        dir: '/____folder/_that/_does/_not/_exist/',\n        pattern: '\\d+'\n    },\n]\n        ".strip()
    obj_spec = load(spec)
    with pytest.raises(MultipleInvalid):
        _dir_spec_schema(strict=True)(obj_spec)