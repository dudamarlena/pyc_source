# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_reindex_op.py
# Compiled at: 2020-03-23 09:56:56
# Size of source mod 2**32: 9783 bytes
import unittest, jittor as jt, numpy as np
from .test_core import expect_error
from .test_grad import ngrad

def conv(x, w):
    N, H, W, C = x.shape
    Kh, Kw, _C, Kc = w.shape
    assert C == _C
    xx = x.reindex([N, H + Kh - 1, W + Kw - 1, Kh, Kw, C, Kc], [
     'i0',
     'i1-i3',
     'i2-i4',
     'i5'])
    ww = w.broadcast_var(xx)
    yy = xx * ww
    y = yy.sum([3, 4, 5])
    return (y, yy)


def conv_naive(x, w):
    N, H, W, C = x.shape
    Kh, Kw, _C, Kc = w.shape
    assert C == _C
    y = np.zeros([N, H + Kh - 1, W + Kw - 1, Kc])
    for i0 in range(N):
        for i1 in range(H + Kh - 1):
            for i2 in range(W + Kw - 1):
                for i3 in range(Kh):
                    for i4 in range(Kw):
                        for i5 in range(C):
                            for i6 in range(Kc):
                                if not i1 - i3 < 0:
                                    if i2 - i4 < 0 or i1 - i3 >= H or i2 - i4 >= W:
                                        continue
                                    y[(i0, i1, i2, i6)] += x[(i0, i1 - i3, i2 - i4, i5)] * w[(i3, i4, i5, i6)]

    return y


def conv_transpose(x, w):
    N, H, W, C = x.shape
    Kh, Kw, _C, Kc = w.shape
    assert C == _C
    xx = x.reindex([N, H * 2 + Kh - 1, W * 2 + Kw - 1, Kh, Kw, C, Kc], [
     'i0',
     '(i1-i3)/2',
     '(i2-i4)/2',
     'i5'], 0, ['(i1-i3)%2', '(i2-i4)%2'])
    ww = w.broadcast_var(xx)
    yy = xx * ww
    y = yy.sum([3, 4, 5])
    return (y, yy)


