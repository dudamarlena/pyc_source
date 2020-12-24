# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_reshape.py
# Compiled at: 2020-03-20 04:44:53
# Size of source mod 2**32: 2576 bytes
import unittest, jittor as jt, numpy as np
from .test_grad import ngrad
from .test_cuda import test_cuda

def get_node_info(s):
    mem_ptr = s.split(')')[0].split(',')[(-1)]
    name = s.split(')')[0].split(',')[(-2)]
    return (name, mem_ptr)


def get_info(graph):
    bop = [node for node in graph.nodes_info if node.startswith('Var')]
    node_dict = {}
    for bop_ in bop:
        name, mem_ptr = get_node_info(bop_)
        node_dict[name] = mem_ptr

    return node_dict


def check_equal(a, b):
    eps = 0.1
    return abs(a - b) < eps


class TestReshapeOp(unittest.TestCase):

    def test_reshape(self):
        a = jt.random([123, 456, 789]).name('a')
        b = jt.reshape(a, [246, int(179892.0)]).name('b')
        c = jt.reshape(b, [44253432]).name('c')
        d = jt.reshape(c, [2, int(41.0), 789, int(228.0), 3]).name('d')
        e = jt.reshape(d, [2, int(41.0), 789, -1, 3]).name('e')
        assert b.shape == [246, int(179892.0)]
        assert c.shape == [44253432]
        assert d.shape == [2, int(41.0), 789, int(228.0), 3]
        assert e.shape == [2, int(41.0), 789, int(228.0), 3]
        a_mean = a.mean().data
        b_mean = b.mean().data
        c_mean = c.mean().data
        d_mean = d.mean().data
        e_mean = e.mean().data
        a = (a + 1).name('new_a')
        new_a_mean = a.mean().data
        new_b_mean = b.mean().data
        node_dict = get_info(jt.dump_all_graphs())
        assert check_equal(a_mean, b_mean), f"{a_mean} != {b_mean}"
        assert check_equal(a_mean, c_mean), f"{a_mean} != {c_mean}"
        assert check_equal(a_mean, d_mean), f"{a_mean} != {d_mean}"
        assert check_equal(a_mean, e_mean), f"{a_mean} != {e_mean}"
        assert check_equal(b_mean, new_b_mean), f"{b_mean} != {new_b_mean}"
        if check_equal(a_mean, new_a_mean):
            raise AssertionError(f"{a_mean} == {new_a_mean}")
        assert node_dict['a'] == node_dict['b']
        assert node_dict['a'] == node_dict['c']
        assert node_dict['a'] == node_dict['d']
        assert node_dict['a'] == node_dict['e']


if __name__ == '__main__':
    unittest.main()