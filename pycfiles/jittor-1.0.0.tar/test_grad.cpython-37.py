# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_grad.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 5120 bytes
import unittest, jittor as jt, numpy as np
from .test_core import expect_error

def equal_size(x, y):
    return x.dtype == y.dtype and x.shape == y.shape


def ngrad(func, vars, eps):
    out = func(vars)
    dout = []
    for i in range(len(vars)):
        pvar = vars[i].astype('float64')
        if type(pvar) == np.ndarray and pvar.size > 1:
            grad = []
            var_f = pvar.flatten()
            for j in range(len(var_f)):
                var = pvar.flatten()
                var[j] += eps
                vars[i] = var.reshape(pvar.shape)
                out2 = func(vars)
                grad.append((out2 - out) / eps)

            dout.append(np.array(grad).reshape(pvar.shape))
        else:
            vars[i] = vars[i] + eps
            out2 = func(vars)
            dout.append((out2 - out) / eps)
        vars[i] = pvar

    return (
     out, dout)


class TestGrad(unittest.TestCase):

    def test_grad(self):
        x = jt.array([1.0, 2.0])
        y = jt.array([3.0, 4.0])
        z = x * y
        dx, dy, dz = jt.grad(z, [x, y, z])
        if not (equal_size(dx, x) and equal_size(dy, y)):
            raise AssertionError(f"{x} {y} {dx} {dy}")
        assert (dy.data == x.data).all(), f"{dy.data} {x.data}"
        assert (dx.data == y.data).all(), f"{dx.data} {y.data}"
        assert (dz.data == 1).all()

    def test_check_float(self):
        x = jt.array(1)
        y = x * x
        expect_error(lambda : jt.grad(y, [x]))

    def test_grad2(self):

        def test(n):
            x = jt.array(2.0)
            y = x
            for _ in range(n - 1):
                y = y * x

            dx, = jt.grad(y, [x])
            assert dx.data == n * 2 ** (n - 1), f"{dx.data} {x.data}, {y.data}"

        test(5)
        test(6)
        test(7)
        test(8)

    def test_var_index(self):
        x = jt.array(2.0)
        y = x - x
        dx, = jt.grad(y, [x])
        assert dx.data == 0, dx.data
        x = jt.array(2.0)
        y = x / x
        dx, = jt.grad(x, [y])
        assert dx.data == 0

    def test_random_graph(self):

        def test(num_vars, num_ops, seed):
            np.random.seed(seed)
            vars = []
            for _ in range(num_vars):
                vars.append(np.random.rand(1))

            def random_func(vars):
                np.random.seed(seed + 1)
                vars = list(vars)
                for i in range(num_ops):
                    v1 = len(vars) - 1 - np.random.randint(num_vars)
                    v2 = len(vars) - 1 - np.random.randint(num_vars)
                    rop = '+-*/'[np.random.randint(4)]
                    if not rop == '/':
                        if rop == '-':
                            if v1 is v2:
                                rop = '+'
                        vout = eval(f"vars[v1]{rop}vars[v2]")
                        vars.append(vout)

                if type(vars[i]) == jt.Var:
                    for i in range(len(vars)):
                        vars[i].name('v' + str(i))

                return vout

            np_out, np_dout = ngrad(random_func, vars, 1e-07)
            jt_vars = [jt.array(v) for v in vars]
            jt_out = random_func(jt_vars)
            assert (np.abs(jt_out.data - np_out) < 1e-05).all(), (jt_out.data, np_out)
            jt_dout = jt.grad(jt_out, jt_vars)
            jt_dout = [v.data for v in jt_dout]
            for jt_d, np_d in zip(jt_dout, np_dout):
                assert abs(jt_d - np_d) < 0.001, f"{jt_d} {np_d}"

        test(1, 1, 0)
        test(3, 6, 0)
        test(10, 100, 2)
        test(30, 100, 4)
        test(50, 100, 6)

    def test_top_sort(self):
        x = jt.array(2.0)
        x.name('x')
        y1 = x * x
        y1.name('y1')
        y2 = x * x
        y2.name('y2')
        y3 = y1 * y2
        y3.name('y3')
        y4 = y3 * y1
        y4.name('y4')
        y5 = y4 * y1
        y5.name('y5')
        y6 = y5 * y1
        y6.name('y6')
        vars = [x, y1, y2, y3, y4, y5, y6]
        grads = [g.data for g in jt.grad(y6, vars)]
        dx = grads[0]
        assert dx == 5120, (f"{grads}")

    def test_int_grad(self):
        x = jt.array(2.0)
        z = x * x * x * x * x
        dx, = jt.grad(z, [x])
        self.assertEqual(dx.data, 80)
        y1 = jt.int(x)
        y2 = jt.float(x)
        z = x * x * y1 * y1 * y2
        expect_error(lambda : jt.grad(z, [y1]))
        dx, = jt.grad(z, [x])
        self.assertEqual(dx.data, 48)

    def test_nth_grad(self):
        x = jt.array(2.0)
        y = x * x * x * x
        dx = jt.grad(y, x)
        ddx = jt.grad(dx, x)
        dddx = jt.grad(ddx, x)
        self.assertEqual(y.data, 16)
        self.assertEqual(dx.data, 32)
        self.assertEqual(ddx.data, 48)
        self.assertEqual(dddx.data, 48)


if __name__ == '__main__':
    unittest.main()