def conv_transpose_naive(x, w):
    N, H, W, C = x.shape
    Kh, Kw, _C, Kc = w.shape
    assert C == _C
    y = np.zeros([N, H * 2 + Kh - 1, W * 2 + Kw - 1, Kc])
    for i0 in range(N):
        for i1 in range(H * 2 + Kh - 1):
            for i2 in range(W * 2 + Kw - 1):
                for i3 in range(Kh):
                    for i4 in range(Kw):
                        for i5 in range(C):
                            for i6 in range(Kc):
                                if not (i1 - i3) // 2 < 0:
                                    if (i2 - i4) // 2 < 0 or (i1 - i3) // 2 >= H or (i2 - i4) // 2 >= W:
                                        continue
                                    if (i1 - i3) % 2 or (i2 - i4) % 2:
                                        continue
                                    y[(i0, i1, i2, i6)] += x[(i0, (i1 - i3) // 2, (i2 - i4) // 2, i5)] * w[(i3, i4, i5, i6)]

    return y


def is_fused(x):
    x.name('_x')
    graph = jt.dump_all_graphs()
    node_a = [node for node in graph.nodes_info if ',_x,' in node]
    return 's0' in node_a[0]


def check_fused(dim):
    jt.clean()
    graph = jt.dump_all_graphs()
    fused = True
    has_v = False
    for node in graph.nodes_info:
        shape = node.split('[')[(-1)].split(',')
        ndim = len(shape) - 1
        if ndim > dim:
            has_v = True
            if 's0' not in node:
                fused = False

    if not (fused and has_v):
        raise AssertionError(graph.nodes_info)


def resize_and_crop(x, bbox, interpolation='nearest'):
    N, k = bbox.shape
    H, W = x.shape
    assert k == 4
    shape = [N, H, W]
    img = x
    bb = [bbox.reindex(shape, ['i0', str(i)]) for i in range(4)]
    hid = jt.index(shape, 1)
    wid = jt.index(shape, 2)
    one = jt.float(1).broadcast(shape)
    x = bb[0] * jt.float(H - 1) + hid * (bb[2] - bb[0])
    y = bb[1] * jt.float(W - 1) + wid * (bb[3] - bb[1])
    if interpolation == 'nearest':
        return img.reindex_var([x.round(), y.round()])
    if interpolation == 'bilinear':
        fx, fy = x.floor(), y.floor()
        cx, cy = fx + one, fy + one
        dx, dy = x - fx, y - fy
        a = img.reindex_var([fx, fy])
        b = img.reindex_var([cx, fy])
        c = img.reindex_var([fx, cy])
        d = img.reindex_var([cx, cy])
        dnx, dny = one - dx, one - dy
        ab = dx * b + dnx * a
        cd = dx * d + dnx * c
        o = ab * dny + cd * dy
        return o
    raise f"Not support {interpolation}"


def resize_and_crop_naive(x, bbox, interpolation='nearest'):
    N, k = bbox.shape
    H, W = x.shape
    assert k == 4
    y = np.zeros([N, H, W])
    if interpolation == 'nearest':
        for i in range(N):
            for j in range(H):
                for k in range(W):
                    nj = int(round(bbox[(i, 0)] * (H - 1) + j * (bbox[(i, 2)] - bbox[(i, 0)])))
                    nk = int(round(bbox[(i, 1)] * (W - 1) + k * (bbox[(i, 3)] - bbox[(i, 1)])))
                    if nk < 0 or nk >= W or nj < 0 or nj >= H:
                        y[(i, j, k)] = 0
                    else:
                        y[(i, j, k)] = x[(nj, nk)]

        return y
    from math import floor, ceil
    data = x
    output = y
    sample = --- This code section failed: ---

 L. 162         0  LOAD_FAST                'nk'
                2  LOAD_CONST               0
                4  COMPARE_OP               <
                6  POP_JUMP_IF_TRUE     32  'to 32'
                8  LOAD_FAST                'nk'
               10  LOAD_DEREF               'W'
               12  COMPARE_OP               >=
               14  POP_JUMP_IF_TRUE     32  'to 32'
               16  LOAD_FAST                'nj'
               18  LOAD_CONST               0
               20  COMPARE_OP               <
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  LOAD_FAST                'nj'
               26  LOAD_DEREF               'H'
               28  COMPARE_OP               >=
               30  POP_JUMP_IF_FALSE    36  'to 36'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            14  '14'
             32_2  COME_FROM             6  '6'
               32  LOAD_CONST               0
               34  RETURN_VALUE_LAMBDA
             36_0  COME_FROM            30  '30'
               36  LOAD_DEREF               'data'
               38  LOAD_FAST                'nj'
               40  LOAD_FAST                'nk'
               42  BUILD_TUPLE_2         2 
               44  BINARY_SUBSCR    
               46  RETURN_VALUE_LAMBDA
               -1  LAMBDA_MARKER    

Parse error at or near `None' instruction at offset -1
    for i in range(N):
        for j in range(H):
            for k in range(W):
                x = bbox[(i, 0)] * (H - 1) + j * (bbox[(i, 2)] - bbox[(i, 0)])
                y = bbox[(i, 1)] * (W - 1) + k * (bbox[(i, 3)] - bbox[(i, 1)])
                fx, fy = floor(x), floor(y)
                cx, cy = fx + 1, fy + 1
                a = sample(fx, fy)
                b = sample(cx, fy)
                c = sample(fx, cy)
                d = sample(cx, cy)
                dx, dy = x - fx, y - fy
                dnx, dny = 1 - dx, 1 - dy
                ab = dx * b + dnx * a
                cd = dx * d + dnx * c
                o = ab * dny + cd * dy
                output[(i, j, k)] = o

    return output


class TestReindexOp(unittest.TestCase):

    def test_pad(self):
        size = 10
        lpad = 3
        rpad = 4
        a = jt.random([size])
        b = a.reindex([size + lpad + rpad], [f"i0-{lpad}"], -1)
        na, nb = jt.fetch_sync([a, b])
        assert (nb[lpad:lpad + size] == na).all()
        assert (nb[:lpad] == -1).all()
        assert (nb[-rpad:] == -1).all()

    def test_matmul(self):
        size = 10
        a = jt.random([size, size])
        b = jt.random([size, size])
        cc = a.reindex([size, size, size], ['i0', 'i1']) * b.reindex([size, size, size], ['i1', 'i2'])
        c = cc.sum(dim=1)
        na, nb, nc = jt.fetch_sync([a, b, c])
        assert is_fused(cc)
        assert not is_fused(c)
        check_fused(len(a.shape))
        npc = np.matmul(na, nb)
        assert np.allclose(npc, nc)

    def test_conv(self):
        N, H, W, C = (3, 10, 10, 3)
        Kh, Kw, Kc = (3, 3, 4)
        x = jt.random([N, H, W, C])
        w = jt.random([Kh, Kw, C, Kc])
        y, yy = conv(x, w)
        ny = y.data
        assert ny.shape == (N, H + Kh - 1, W + Kw - 1, Kc), (ny.shape, [N, H + Kh - 1, W + Kw - 1, Kc])
        assert is_fused(yy)
        check_fused(len(x.shape))
        npy = conv_naive(x.data, w.data)
        assert np.allclose(npy, ny)

    def test_conv_transpose(self):
        N, H, W, C = (3, 10, 10, 3)
        Kh, Kw, Kc = (3, 3, 4)
        x = jt.random([N, H, W, C])
        w = jt.random([Kh, Kw, C, Kc])
        y, yy = conv_transpose(x, w)
        ny = y.data
        assert is_fused(yy)
        check_fused(len(x.shape))
        npy = conv_transpose_naive(x.data, w.data)
        assert np.allclose(npy, ny), (np.where(np.abs(npy - ny) > 0.0001), npy[0, :4, :4, 0], ny[0, :4, :4, 0])

    def test_conv_transpose_grad(self):
        N, H, W, C = (1, 5, 5, 2)
        Kh, Kw, Kc = (3, 3, 2)
        x = jt.random([N, H, W, C])
        w = jt.random([Kh, Kw, C, Kc])
        y, yy = conv_transpose(x, w)
        mask = jt.random(y.shape)
        loss = (y * mask).sum()
        dx, dw = jt.grad(loss, [x, w])
        jdx, jdw = jt.fetch_sync([dx, dw])
        check_fused(len(x.shape))
        nmask = mask.data
        _, (ndx, ndw) = ngrad(lambda args: (conv_transpose_naive(args[0], args[1]) * nmask).sum(), [
         np.float64(x.data), np.float64(w.data)], 1e-07)
        assert np.allclose(ndx, jdx), (ndx, jdx, ndx - jdx)
        assert np.allclose(ndw, jdw), (ndw, jdw)

    def test_resize_and_crop(self):
        jt.set_seed(3)
        N, H, W = (4, 5, 5)
        for interpolation in ('bilinear', 'nearest'):
            x = jt.random([H, W])
            bbox = jt.random([N, 4])
            y = resize_and_crop(x, bbox, interpolation)
            ny = resize_and_crop_naive(x.data, bbox.data, interpolation)
            assert np.allclose(y.data, ny), (y.data, ny, x.data)
            mask = jt.random(y.shape)
            nmask = mask.data
            import gc
            gc.collect()
            loss = y * mask
            dx, dbbox = jt.grad(loss, [x, bbox])
            _, (ndx, ndbbox) = ngrad(lambda args: (resize_and_crop_naive(args[0], args[1], interpolation) * nmask).sum(), [
             np.float64(x.data), np.float64(bbox.data)], 1e-07)
            assert np.allclose(y.data, ny), (y.data, ny, x.data)
            assert np.allclose(ndx, dx.data, 0.01), (ndx, dx.data)
            assert np.allclose(ndbbox, dbbox.data, 0.01), (ndbbox, dbbox.data)

    def test_doc(self):
        assert 'Reindex Operator' in jt.reindex.__doc__


@unittest.skipIf(not jt.compiler.has_cuda, 'No CUDA found')
class TestReindexOpCuda(TestReindexOp):

    def setUp(self):
        jt.flags.use_cuda = 1

    def tearDown(self):
        jt.flags.use_cuda = 0


if __name__ == '__main__':
    unittest.main()