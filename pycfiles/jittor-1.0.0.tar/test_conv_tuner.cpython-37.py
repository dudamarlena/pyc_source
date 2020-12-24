# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_conv_tuner.py
# Compiled at: 2020-04-02 03:48:10
# Size of source mod 2**32: 7034 bytes
import unittest, jittor as jt, os, numpy as np
from jittor import compile_extern
from jittor.test.test_log import find_log_with_re
if compile_extern.has_cuda:
    from jittor.compile_extern import cublas_ops, cudnn_ops
else:
    cublas_ops = cudnn_ops = None

def conv_nchw(x, in_planes, out_planes, kernel_size, padding, stride=1, dilation=1, init_method=None, w_=None):
    Kw = kernel_size
    Kh = kernel_size
    _C = in_planes
    Kc = out_planes
    N, C, H, W = x.shape
    if not C == _C:
        raise AssertionError
    elif w_ is None:
        if init_method == None:
            w = jt.make_var([Kc, _C, Kh, Kw], init=(lambda *a: (init.relu_invariant_gauss)(*a, **{'mode': 'fan_out'})))
        else:
            w = jt.make_var([Kc, _C, Kh, Kw], init=init_method)
    else:
        w = w_
    oh = (H - Kh * dilation + dilation - 1 + padding * 2) // stride + 1
    ow = (W - Kw * dilation + dilation - 1 + padding * 2) // stride + 1
    xx = x.reindex([N, Kc, C, oh, ow, Kh, Kw], [
     'i0',
     'i2',
     f"i3*{stride}-{padding}+i5*{dilation}",
     f"i4*{stride}-{padding}+i6*{dilation}"])
    ww = w.broadcast(xx.shape, [0, 3, 4])
    yy = xx * ww
    y = yy.sum([2, 5, 6])
    return y


def conv_nhwc(x, in_planes, out_planes, kernel_size, padding, stride=1, dilation=1, init_method=None, w_=None):
    Kw = kernel_size
    Kh = kernel_size
    _C = in_planes
    Kc = out_planes
    N, H, W, C = x.shape
    if not C == _C:
        raise AssertionError
    elif w_ is None:
        if init_method == None:
            w = jt.make_var([Kc, _C, Kh, Kw], init=(lambda *a: (init.relu_invariant_gauss)(*a, **{'mode': 'fan_out'})))
        else:
            w = jt.make_var([Kc, _C, Kh, Kw], init=init_method)
    else:
        w = w_
    oh = (H - Kh * dilation + dilation - 1 + padding * 2) // stride + 1
    ow = (W - Kw * dilation + dilation - 1 + padding * 2) // stride + 1
    xx = x.reindex([N, Kc, C, oh, ow, Kh, Kw], [
     'i0',
     f"i3*{stride}-{padding}+i5*{dilation}",
     f"i4*{stride}-{padding}+i6*{dilation}",
     'i2'])
    ww = w.broadcast(xx.shape, [0, 3, 4])
    yy = xx * ww
    y = yy.sum([2, 5, 6])
    return y


def test_nhwc(x, w, stride, padding, dilation):
    out_planes, in_planes, kernel_size, _ = w.shape
    return conv_nhwc(x, in_planes, out_planes, kernel_size, padding, stride=stride, dilation=dilation, w_=w)


def test_nchw(x, w, stride, padding, dilation):
    out_planes, in_planes, kernel_size, _ = w.shape
    return conv_nchw(x, in_planes, out_planes, kernel_size, padding, stride=stride, dilation=dilation, w_=w)


def check_forward(xshape, wshape, stride, padding, dilation, use_cuda, nhwc):
    if nhwc:
        test_func = test_nhwc
    else:
        test_func = test_nchw
    if use_cuda == 1:
        op_name = 'cudnn_conv'
    else:
        op_name = 'mkl_conv'
    with jt.log_capture_scope(use_cuda=use_cuda, enable_tuner=1, log_v=0,
      log_vprefix='op.cc=100',
      compile_options={'test': 266}) as (raw_log):
        x = jt.random(xshape)
        w = jt.random(wshape)
        y = test_func(x, w, stride, padding, dilation)
        y.sync()
    with jt.flag_scope(use_cuda=0, enable_tuner=0, compile_options={'test': 255}):
        cy = test_func(x, w, stride, padding, dilation)
        cy.sync()
    logs = find_log_with_re(raw_log, '(Jit op key (not )?found: ' + op_name + '.*)')
    if not (len(logs) == 1 and 'oihw' in logs[0][0]):
        raise AssertionError(logs)
    assert np.allclose(y.data, cy.data)


