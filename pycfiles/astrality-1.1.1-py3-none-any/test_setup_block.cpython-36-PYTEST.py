# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/JakobGM/astrality/astrality/tests/module/test_setup_block.py
# Compiled at: 2018-11-27 12:34:29
# Size of source mod 2**32: 972 bytes
"""Tests for setup block in module."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pathlib import Path
from astrality.actions import SetupActionBlock
from astrality.module import Module

def test_that_module_block_is_persisted():
    """Module should create a 'setup' action block."""
    module_config = {'on_setup': {'run': {'shell': 'echo first time!'}}}
    params = {'name':'test', 
     'module_config':module_config, 
     'module_directory':Path(__file__).parent}
    module = Module(**params)
    @py_assert2 = module.get_action_block
    @py_assert4 = 'on_setup'
    @py_assert6 = @py_assert2(name=@py_assert4)
    @py_assert9 = isinstance(@py_assert6, SetupActionBlock)
    if not @py_assert9:
        @py_format11 = ('' + 'assert %(py10)s\n{%(py10)s = %(py0)s(%(py7)s\n{%(py7)s = %(py3)s\n{%(py3)s = %(py1)s.get_action_block\n}(name=%(py5)s)\n}, %(py8)s)\n}') % {'py0':@pytest_ar._saferepr(isinstance) if 'isinstance' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(isinstance) else 'isinstance',  'py1':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py8':@pytest_ar._saferepr(SetupActionBlock) if 'SetupActionBlock' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(SetupActionBlock) else 'SetupActionBlock',  'py10':@pytest_ar._saferepr(@py_assert9)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert9 = None
    @py_assert1 = module.execute
    @py_assert3 = 'run'
    @py_assert5 = 'on_setup'
    @py_assert7 = @py_assert1(action=@py_assert3, block=@py_assert5)
    @py_assert10 = (('echo first time!', 'first time!'), )
    @py_assert9 = @py_assert7 == @py_assert10
    if not @py_assert9:
        @py_format12 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.execute\n}(action=%(py4)s, block=%(py6)s)\n} == %(py11)s', ), (@py_assert7, @py_assert10)) % {'py0':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py11':@pytest_ar._saferepr(@py_assert10)}
        @py_format14 = 'assert %(py13)s' % {'py13': @py_format12}
        raise AssertionError(@pytest_ar._format_explanation(@py_format14))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert10 = None
    del module
    module = Module(**params)
    @py_assert1 = module.execute
    @py_assert3 = 'run'
    @py_assert5 = 'on_setup'
    @py_assert7 = @py_assert1(action=@py_assert3, block=@py_assert5)
    @py_assert11 = tuple()
    @py_assert9 = @py_assert7 == @py_assert11
    if not @py_assert9:
        @py_format13 = @pytest_ar._call_reprcompare(('==', ), (@py_assert9,), ('%(py8)s\n{%(py8)s = %(py2)s\n{%(py2)s = %(py0)s.execute\n}(action=%(py4)s, block=%(py6)s)\n} == %(py12)s\n{%(py12)s = %(py10)s()\n}', ), (@py_assert7, @py_assert11)) % {'py0':@pytest_ar._saferepr(module) if 'module' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(module) else 'module',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py8':@pytest_ar._saferepr(@py_assert7),  'py10':@pytest_ar._saferepr(tuple) if 'tuple' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tuple) else 'tuple',  'py12':@pytest_ar._saferepr(@py_assert11)}
        @py_format15 = 'assert %(py14)s' % {'py14': @py_format13}
        raise AssertionError(@pytest_ar._format_explanation(@py_format15))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = @py_assert11 = None