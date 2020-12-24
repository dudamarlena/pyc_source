# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/model/space/node.py
# Compiled at: 2019-09-05 10:20:47
# Size of source mod 2**32: 7816 bytes
from tensorflow import keras
from core.exceptions import DeephyperRuntimeError
from op.basic import Operation

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
        if isinstance(op, keras.layers.Layer):
            return Operation(op)
        raise RuntimeError(f"Can't add this operation '{op.__name__}'. An operation should be either of type Operation or keras.layers.Layer when is of type: {type(op)}")


class OperationNode(Node):

    def __init__(self, name='', *args, **kwargs):
        (super().__init__)(args, name=name, **kwargs)

    def create_tensor(self, inputs=None, train=True, seed=None, **kwargs):
        if self._tensor is None:
            if inputs == None:
                try:
                    self._tensor = self.op(train=train, seed=None)
                except TypeError:
                    raise RuntimeError(f'Verify if node: "{self}" has incoming connexions!')

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
        return f"{super().__str__()}(Variable[?])"

    def add_op(self, op):
        self._ops.append(self.verify_operation(op))

    @property
    def num_ops(self):
        return len(self._ops)

    def set_op(self, index):
        self.get_op(index).init(self)

    def get_op(self, index):
        if not 'float' in str(type(index)):
            assert type(index) is int, f"found type is : {type(index)}"
        if 'float' in str(type(index)):
            self._index = self.denormalize(index)
        else:
            if not (0 <= index and index < len(self._ops)):
                raise AssertionError(f"Number of possible operations is: {len(self._ops)}, but index given is: {index} (index starts from 0)!")
            self._index = index
        return self.op

    def denormalize(self, index):
        """Denormalize a normalized index to get an absolute indexes. Useful when you want to compare the number of different search_spaces.

        Args:
            indexes (float|int): a normalized index.

        Returns:
            int: An absolute indexes corresponding to the operation choosen with the relative index of `index`.
        """
        if type(index) is int:
            return index
        if not (0.0 <= index and index <= 1.0):
            raise AssertionError
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
    __doc__ = "A ConstantNode represents a node with a fixed operation. It means the agent will not make any new decision for this node. The common use case for this node is to add a tensor in the graph.\n\n    >>> import tensorflow as tf\n    >>> from deephyper.search.nas.model.space.node import ConstantNode\n    >>> from deephyper.search.nas.model.space.op.op1d import Dense\n    >>> cnode = ConstantNode(op=Dense(units=100, activation=tf.nn.relu), name='CNode1')\n    >>> cnode.op\n    Dense_100_relu\n\n    Args:\n        op (Operation, optional): [description]. Defaults to None.\n        name (str, optional): [description]. Defaults to ''.\n    "

    def __init__(self, op=None, name='', *args, **kwargs):
        super().__init__(name=name)
        if op is not None:
            op = self.verify_operation(op)
            op.init(self)
        self._op = op

    def set_op(self, op):
        op = self.verify_operation(op)
        op.init(self)
        self._op = op

    def __str__(self):
        return f"{super().__str__()}(Constant[{str(self.op)}])"

    @property
    def op(self):
        return self._op


class MirrorNode(OperationNode):
    __doc__ = 'A MirrorNode is a node which reuse an other, it enable the reuse of keras layers. This node will not add operations to choose.\n\n    Args:\n        node (Node): The targeted node to mirror.\n\n    >>> from deephyper.search.nas.model.space.node import VariableNode, MirrorNode\n    >>> from deephyper.search.nas.model.space.op.op1d import Dense\n    >>> vnode = VariableNode()\n    >>> vnode.add_op(Dense(10))\n    >>> vnode.add_op(Dense(20))\n    >>> mnode = MirrorNode(vnode)\n    >>> vnode.set_op(0)\n    >>> vnode.op\n    Dense_10\n    >>> mnode.op\n    Dense_10\n    '

    def __init__(self, node):
        super().__init__(name=f"Mirror[{str(node)}]")
        self._node = node

    @property
    def op(self):
        return self._node.op


class MimeNode(OperationNode):
    __doc__ = 'A MimeNode is a node which reuse an the choice made for an VariableNode, it enable the definition of a Cell based search_space. This node reuse the operation from the mimed VariableNode but only the choice made.\n\n    Args:\n        node (VariableNode): the VariableNode to mime.\n\n    >>> from deephyper.search.nas.model.space.node import VariableNode, MimeNode\n    >>> from deephyper.search.nas.model.space.op.op1d import Dense\n    >>> vnode = VariableNode()\n    >>> vnode.add_op(Dense(10))\n    >>> vnode.add_op(Dense(20))\n    >>> mnode = MimeNode(vnode)\n    >>> mnode.add_op(Dense(30))\n    >>> mnode.add_op(Dense(40))\n    >>> vnode.set_op(0)\n    >>> vnode.op\n    Dense_10\n    >>> mnode.op\n    Dense_30\n    '

    def __init__(self, node):
        super().__init__(name=f"Mime[{str(node)}]")
        self.node = node
        self._ops = list()

    def add_op(self, op):
        self._ops.append(self.verify_operation(op))

    @property
    def num_ops(self):
        return len(self._ops)

    @property
    def op(self):
        if self.num_ops != self.node.num_ops:
            raise DeephyperRuntimeError(f"{str(self)} and {str(self.node)} should have the same number of opertions, when {str(self)} has {self.num_ops} and {str(self.node)} has {self.node.num_ops}!")
        else:
            return self._ops[self.node._index]

    @property
    def ops(self):
        return self._ops