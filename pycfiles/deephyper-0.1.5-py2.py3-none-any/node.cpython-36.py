# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/node.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 5622 bytes
from tensorflow.keras.layers import Layer
from deephyper.search.nas.model.space.op.basic import Operation

class Node:
    __doc__ = 'This class represents a node of a graph\n\n    Args:\n        name (str): node name.\n    '
    num = 0

    def __init__(self, name='', *args, **kwargs):
        Node.num += 1
        self._num = Node.num
        self._tensor = None
        self.name = name

    def __str__(self):
        return f"{self.name}[id={self._num}]"

    @property
    def id(self):
        return self._num

    @property
    def op(self):
        raise NotImplementedError

    def create_tensor(self, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def verify_operation(op):
        if isinstance(op, Operation):
            return op
        if isinstance(op, Layer):
            return Operation(op)
        raise RuntimeError(f"Can't add this operation '{op.__name__}'. An operation should be either of type Operation or Layer when is of type: {type(op)}")


class OperationNode(Node):

    def __init__(self, name='', *args, **kwargs):
        (super().__init__)(args, name=name, **kwargs)

    def create_tensor(self, inputs=None, train=True, *args, **kwargs):
        if self._tensor is None:
            if inputs == None:
                self._tensor = self.op(train=train)
            else:
                self._tensor = self.op(inputs, train=train)
        return self._tensor


class VariableNode(OperationNode):
    __doc__ = 'This class represents a node of a graph where you have a set of possible operations. It means the agent will have to act to choose one of these operations.\n\n    >>> import tensorflow as tf\n    >>> from deephyper.search.nas.model.space.node import VariableNode\n    >>> vnode = VariableNode("VNode1")\n    >>> from deephyper.search.nas.model.space.op.op1d import Dense\n    >>> vnode.add_op(Dense(\n    ... units=10,\n    ... activation=tf.nn.relu))\n    >>> vnode.num_ops\n    1\n    >>> vnode.add_op(Dense(\n    ... units=1000,\n    ... activation=tf.nn.tanh))\n    >>> vnode.num_ops\n    2\n    >>> vnode.set_op(0)\n    >>> vnode.op.units\n    10\n\n    Args:\n        name (str): node name.\n    '

    def __init__(self, name=''):
        super().__init__(name=name)
        self._ops = list()
        self._index = None

    def __str__(self):
        if self._index != None:
            return f"{super().__str__()}(Variable[{str(self.op)}])"
        else:
            return f"{super().__str__()}(Variable[?])"

    def add_op(self, op):
        self._ops.append(self.verify_operation(op))

    @property
    def num_ops(self):
        return len(self._ops)

    def set_op(self, index):
        self.get_op(index).init()

    def get_op(self, index):
        if not 'float' in str(type(index)):
            if not type(index) is int:
                raise AssertionError(f"found type is : {type(index)}")
        else:
            if 'float' in str(type(index)):
                self._index = self.denormalize(index)
            else:
                assert 0 <= index and index < len(self._ops), f"len self._ops: {len(self._ops)}, index: {index}"
                self._index = index
        return self.op

    def denormalize(self, index):
        """Denormalize a normalized index to get an absolute indexes. Useful when you want to compare the number of different architectures.

        Args:
            indexes (float): a normalized index.

        Returns:
            int: An absolute indexes corresponding to the operation choosen with the relative index of `index`.
        """
        assert 0.0 <= index and index <= 1.0
        return int(index * len(self._ops))

    @property
    def op(self):
        if len(self._ops) == 0:
            raise RuntimeError("This VariableNode doesn't have any operation yet.")
        else:
            if self._index is None:
                raise RuntimeError('This VariableNode doesn\'t have any set operation, please use "set_op(index)" if you want to set one')
            else:
                return self._ops[self._index]

    @property
    def ops(self):
        return self._ops


class ConstantNode(OperationNode):
    __doc__ = "A ConstantNode represents a node with a fixed operation. It means the agent will not make any new decision for this node. The common use case for this node is to add a tensor in the graph.\n\n    >>> import tensorflow as tf\n    >>> from deephyper.search.nas.model.space.node import ConstantNode\n    >>> from deephyper.search.nas.model.space.op.op1d import Dense\n    >>> cnode = ConstantNode(op=Dense(units=100, activation=tf.nn.relu), name='CNode1')\n\n    Args:\n        op (Operation, optional): [description]. Defaults to None.\n        name (str, optional): [description]. Defaults to ''.\n    "

    def __init__(self, op=None, name='', *args, **kwargs):
        super().__init__(name=name)
        if op is not None:
            op = self.verify_operation(op)
            op.init()
        self._op = op

    def set_op(self, op):
        op = self.verify_operation(op)
        op.init()
        self._op = op

    def __str__(self):
        return f"{super().__str__()}(Constant[{str(self.op)}])"

    @property
    def op(self):
        return self._op


class MirrorNode(OperationNode):
    __doc__ = 'A MirrorNode is a node which reuse an other, it enable the reuse of keras layers. This node will not add operations to choose.\n\n    Arguments:\n        node {Node} -- [description]\n    '

    def __init__(self, node):
        super().__init__(name=f"Mirror[{str(node)}]")
        self._node = node

    @property
    def op(self):
        return self._node.op