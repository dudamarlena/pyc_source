# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/op/merge.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 4850 bytes
import tensorflow as tf
from tensorflow import keras
from deephyper.search.nas.model.space.op import Operation
import deephyper.search.nas.model.space.layers as deeplayers

class Concatenate(Operation):
    __doc__ = 'Concatenate operation.\n\n    Args:\n        graph:\n        node (Node): current_node of the operation\n        stacked_nodes (list(Node)): nodes to concatenate\n        axis (int): axis to concatenate\n    '

    def __init__(self, struct, node=None, stacked_nodes=None, axis=-1):
        self.struct = struct
        self.node = node
        self.stacked_nodes = stacked_nodes
        self.axis = axis

    def init(self):
        if self.stacked_nodes is not None:
            for n in self.stacked_nodes:
                self.struct.connect(n, self.node)

    def __call__(self, values, **kwargs):
        len_shp = max([len(x.get_shape()) for x in values])
        if len_shp > 3:
            raise RuntimeError('This concatenation is for 2D or 3D tensors only when a {len_shp}D is passed!')
        else:
            if len(values) > 1:
                if all(map(lambda x: len(x.get_shape()) == len_shp or len(x.get_shape()) == len_shp - 1, values)):
                    for i, v in enumerate(values):
                        if len(v.get_shape()) < len_shp:
                            values[i] = keras.layers.Reshape((
                             *tuple(v.get_shape()[1:]), *(1, )))(v)

                    if len_shp == 3:
                        max_len = max(map(lambda x: int(x.get_shape()[1]), values))
                        paddings = map(lambda x: max_len - int(x.get_shape()[1]), values)
                        for i, (p, v) in enumerate(zip(paddings, values)):
                            lp = p // 2
                            rp = p - lp
                            values[i] = keras.layers.ZeroPadding1D(padding=(
                             lp, rp))(v)

                else:
                    raise RuntimeError(f"All inputs of concatenation operation should have same shape length:\nnumber_of_inputs=={len(values)}\nshape_of_inputs=={[str(x.get_shape()) for x in values]}")
            if len(values) > 1:
                out = keras.layers.Concatenate(axis=(-1))(values)
            else:
                out = values[0]
        return out


class AddByPadding(Operation):
    __doc__ = 'Add operation.\n\n    Args:\n        graph:\n        node (Node): current_node of the operation\n        stacked_nodes (list(Node)): nodes to add\n        axis (int): axis to concatenate\n    '

    def __init__(self, struct=None, node=None, stacked_nodes=None, axis=-1):
        self.struct = struct
        self.node = node
        self.stacked_nodes = stacked_nodes
        self.axis = axis

    def init(self):
        if self.stacked_nodes is not None:
            for n in self.stacked_nodes:
                self.struct.connect(n, self.node)

    def __call__(self, values, **kwargs):
        values = values[:]
        max_len_shp = max([len(x.get_shape()) for x in values])
        if len(values) > 1:
            for i, v in enumerate(values):
                if len(v.get_shape()) < max_len_shp:
                    values[i] = keras.layers.Reshape((
                     *tuple(v.get_shape()[1:]),
                     *tuple(1 for i in range(max_len_shp - len(v.get_shape())))))(v)

            def max_dim_i(i):
                return max(map(lambda x: int(x.get_shape()[i]), values))

            max_dims = [None] + list(map(max_dim_i, range(1, max_len_shp)))

            def paddings_dim_i(i):
                return list(map(lambda x: max_dims[i] - int(x.get_shape()[i]), values))

            paddings_dim = list(map(paddings_dim_i, range(1, max_len_shp)))
            for i in range(len(values)):
                paddings = list()
                for j in range(len(paddings_dim)):
                    p = paddings_dim[j][i]
                    lp = p // 2
                    rp = p - lp
                    paddings.append([lp, rp])

                if sum(map(sum, paddings)) != 0:
                    values[i] = deeplayers.Padding(paddings)(values[i])

        else:
            if len(values) > 1:
                out = keras.layers.Add()(values)
            else:
                out = values[0]
        return out