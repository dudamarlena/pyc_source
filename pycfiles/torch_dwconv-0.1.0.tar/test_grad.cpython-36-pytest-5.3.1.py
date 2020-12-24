# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/works/github/depthwise-conv-pytorch/test/test_grad.py
# Compiled at: 2020-02-20 04:53:35
# Size of source mod 2**32: 4086 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, torch
from torch.autograd import gradcheck
from torch_dwconv import depthwise_conv2d
BATCH_SIZE = 8

def make_tensor(N, C, H, W, kernel_size, input_grad=False, kernel_grad=False):
    x = torch.randn(N, C, H, W).double().to('cuda')
    k = torch.randn(C, 1, kernel_size, kernel_size).double().to('cuda')
    x.requires_grad = input_grad
    k.requires_grad = kernel_grad
    return (
     x, k)


def check_input_grad(N, C, H, W, kernel_size, stride, padding):
    x, k = make_tensor(N, C, H, W, kernel_size, input_grad=True)
    result = gradcheck((lambda x_i: depthwise_conv2d(x_i, k, stride=stride, padding=padding).sum()),
      x,
      raise_exception=False)
    return result


def check_kernel_grad(N, C, H, W, kernel_size, stride, padding):
    x, k = make_tensor(N, C, H, W, kernel_size, kernel_grad=True)
    result = gradcheck((lambda k_i: depthwise_conv2d(x, k_i, stride=stride, padding=padding).sum()),
      k,
      raise_exception=False)
    return result


def test_input_grad_large_size():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=45)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_large_kernel():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=49)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_stride():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 1
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=53)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_large_kernel_stride():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 2
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=57)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_no_pad():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 0
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=61)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_large_kernel_no_pad():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 0
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=65)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_stride_no_pad():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 0
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=69)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_large_kernel_stride_no_pad():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 0
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=73)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_odd():
    @py_assert2 = 8
    @py_assert4 = 33
    @py_assert6 = 35
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=77)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_odd_large_kernel():
    @py_assert2 = 8
    @py_assert4 = 33
    @py_assert6 = 35
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=81)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_odd_stride():
    @py_assert2 = 8
    @py_assert4 = 33
    @py_assert6 = 35
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 1
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=85)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_large_size_odd_large_kernel_stride():
    @py_assert2 = 8
    @py_assert4 = 33
    @py_assert6 = 35
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 2
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=89)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=93)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_large_kernel():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=97)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_stride():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 1
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=101)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_large_kernel_stride():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 2
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=105)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_no_pad():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 0
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=109)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_large_kernel_no_pad():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 0
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=113)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_stride_no_pad():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 0
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=117)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_large_kernel_stride_no_pad():
    @py_assert2 = 8
    @py_assert4 = 34
    @py_assert6 = 34
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 0
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=121)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_odd():
    @py_assert2 = 8
    @py_assert4 = 33
    @py_assert6 = 35
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=125)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_odd_large_kernel():
    @py_assert2 = 8
    @py_assert4 = 33
    @py_assert6 = 35
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=129)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_odd_stride():
    @py_assert2 = 8
    @py_assert4 = 33
    @py_assert6 = 35
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 1
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=133)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_large_size_odd_large_kernel_stride():
    @py_assert2 = 8
    @py_assert4 = 33
    @py_assert6 = 35
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 2
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=137)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_small_size():
    @py_assert2 = 8
    @py_assert4 = 16
    @py_assert6 = 16
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=141)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_input_grad_small_size_large_kernel():
    @py_assert2 = 8
    @py_assert4 = 16
    @py_assert6 = 16
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = check_input_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=145)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_input_grad) if 'check_input_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_input_grad) else 'check_input_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_small_size():
    @py_assert2 = 8
    @py_assert4 = 16
    @py_assert6 = 16
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=149)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None


def test_kernel_grad_small_size_large_kernel():
    @py_assert2 = 8
    @py_assert4 = 16
    @py_assert6 = 16
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = check_kernel_grad(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    if @py_assert14 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_grad.py', lineno=153)
    if not @py_assert14:
        @py_format16 = 'assert %(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n}' % {'py0':@pytest_ar._saferepr(check_kernel_grad) if 'check_kernel_grad' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(check_kernel_grad) else 'check_kernel_grad',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14)}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = None