# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_longest_dis_fuse.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 3020 bytes
import sys, os, jittor as jt, unittest, time, numpy as np

def get_init_var(shape, dtype):
    return jt.random(shape, dtype)


def batch_norm(x):
    xmean = jt.mean(x, dims=[0, 2, 3], keepdims=1)
    x2mean = jt.mean((x * x), dims=[0, 2, 3], keepdims=1)
    norm_x = (x - xmean.broadcast_var(x)) / jt.sqrt(x2mean - xmean * xmean + jt.float32(1e-05)).broadcast_var(x)
    w = jt.make_var([x.shape[1]], init=get_init_var)
    b = jt.make_var([x.shape[1]], init=get_init_var)
    w = w.broadcast([1, w.shape[0], 1, 1], [0, 2, 3])
    b = b.broadcast([1, b.shape[0], 1, 1], [0, 2, 3])
    return norm_x * w + b


def pool(x, size, op, padding, stride=1):
    N, C, H, W = x.shape
    h = (H + padding * 2 - size) // stride + 1
    w = (W + padding * 2 - size) // stride + 1
    xx = x.reindex([N, C, h, w, size, size], [
     'i0',
     'i1',
     f"i2*{stride}-{padding}+i4",
     f"i3*{stride}-{padding}+i5"])
    return xx.reindex_reduce(op, [N, C, h, w], [
     'i0',
     'i1',
     'i2',
     'i3'])


def conv(x, in_planes, out_planes, kernel_size, padding, stride=1):
    Kw = kernel_size
    Kh = kernel_size
    _C = in_planes
    Kc = out_planes
    N, C, H, W = x.shape
    assert C == _C
    w = jt.make_var([Kc, _C, Kh, Kw], init=get_init_var)
    xx = x.reindex([N, Kc, C, (H + padding * 2 - kernel_size) // stride + 1, (W + padding * 2 - kernel_size) // stride + 1, Kh, Kw], [
     'i0',
     'i2',
     f"i3*{stride}-{padding}+i5",
     f"i4*{stride}-{padding}+i6"])
    ww = w.broadcast(xx.shape, [0, 3, 4])
    yy = xx * ww
    y = yy.sum([2, 5, 6])
    return y


def relu(x):
    return jt.maximum(x, jt.float32(0))


@jt.var_scope('resnet_fake', unique=True)
def resnet_fake(x):
    x = conv(x, 3, 64, 7, 3, 2)
    x = batch_norm(x)
    x = relu(x)
    x = pool(x, 3, 'maximum', 1, 2)
    return x


class TestLongestDisFuse(unittest.TestCase):

    def test_longest_dis_fuse(self):
        x = jt.array(np.random.rand(1, 3, 224, 224).astype(np.float32))
        loss = jt.sum(resnet_fake(x))
        ps = jt.find_vars('resnet_fake')
        gs = jt.grad(loss, ps)
        jt.sync(gs)
        g = jt.dump_all_graphs()
        for s in g.nodes_info:
            if not s.startswith('Var'):
                continue
            shape = s.split('[')[1].split(']')[0].split(',')
            ptr = s.split('(')[1].split(')')[0].split(',')[(-1)]
            if ptr != '0' and not len(shape) <= 5:
                raise AssertionError(s)


if __name__ == '__main__':
    unittest.main()