def check_backward(xshape, wshape, stride, padding, dilation, use_cuda, nhwc):
    if nhwc:
        test_func = test_nhwc
    else:
        test_func = test_nchw
    if use_cuda == 1:
        op_name = 'cudnn_conv'
    else:
        op_name = 'mkl_conv'
    with jt.log_capture_scope(use_cuda=use_cuda, enable_tuner=1, log_v=1,
      log_vprefix='op.cc=100,exe=1000',
      compile_options={'test': 244}) as (raw_log):
        x = jt.random(xshape)
        w = jt.random(wshape)
        y = test_func(x, w, stride, padding, dilation)
        loss = y.mean()
        dx, dw = jt.grad(loss, [x, w])
        jt.sync([y, loss, dx, dw])
    with jt.flag_scope(use_cuda=0, enable_tuner=0, compile_options={'test': 233}):
        cy = test_func(x, w, stride, padding, dilation)
        closs = cy.mean()
        cdx, cdw = jt.grad(closs, [x, w])
        jt.sync([cy, closs, cdx, cdw])
    logs = find_log_with_re(raw_log, '(Jit op key (not )?found: ' + op_name + '.*)')
    if not (len(logs) == 3 and 'oihw' in logs[0][0]):
        raise AssertionError(logs)
    assert np.allclose(y.data, cy.data, 0.001)
    assert np.allclose(dw.data, cdw.data, 0.001), (dw.data, cdw.data)
    assert np.allclose(dx.data, cdx.data, 0.001), (dx.data, cdx.data, np.abs(cdx.data).max(), np.abs(dx.data - cdx.data).max())


class TestConvTuner(unittest.TestCase):

    def test_forward(self):
        for dilation in (1, 2, 3):
            check_forward([10, 100, 100, 3], [5, 3, 3, 3], 2, 0, dilation, 0, True)
            check_forward([10, 40, 50, 4], [5, 4, 5, 5], 1, 1, dilation, 0, True)
            check_forward([10, 40, 50, 4], [5, 4, 4, 4], 3, 1, dilation, 0, True)
            check_forward([10, 3, 100, 100], [5, 3, 3, 3], 2, 0, dilation, 0, False)
            check_forward([10, 4, 40, 50], [5, 4, 5, 5], 1, 1, dilation, 0, False)
            check_forward([10, 4, 40, 50], [5, 4, 4, 4], 3, 1, dilation, 0, False)

    def test_backward(self):
        for dilation in (1, 2, 3):
            check_backward([10, 3, 100, 100], [5, 3, 3, 3], 2, 0, dilation, 0, False)
            check_backward([10, 4, 40, 50], [5, 4, 5, 5], 1, 1, dilation, 0, False)
            check_backward([10, 4, 40, 50], [5, 4, 4, 4], 3, 1, dilation, 0, False)

    @unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
    def test_forward_cuda(self):
        for dilation in (1, 2, 3):
            check_forward([10, 100, 100, 3], [5, 3, 3, 3], 2, 0, dilation, 1, True)
            check_forward([10, 40, 50, 4], [5, 4, 5, 5], 1, 1, dilation, 1, True)
            check_forward([10, 40, 50, 4], [5, 4, 4, 4], 3, 1, dilation, 1, True)
            check_forward([10, 3, 100, 100], [5, 3, 3, 3], 2, 0, dilation, 1, False)
            check_forward([10, 4, 40, 50], [5, 4, 5, 5], 1, 1, dilation, 1, False)
            check_forward([10, 4, 40, 50], [5, 4, 4, 4], 3, 1, dilation, 1, False)

    @unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
    def test_backward_cuda(self):
        for dilation in (1, 2, 3):
            check_backward([10, 3, 100, 100], [5, 3, 3, 3], 2, 0, dilation, 1, False)
            check_backward([10, 4, 40, 50], [5, 4, 5, 5], 1, 1, dilation, 1, False)
            check_backward([10, 4, 40, 50], [5, 4, 4, 4], 3, 1, dilation, 1, False)


if __name__ == '__main__':
    unittest.main()