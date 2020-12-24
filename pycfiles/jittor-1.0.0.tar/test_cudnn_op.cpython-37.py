# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_cudnn_op.py
# Compiled at: 2020-04-02 03:49:09
# Size of source mod 2**32: 5793 bytes
import unittest, jittor as jt, os, numpy as np
from jittor import compile_extern
from jittor.test.test_log import find_log_with_re
if compile_extern.has_cuda:
    from jittor.compile_extern import cublas_ops, cudnn_ops
else:
    cublas_ops = cudnn_ops = None

def conv_oihw(x, w, stride=1, padding=0, dilation=1):
    if not (type(stride) == int and type(padding) == int):
        raise AssertionError
    N, H, W, C = x.shape
    c, C2, Kh, Kw = w.shape
    oh, ow = (H - Kh * dilation + dilation - 1 + padding * 2) // stride + 1, (W - Kw * dilation + dilation - 1 + padding * 2) // stride + 1
    if not C2 == C:
        assert C2 == 1, (C2, C)
    x = x.reindex([N, oh, ow, c, C2, Kh, Kw], [
     'i0',
     f"i1*{stride}+i5*{dilation}-{padding}",
     f"i2*{stride}+i6*{dilation}-{padding}",
     'i3' if (C2 == 1 and C > 1) else 'i4'])
    y = (x * w).sum([4, 5, 6])
    return y


def conv(x, w, stride, padding):
    out_planes, in_planes, kernel_size, _ = w.shape
    Kw = kernel_size
    Kh = kernel_size
    _C = in_planes
    Kc = out_planes
    N, C, H, W = x.shape
    assert C == _C
    xx = x.reindex([N, Kc, C, (H + padding * 2 - kernel_size) // stride + 1, (W + padding * 2 - kernel_size) // stride + 1, Kh, Kw], [
     'i0',
     'i2',
     f"i3*{stride}-{padding}+i5",
     f"i4*{stride}-{padding}+i6"])
    ww = w.broadcast(xx.shape, [0, 3, 4])
    yy = xx * ww
    y = yy.sum([2, 5, 6])
    return y


@unittest.skipIf(cudnn_ops == None, 'Not use cudnn, Skip')
class TestCudnnConvOp(unittest.TestCase):

    def test(self):

        def check(xshape, wshape, stride=1, padding=0, dilation=1):
            with jt.log_capture_scope(use_cuda=1, enable_tuner=1, log_v=0,
              log_vprefix='op.cc=100') as (raw_log):
                x = jt.random(xshape)
                w = jt.random(wshape)
                y = conv_oihw(x, w, stride, padding, dilation)
                y.sync()
            with jt.flag_scope(use_cuda=0, enable_tuner=1):
                cy = conv_oihw(x, w, stride, padding, dilation)
                cy.sync()
            logs = find_log_with_re(raw_log, '(Jit op key (not )?found: cudnn_conv.*)')
            if not (len(logs) == 1 and 'oihw' in logs[0][0]):
                raise AssertionError(logs)
            assert np.allclose(y.data, cy.data), np.abs(y.data - cy.data).max()

        check([10, 100, 100, 3], [5, 3, 3, 3], stride=2, padding=0, dilation=1)
        check([10, 40, 50, 4], [5, 4, 5, 5], stride=1, padding=1, dilation=1)
        check([10, 40, 50, 4], [5, 4, 4, 4], stride=3, padding=1, dilation=1)

    def test_backward_nhwc(self):
        pass

    def test_backward(self):

        def check(xshape, wshape, stride=1, padding=0, dilation=1):
            with jt.log_capture_scope(use_cuda=1, enable_tuner=1, log_v=1,
              log_vprefix='op.cc=100,exe=1000') as (raw_log):
                x = jt.random(xshape)
                w = jt.random(wshape)
                y = conv(x, w, stride, padding)
                mask = jt.random(y.shape)
                loss = mask * y
                dx, dw = jt.grad(loss, [x, w])
                jt.sync([y, loss, dx, dw])
            with jt.flag_scope(use_cuda=0, enable_tuner=0):
                cy = conv(x, w, stride, padding)
                closs = mask * cy
                cdx, cdw = jt.grad(closs, [x, w])
                jt.sync([cy, closs, cdx, cdw])
            logs = find_log_with_re(raw_log, '(Jit op key (not )?found: cudnn_conv.*)')
            if not (len(logs) == 3 and 'oihw' in logs[0][0]):
                raise AssertionError(logs)
            assert np.allclose(y.data, cy.data)
            assert np.allclose(dx.data, cdx.data, 0.01)
            assert np.allclose(dw.data, cdw.data, 0.01)

        check([10, 3, 100, 100], [5, 3, 3, 3], stride=2, padding=0, dilation=1)
        check([10, 4, 40, 50], [5, 4, 5, 5], stride=1, padding=1, dilation=1)
        check([10, 4, 40, 50], [5, 4, 4, 4], stride=3, padding=1, dilation=1)


if __name__ == '__main__':
    unittest.main()