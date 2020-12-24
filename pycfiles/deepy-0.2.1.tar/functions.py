# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/functions.py
# Compiled at: 2016-05-18 19:34:36
import os, theano, theano.tensor as T, numpy as np, re, copy
from theano.sandbox.rng_mrg import MRG_RandomStreams as RandomStreams
import logging as loggers
logging = loggers.getLogger(__name__)
logging.setLevel(loggers.INFO)
FLOATX = theano.config.floatX
EPSILON = T.constant(1e-15, dtype=FLOATX)
BIG_EPSILON = T.constant(1e-07, dtype=FLOATX)
if 'DEEPY_SEED' in os.environ:
    global_seed = int(os.environ['DEEPY_SEED'])
    logging.info('set global random seed to %d' % global_seed)
else:
    global_seed = 3
global_rand = np.random.RandomState(seed=global_seed)
global_theano_rand = RandomStreams(seed=global_seed)

def onehot(size, eye):
    return np.eye(1, size, eye, dtype=FLOATX)[0]


def onehot_tensor(i_matrix, vocab_size):
    """
    # batch x time
    """
    dim0, dim1 = i_matrix.shape
    i_vector = i_matrix.reshape((-1, ))
    hot_matrix = T.extra_ops.to_one_hot(i_vector, vocab_size).reshape((dim0, dim1, vocab_size))
    return hot_matrix


def shared_scalar(value, name=None):
    """
    Create a shared theano scalar value.
    """
    return theano.shared(np.array(value, dtype=FLOATX), name=name)


def make_float_matrices(*names):
    ret = []
    for n in names:
        ret.append(T.matrix(n, dtype=FLOATX))

    return ret


def make_float_vectors(*names):
    ret = []
    for n in names:
        ret.append(T.vector(n, dtype=FLOATX))

    return ret


def monitor_var(value, name='', disabled=False):
    if disabled:
        return value
    else:
        return theano.printing.Print(name)(value)


def monitor_var_sum(value, name='', disabled=False):
    if disabled:
        return T.sum(value) * 0
    else:
        val = T.sum(theano.printing.Print(name)(value)) * T.constant(1e-07, dtype=FLOATX)
        return T.cast(val, FLOATX)


def back_grad(jacob, err_g):
    return T.dot(jacob, err_g)


def replace_graph(node, dct, deepcopy=True):
    """
    Replace nodes in a computational graph (Safe).
    """
    if not hasattr(node, 'owner'):
        return node
    if not hasattr(node.owner, 'inputs'):
        return node
    if deepcopy:
        new_node = copy.deepcopy(node)
        new_node.owner.inputs = copy.copy(node.owner.inputs)
        node = new_node
    owner = node.owner
    for i, elem in enumerate(owner.inputs):
        if elem in dct:
            owner.inputs[i] = dct[elem]
        else:
            owner.inputs[i] = replace_graph(elem, dct)

    return node


def build_node_name(n):
    if 'owner' not in dir(n) or 'inputs' not in dir(n.owner):
        return str(n)
    else:
        op_name = str(n.owner.op)
        if '{' not in op_name:
            op_name = 'Elemwise{%s}' % op_name
        if ',' in op_name:
            op_name = re.sub('\\{([^}]+),[^}]+\\}', '{\\1}', op_name)
        if '_' in op_name:
            op_name = re.sub('\\{[^}]+_([^_}]+)\\}', '{\\1}', op_name)
        return '%s(%s)' % (op_name, (',').join([ build_node_name(m) for m in n.owner.inputs ]))


def smart_replace_graph(n, dct, name_map=None, deepcopy=True):
    """
    Replace nodes in a computational graph (Smart).
    """
    if not name_map:
        name_map = {}
        for src, dst in dct.items():
            name_map[build_node_name(src)] = dst

    if not hasattr(n, 'owner'):
        return n
    if not hasattr(n.owner, 'inputs'):
        return n
    if deepcopy:
        new_node = copy.deepcopy(n)
        new_node.owner.inputs = copy.copy(n.owner.inputs)
        n = new_node
    owner = n.owner
    for i, elem in enumerate(owner.inputs):
        if elem in dct:
            owner.inputs[i] = dct[elem]
        elif build_node_name(elem) in name_map:
            owner.inputs[i] = name_map[build_node_name(elem)]
        else:
            owner.inputs[i] = smart_replace_graph(elem, dct, name_map, deepcopy)

    return n


class VarMap:

    def __init__(self):
        self.varmap = {}

    def __get__(self, instance, owner):
        if instance not in self.varmap:
            return
        else:
            return self.varmap[instance]
            return

    def __set__(self, instance, value):
        self.varmap[instance] = value

    def __contains__(self, item):
        return item in self.varmap

    def update_if_not_existing(self, name, value):
        if name not in self.varmap:
            self.varmap[name] = value

    def get(self, name):
        return self.varmap[name]

    def set(self, name, value):
        self.varmap[name] = value


import numpy as np
chars = [
 ' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']

def plot_hinton(arr, max_arr=None):
    if max_arr == None:
        max_arr = arr
    arr = np.array(arr)
    max_val = max(abs(np.max(max_arr)), abs(np.min(max_arr)))
    print np.array2string(arr, formatter={'float_kind': lambda x: visual_hinton(x, max_val)}, max_line_width=5000)
    return


def visual_hinton(val, max_val):
    if abs(val) == max_val:
        step = len(chars) - 1
    else:
        step = int(abs(float(val) / max_val) * len(chars))
    colourstart = ''
    colourend = ''
    if val < 0:
        colourstart, colourend = ('\x1b[90m', '\x1b[0m')
    return colourstart + chars[step] + colourend


from theano.compile import ViewOp
from theano.gradient import DisconnectedType

class DisconnectedGrad(ViewOp):

    def grad(self, args, g_outs):
        return [ DisconnectedType()() for g_out in g_outs ]

    def connection_pattern(self, node):
        return [
         [
          False]]


disconnected_grad = DisconnectedGrad()