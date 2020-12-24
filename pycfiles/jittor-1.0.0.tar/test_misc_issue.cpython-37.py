# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_misc_issue.py
# Compiled at: 2020-04-16 03:52:00
# Size of source mod 2**32: 4118 bytes
import unittest, jittor as jt, os, numpy as np

class TestMiscIssue(unittest.TestCase):

    def test_issue4(self):
        try:
            jt.dirty_fix_pytorch_runtime_error()
            import torch
        except:
            return
        else:
            src = 'N = 100\nimport jittor as jt\na = jt.random([N, N])\nb = a.broadcast([N,N,N], dims=[0]) * a.broadcast([N,N,N], dims=[2])\nb = b.sum(1)\nb.sync()\n\nimport torch\nA = torch.rand(N, N)\ntorch.matmul(A, A)\n'
            assert os.system(f"python3.7 -c '{src}'") == 0
            src = 'N = 100\nimport torch\nA = torch.rand(N, N)\ntorch.matmul(A, A)\n\nimport jittor as jt\na = jt.random([N, N])\nb = a.broadcast([N,N,N], dims=[0]) * a.broadcast([N,N,N], dims=[2])\nb = b.sum(1)\nb.sync()\n'
            assert os.system(f"python3.7 -c '{src}'") == 0

    def test_mkl_conflict1(self):
        try:
            jt.dirty_fix_pytorch_runtime_error()
            import torch
        except:
            return
        else:
            if jt.mkl_ops is None:
                return
            src = '\nnchw = [2, 3, 100, 100]\noihw = [4, 3, 5, 5]\nimport jittor as jt\nx = jt.random(nchw)\nw = jt.random(oihw)\njt.mkl_ops.mkl_conv(x, w, 1, 2).sync()\n\njt.dirty_fix_pytorch_runtime_error()\n\nimport torch\nm = torch.nn.Conv2d(3, 4, 5, 1, 2)\nm(torch.rand(*nchw))\n\n'
            assert os.system(f"python3.7 -c '{src}'") == 0

    def test_mkl_conflict2(self):
        try:
            jt.dirty_fix_pytorch_runtime_error()
            import torch
        except:
            return
        else:
            if jt.mkl_ops is None:
                return
            src = '\nnchw = [2, 3, 100, 100]\noihw = [4, 3, 5, 5]\n\nimport torch\nm = torch.nn.Conv2d(3, 4, 5, 1, 2)\nm(torch.rand(*nchw))\n\nimport jittor as jt\nx = jt.random(nchw)\nw = jt.random(oihw)\njt.mkl_ops.mkl_conv(x, w, 1, 2).sync()\n\n\n'
            assert os.system(f"python3.7 -c '{src}'") == 0

    def test_parallel(self):
        a = jt.code([4], 'int', cpu_src='\n            #pragma omp parallel num_threads(4)\n            @out(omp_get_thread_num()) = 456;\n        ',
          cpu_header='#include <omp.h>').data
        assert (a == [456] * 4).all(), a

    @unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
    @jt.flag_scope(use_cuda=1)
    def test_reduce_opt(self):
        a = jt.random((16, 512, 38, 38))
        b = jt.random((16, 512, 38, 38))
        jt.sync([a, b])
        with jt.profile_scope(rerun=10, warmup=10) as (rep):
            norm = a.sqr().sum(1, keepdims=True).sqrt()
            c = a / norm
            da = jt.grad(c * b, a)
            jt.sync([c, da])
        gpu_c = c.numpy()
        gpu_da = da.numpy()
        with jt.flag_scope(use_cuda=0):
            norm = a.sqr().sum(1, keepdims=True).sqrt()
            c = a / norm
            da = jt.grad(c * b, a)
            assert np.allclose(gpu_c, c.data, 0.001)
            assert np.abs(gpu_da - da.data).max() < 1e-06
        assert float(rep[1][3]) < 15000000.0, float(rep[1][3])

    @unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
    @jt.flag_scope(use_cuda=1)
    def test_cuda_min_max(self):
        a = jt.random((10, )) - 2
        assert a.min().data == a.data.min(), (a.min(), a.data.min())
        assert a.max().data == a.data.max(), (a.max(), a.data.max())

    @unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
    @jt.flag_scope(use_cuda=1)
    def test_cuda_pow_grad_nan(self):
        a = jt.float32([1, -1, -1000.1])
        da = jt.grad(a ** 2, a)
        assert np.isnan(da.data).sum() == 0, da.data

    def test_tanh_nan(self):
        m = jt.nn.Tanh()
        a = m(jt.array([1000]))
        assert np.isnan(a.data).sum() == 0, a


if __name__ == '__main__':
    unittest.main()