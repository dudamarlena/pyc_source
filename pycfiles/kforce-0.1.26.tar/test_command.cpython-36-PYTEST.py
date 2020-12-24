# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kelvin.liu/Code/OSS/kforce/tests/unit/test_command.py
# Compiled at: 2018-02-24 09:50:51
# Size of source mod 2**32: 1199 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from importlib import import_module
from unittest import TestCase
import pytest
from kforce import commands

class TestCommands(TestCase):

    def setUp(self):
        params = dict(env='s', account_name='acc1', vpc_id='vpc-xxxx')
        self.cmd = (commands.Commands)(**params)

    def test_register(self):
        cmds = [
         'new',
         'build',
         'diff',
         'apply',
         'install']
        module = import_module('kforce.commands')
        for c_name in cmds:
            c = getattr(self.cmd, c_name)
            c_raw = getattr(module, c_name.title())
            @py_assert1 = c.__name__
            @py_assert4 = '_run'
            @py_assert3 = @py_assert1 == @py_assert4
            if not @py_assert3:
                @py_format6 = @pytest_ar._call_reprcompare(('==', ), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.__name__\n} == %(py5)s', ), (@py_assert1, @py_assert4)) % {'py0':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py2':@pytest_ar._saferepr(@py_assert1),  'py5':@pytest_ar._saferepr(@py_assert4)}
                @py_format8 = 'assert %(py7)s' % {'py7': @py_format6}
                raise AssertionError(@pytest_ar._format_explanation(@py_format8))
            @py_assert1 = @py_assert3 = @py_assert4 = None
            @py_assert2 = c.__self__
            @py_assert5 = isinstance(@py_assert2, c_raw)
            if not @py_assert5:
                @py_format7 = ('' + 'assert %(py6)s\n{%(py6)s = %(py0)s(%(py3)s\n{%(py3)s = %(py1)s.__self__\n}, %(py4)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(c) if 'c' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c) else 'c',  'py3':@pytest_ar._saferepr(@py_assert2),  'py4':@pytest_ar._saferepr(c_raw) if 'c_raw' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(c_raw) else 'c_raw',  'py6':@pytest_ar._saferepr(@py_assert5)}
                raise AssertionError(@pytest_ar._format_explanation(@py_format7))
            @py_assert2 = @py_assert5 = None


class TestCommand(TestCase):

    def setUp(self):
        params = dict(env='s', account_name='acc1', vpc_id='vpc-xxxx')
        self.c = (commands.Command)(**params)

    def test_env_check(self):
        params = dict(env='this is not a valid env', account_name='acc1', vpc_id='vpc-xxxx')
        with pytest.raises(ValueError):
            (commands.Command)(**params)
        params = dict(env='s', account_name='acc1', vpc_id='vpc-xxxx')
        @py_assert1 = commands.Command
        @py_assert4 = @py_assert1(**params)
        @py_assert6 = @py_assert4.env
        @py_assert9 = 's'
        @py_assert8 = @py_assert6 == @py_assert9
        if not @py_assert8:
            @py_format11 = @pytest_ar._call_reprcompare(('==', ), (@py_assert8,), ('%(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py2)s\n{%(py2)s = %(py0)s.Command\n}(**%(py3)s)\n}.env\n} == %(py10)s', ), (@py_assert6, @py_assert9)) % {'py0':@pytest_ar._saferepr(commands) if 'commands' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(commands) else 'commands',  'py2':@pytest_ar._saferepr(@py_assert1),  'py3':@pytest_ar._saferepr(params) if 'params' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(params) else 'params',  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py10':@pytest_ar._saferepr(@py_assert9)}
            @py_format13 = 'assert %(py12)s' % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert1 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert9 = None