# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/works/github/depthwise-conv-pytorch/test/test_forward.py
# Compiled at: 2020-02-20 04:47:49
# Size of source mod 2**32: 1944 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, torch
from torch.nn import functional as F
from torch_dwconv import depthwise_conv2d
BATCH_SIZE = 32

def get_diff(N, C, H, W, kernel_size, stride, padding):
    x = torch.randn(N, C, H, W).to('cuda')
    k = torch.randn(C, 1, kernel_size, kernel_size).to('cuda')
    native = F.conv2d(x, k, stride=stride, padding=padding, groups=C)
    custom = depthwise_conv2d(x, k, stride=stride, padding=padding)
    return (native - custom).abs().max().item()


def test_forward_large_size():
    @py_assert2 = 32
    @py_assert4 = 64
    @py_assert6 = 64
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=21)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_large_kernel():
    @py_assert2 = 32
    @py_assert4 = 64
    @py_assert6 = 64
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=25)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_stride():
    @py_assert2 = 32
    @py_assert4 = 64
    @py_assert6 = 64
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 1
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=29)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_large_kernel_stride():
    @py_assert2 = 32
    @py_assert4 = 64
    @py_assert6 = 64
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 2
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=33)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_no_pad():
    @py_assert2 = 32
    @py_assert4 = 64
    @py_assert6 = 64
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 0
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=37)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_large_kernel_no_pad():
    @py_assert2 = 32
    @py_assert4 = 64
    @py_assert6 = 64
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 0
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=41)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_stride_no_pad():
    @py_assert2 = 32
    @py_assert4 = 64
    @py_assert6 = 64
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 0
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=45)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_large_kernel_stride_no_pad():
    @py_assert2 = 32
    @py_assert4 = 64
    @py_assert6 = 64
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 0
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=49)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_odd():
    @py_assert2 = 32
    @py_assert4 = 63
    @py_assert6 = 65
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=53)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_odd_large_kernel():
    @py_assert2 = 32
    @py_assert4 = 63
    @py_assert6 = 65
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=57)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_odd_stride():
    @py_assert2 = 32
    @py_assert4 = 63
    @py_assert6 = 65
    @py_assert8 = 3
    @py_assert10 = 2
    @py_assert12 = 1
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=61)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_large_size_odd_large_kernel_stride():
    @py_assert2 = 32
    @py_assert4 = 63
    @py_assert6 = 65
    @py_assert8 = 5
    @py_assert10 = 2
    @py_assert12 = 2
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=65)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_small_size():
    @py_assert2 = 128
    @py_assert4 = 32
    @py_assert6 = 32
    @py_assert8 = 3
    @py_assert10 = 1
    @py_assert12 = 1
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=69)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None


def test_forward_small_size_large_kernel():
    @py_assert2 = 128
    @py_assert4 = 32
    @py_assert6 = 32
    @py_assert8 = 5
    @py_assert10 = 1
    @py_assert12 = 2
    @py_assert14 = get_diff(BATCH_SIZE, @py_assert2, @py_assert4, @py_assert6, @py_assert8, @py_assert10, @py_assert12)
    @py_assert17 = 1e-08
    @py_assert16 = @py_assert14 < @py_assert17
    if @py_assert16 is None:
        from _pytest.warning_types import PytestAssertRewriteWarning
        from warnings import warn_explicit
        warn_explicit((PytestAssertRewriteWarning('asserting the value None, please use "assert is None"')), category=None, filename='/root/works/github/depthwise-conv-pytorch/test/test_forward.py', lineno=73)
    if not @py_assert16:
        @py_format19 = @pytest_ar._call_reprcompare(('<', ), (@py_assert16,), ('%(py15)s\n{%(py15)s = %(py0)s(%(py1)s, %(py3)s, %(py5)s, %(py7)s, %(py9)s, %(py11)s, %(py13)s)\n} < %(py18)s', ), (@py_assert14, @py_assert17)) % {'py0':@pytest_ar._saferepr(get_diff) if 'get_diff' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(get_diff) else 'get_diff',  'py1':@pytest_ar._saferepr(BATCH_SIZE) if 'BATCH_SIZE' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(BATCH_SIZE) else 'BATCH_SIZE',  'py3':@pytest_ar._saferepr(@py_assert2),  'py5':@pytest_ar._saferepr(@py_assert4),  'py7':@pytest_ar._saferepr(@py_assert6),  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(@py_assert12),  'py15':@pytest_ar._saferepr(@py_assert14),  'py18':@pytest_ar._saferepr(@py_assert17)}
        @py_format21 = 'assert %(py20)s' % {'py20': @py_format19}
        raise AssertionError(@pytest_ar._format_explanation(@py_format21))
    @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = @py_assert10 = @py_assert12 = @py_assert14 = @py_assert16 = @py_assert17 = None