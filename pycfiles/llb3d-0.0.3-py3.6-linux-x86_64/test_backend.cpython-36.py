# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/tests/test_backend.py
# Compiled at: 2019-01-14 10:01:56
# Size of source mod 2**32: 1938 bytes
"""Test case for backend."""
import subprocess
from llvmlite import ir, binding
from ..backend import Backend
from .. import backend as backend_module

def test_types():
    """Check that we have types."""
    if not isinstance(backend_module.UCHAR_T, ir.IntType):
        raise AssertionError
    else:
        if not isinstance(backend_module.USTR_T, ir.PointerType):
            raise AssertionError
        else:
            if not isinstance(backend_module.INT32_T, ir.IntType):
                raise AssertionError
            else:
                assert isinstance(backend_module.FLOAT32_T, ir.FloatType)
                assert isinstance(backend_module.VOID_T, ir.VoidType)
            assert isinstance(backend_module.BBMAIN_SIGNATURE, ir.FunctionType)
        assert isinstance(backend_module.INT32_ZERO, ir.Constant)


def test_init_backend():
    """Check that after init builder and runtime is available."""
    backend = Backend()
    if not isinstance(backend.source_module, ir.Module):
        raise AssertionError
    else:
        assert isinstance(backend.runtime, dict)
        assert isinstance(backend.builder, ir.IRBuilder)


def test_optimize():
    """Check that optimize return llvm module."""
    backend = Backend()
    assert isinstance(backend.optimize(), binding.ModuleRef)


def test_emit_llvm():
    """Check that emit_llvm return valid llvm."""
    backend = Backend()
    assert 'bbmain' in backend.emit_llvm()


def test_emit_assembly():
    """Check that in assembler remains bbmain."""
    backend = Backend()
    asm = backend.emit_assembly()
    assert 'bbmain' in asm


def test_run():
    """Check that we can run llvm program."""
    backend = Backend()
    run = backend.run()
    if not isinstance(run, subprocess.CompletedProcess):
        raise AssertionError
    else:
        assert run.stdout is None
        run = backend.run(stdout=(subprocess.PIPE), encoding='utf-8')
        assert run.stdout == ''


def test_emit_executable(tmpdir):
    """Check that we can create empty executable."""
    backend = Backend()
    output = tmpdir.join('output')
    backend.emit_executable(output)
    output.check(file=1, exists=1)
    assert output.sysexec() == ''