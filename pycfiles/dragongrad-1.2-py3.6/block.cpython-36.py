# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/autograd/blocks/block.py
# Compiled at: 2018-12-12 06:22:23
# Size of source mod 2**32: 5695 bytes
import numpy as np, autograd as ad

class Block:
    __doc__ = '\n    main class for the blocks of the AD package. The several blocks will be of several types\n    We have two types of block : main and simple\n    the simple blocks will represent vectorized functions\n    \n    For instance :\n        sin(.) is a simple block as it applies sin on all the data of the input variable\n\n        sum_elts(.,.) is a main block as it processes all the data of the input vector in a specific way\n\n    \n    '

    def data_fn(self, *args, **kwargs):
        """
        function to apply to the input Variable.
        for instance :
            sin.data_fn(x) will return sin(x)
        """
        raise NotImplementedError

    def get_jacobians(self, *args, **kwargs):
        """
        get the jacobians of the current block, evaluated at the input.data point

        we specify jacobianS as we want to have the jacobian of the ouput of the block with respect
        to each of the inputs
        """
        raise NotImplementedError

    def gradient_forward(self, *args, **kwargs):
        """
        function implementing the forward pass of the gradient.

        Let's consider a computational graph which transforms
        x_0 --> x_1 --> x_2 --> x_3 --> y
        let's call the output of that block y, then the output of
        gradient_forward(x3), will contain the jacobian of the function x_0 --> y

        this function is in charge of pushing the gradients forward, it will combine the
        previously computed gradients to the derivative of this block_function

        this function will depend on wether this is a simple block or a double block.
        for instance :
            sin.gradient_forward(x) will return grad(x) * cos(x)

            multiply(x,y) will return : grad(x)*y + x*grad(y)
        """
        input_grad = np.concatenate([var.gradient for var in args], axis=0)
        jacobians = (self.get_jacobians)(*args, **kwargs)
        jacobian = np.concatenate([jacob for jacob in jacobians], axis=1)
        new_grad = np.matmul(jacobian, input_grad)
        return new_grad

    def __call__(self, *args, **kwargs):
        """
        applies the forward pass of the data and the gradient.
        returns a new variable with the updated information on data and gradient.
        """
        if 'Variable' not in dir():
            from autograd.variable import Variable
        else:
            new_data = (self.data_fn)(*args, **kwargs)
            if ad.mode == 'forward':
                new_grad = (self.gradient_forward)(*args, **kwargs)
                return Variable(new_data, new_grad, input_node=False)
            if ad.mode == 'reverse':
                input_variables = []
                variables_indexes = []
                for index, arg in enumerate(args):
                    if type(arg) == Variable:
                        input_variables += [arg]
                        variables_indexes += [index]

                children_nodes = [var.node for var in input_variables]
                children_jacs = (self.get_jacobians)(*args, **kwargs)
                outputVariable = Variable(new_data, input_node=False)
                for index, i in enumerate(variables_indexes):
                    outputVariable.node.childrens += [{'node':children_nodes[index],  'jacobian':children_jacs[i]}]

                return outputVariable
        print('unknown mode : ', ad.mode)


class SimpleBlock(Block):
    __doc__ = '\n    this block is meant to implement one-variable functions that have been vectorized :\n        sin(vector) is the vector of coordinates (sin(vector[i]))\n\n    For this, these functions are functions from Rn to Rn and they have a Jacobian which is\n    a square matrix, with elements only on the diagonal\n    '

    def gradient_fn(self, *args, **kwargs):
        """
        function implementing the gradient of data_fn, when it is easy to express
        for instance :
            sin.gradient_fn(x) will return cos(x)
        """
        raise NotImplementedError

    def get_jacobians(self, *args, **kwargs):
        """
        get the Jacobian matrix of the simple block. It is a diagonal matrix easy to build from the
        derivative function of the simpleBlock
        """
        elts = (self.gradient_fn)(*args, **kwargs)
        jacobian = np.diag(elts)
        return [jacobian]