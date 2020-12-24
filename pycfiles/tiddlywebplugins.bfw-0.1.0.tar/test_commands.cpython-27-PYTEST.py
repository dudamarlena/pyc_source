# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fnd/Dev/TiddlyWeb/bfw/test/test_commands.py
# Compiled at: 2014-01-18 04:42:10
import __builtin__ as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, os
from pytest import raises
from tiddlyweb.manage import handle
from . import make_instance, StreamCapture

def setup_module(module):
    instance = make_instance()
    module.TMPDIR = instance['tmpdir']


def test_assetcopy():
    target_dir = os.path.join(TMPDIR, 'static_assets')
    with StreamCapture('stderr') as (stream):
        with raises(SystemExit):
            handle(['', 'assetcopy'])
        handle(['', 'assetcopy', target_dir])
        entries = os.listdir(target_dir)
        @py_assert0 = 'favicon.ico'
        @py_assert2 = @py_assert0 in entries
        if not @py_assert2:
            @py_format4 = @pytest_ar._call_reprcompare(('in', ), (@py_assert2,), ('%(py1)s in %(py3)s', ), (@py_assert0, entries)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py3': @pytest_ar._saferepr(entries) if 'entries' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(entries) else 'entries'}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert0 = @py_assert2 = None
        with raises(SystemExit):
            handle(['', 'assetcopy', target_dir])
    return