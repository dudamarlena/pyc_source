# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/autograd/variable.py
# Compiled at: 2018-12-12 06:22:23
# Size of source mod 2**32: 16040 bytes
import numpy as np
from autograd import utils
import autograd as ad
from autograd.node import Node
from autograd import config

class Variable:
    __doc__ = '\n    The variable class is the main class that will carry the information flow : data and gradient\n    A variable has a data attribute, and a gradient one\n    The data attribute is the data contained is this variable, for instance:\n        x=Variable(1)\n        y=ad.sin(x)\n        \n        y is a variable and y.data=sin(1)\n        \n    The gradient attribute contains the Jacobian matrix that gathers all the gradient flow\n    from the beginning of the computational graph, until this variable. For instance\n        x=Variable([1,2,-12])\n        \n        x.gradient is equal to Identity(3)\n        \n        y=ad.sin(x)\n        \n        y.gradient is the square matrix with diagonal elements (cos(1), cos(2), cos(-12))\n        \n        z=x.power(2)\n        \n        z.gradient is the square matrix with diagonal elements of (2*cos(1)*1, 2*cos(2)*1, 2*cos(-12)*1)\n        the *1 term corresponds to the gradient of the variable x\n    '

    def __init__(self, data, gradient=None, constant=False, input_node=True):
        self.data = utils.data_2_numpy(data)
        self.input_node = input_node
        data_shape = utils.get_shape(data)
        if ad.mode == 'forward':
            if type(gradient) != type(None):
                self.gradient = utils.data_2_numpy(gradient)
            else:
                if len(data_shape) > 2:
                    print('dealing with high order tensors as input. not handled yet')
                    raise NotImplementedError
                if len(data_shape) == 2:
                    if data_shape[0] != data_shape[1]:
                        print('dealing with non square matrices, not handled yet')
                        raise NotImplementedError
                lenght = data_shape[0]
                self.gradient = np.eye(lenght)
            if input_node == True:
                ad.c_graph.input_shapes = [
                 self.data.shape[0]]
        else:
            self.gradient = None
        if constant == False:
            self.node = Node(output_dim=(self.data.shape[0]))
            config.list_of_nodes += [self.node]
            if input_node == True:
                ad.c_graph.input_node = [self.node]
                config.list_of_nodes = [
                 self.node]

    @classmethod
    def multi_variables(self, *args, input_node=True):
        """
        embed all the data in the *args into one big variable, and then output the small variables 
        corresponding to each data provided
        
        EX : 
            data1=[1,2,3]
            data2=3
            data3=[5,6,76,7,7,8]
            
            we will have
            var1, var2, var3 = multi_variables(data1, data2, data3)
            
            who will be variables with var1.data=data1, etc. 
        """
        ad.c_graph.input_shapes = []
        big_data = None
        for data in args:
            processed_data = utils.data_2_numpy(data)
            if not len(processed_data.shape) == 1:
                if not processed_data.shape[1] == 1:
                    raise AssertionError('can only deal with vector inputs')
            ad.c_graph.input_shapes += [processed_data.shape[0]]
            if big_data is None:
                big_data = processed_data
            else:
                big_data = np.concatenate([big_data, processed_data], axis=0)

        big_variable = self(big_data, input_node=False)
        output_variables = []
        current_index = 0
        for shape in ad.c_graph.input_shapes:
            output_variables += [big_variable[current_index:current_index + shape]]
            current_index += shape

        if ad.mode == 'reverse':
            if input_node == True:
                ad.c_graph.input_node = [var.node for var in output_variables]
                config.list_of_nodes = [var.node for var in output_variables]
        return output_variables

    def compute_gradients(self):
        """
        in forward mode: 
            if the comp. graph has only one input node return the gradient w.r to this node
            otherwise, return the list of gradients with respect to all the input nodes
            
        in the reverse mode:
            same thing
        """
        if ad.mode == 'forward':
            if len(ad.c_graph.input_shapes) == 1:
                return self.gradient
            else:
                output = []
                current_index = 0
                for shape in ad.c_graph.input_shapes:
                    output += [self.gradient[:, current_index:current_index + shape]]
                    current_index += shape

                self.gradient = output
                return output
        else:
            self.backward()
            output_gradients = [inp_node.gradient for inp_node in ad.c_graph.input_node]
            if len(output_gradients) == 1:
                self.gradient = output_gradients[0]
                return self.gradient
            else:
                self.gradient = output_gradients
                return self.gradient

    def set_data(self, data):
        """
        set the data of a Variable. the new data needs to have the same shape as the previous data
        stored in this variable
        """
        new_shape = utils.get_shape(data)
        assert new_shape == self.data.shape, 'trying to set data with inconsistent shapes! previous shape : {} -- shape provided {}'.format(self.data.shape, new_shape)
        self.data = data

    def set_gradient(self, gradient):
        """
        set the gradient of a Variable. the new gradient needs to have the same shape as the previous
        gradient stored in this variable
        """
        new_shape = utils.get_shape(gradient)
        if ad.mode == 'forward':
            assert new_shape == self.gradient.shape, 'trying to set data with inconsistent shapes! previous shape : {} -- shape provided {}'.format(self.gradient.shape, new_shape)
        else:
            print('in reverse mode, you cannot modify in place the gradients of the variables')
        self.gradient = gradient

    def __str__(self):
        """
        nice print to see what is in the variable
        """
        return 'data : {} \ngrad : {}'.format(self.data, self.gradient)

    def scalar_to_variable(self, other):
        const_vec = [
         other] * self.data.shape[0]
        if ad.mode == 'forward':
            return Constant(const_vec, gradient=(np.zeros(self.gradient.shape)))
        else:
            return Constant(const_vec)

    def backward(self):
        """
        implement reverse AD, return the gradient of current variable w.r. input Variables
        input variables are the ones who don't have any childrens
        
        we are referencing the function here sot hat the user can do var.backward()
        instead of var.node.backward()
        """
        ad.c_graph.output_node = self.node
        ad.c_graph.define_path(self.node)
        self.node.backward()

    def __add__(self, other):
        """
        overload addition
        """
        if 'add' not in dir():
            from autograd.blocks.operations import add
            add = add()
        if not isinstance(other, Variable):
            other = self.scalar_to_variable(other)
        return add(self, other)

    def __radd__(self, other):
        """
        overload right-addition
        """
        if 'add' not in dir():
            from autograd.blocks.operations import add
            add = add()
        if not isinstance(other, Variable):
            other = self.scalar_to_variable(other)
        return add(self, other)

    def __sub__(self, other):
        """
        overload subtraction
        """
        if 'substract' not in dir():
            from autograd.blocks.operations import subtract
            subtract = subtract()
        if not isinstance(other, Variable):
            other = self.scalar_to_variable(other)
        return subtract(self, other)

    def __rsub__(self, other):
        """
        overload right-subtraction (order matters)
        """
        if 'substract' not in dir():
            from autograd.blocks.operations import subtract
            subtract = subtract()
        if not isinstance(other, Variable):
            other = self.scalar_to_variable(other)
        return subtract(other, self)

    def __mul__(self, other):
        """
        overload element-wise multiplication
        """
        if 'multiply' not in dir():
            from autograd.blocks.operations import multiply
            multiply = multiply()
        if not isinstance(other, Variable):
            other = self.scalar_to_variable(other)
        return multiply(self, other)

    def __rmul__(self, other):
        """
        overload element-wise multiplication
        """
        if 'multiply' not in dir():
            from autograd.blocks.operations import multiply
            multiply = multiply()
        if not isinstance(other, Variable):
            other = self.scalar_to_variable(other)
        return multiply(self, other)

    def __truediv__(self, other):
        """
        overload division
        """
        if 'divide' not in dir():
            from autograd.blocks.operations import divide
            divide = divide()
        if not isinstance(other, Variable):
            other = self.scalar_to_variable(other)
        return divide(self, other)

    def __rtruediv__(self, other):
        """
        overload right-division (order matters)
        """
        if 'divide' not in dir():
            from autograd.blocks.operations import divide
            divide = divide()
        if not isinstance(other, Variable):
            other = self.scalar_to_variable(other)
        return divide(other, self)

    def __pow__(self, other):
        """
        overload power
        """
        if 'power_const_exponent' not in dir():
            from autograd.blocks.operations import power_const_exponent
            power_const_exponent = power_const_exponent()
        if 'power' not in dir():
            from autograd.blocks.operations import power
            power = power()
        if type(other) == int or type(other) == float:
            return power_const_exponent(self, power_exponent=other)
        else:
            return power(self, other)

    def __rpow__(self, other):
        if 'power_const_base' not in dir():
            from autograd.blocks.operations import power_const_base
            power_const_base = power_const_base()
        return power_const_base(self, base=other)

    def __neg__(self):
        """
        implementing the - unary overloading
        """
        return -1 * self

    def __getitem__(self, key):
        """
        overload extracting elements from a vector
        works for both integer and slice
        """
        if 'extract' not in dir():
            from autograd.blocks.operations import extract
            extract = extract()
        return extract(self, key=key)

    def __eq__(self, other):
        """
        overload equals dunder method, only on the data
        """
        assert type(self) == type(other), 'trying to compare two different objects {} and {}'.format(type(self), type(other))
        return np.equal(self.data, other.data)

    def __ne__(self, other):
        """
        overload not equal dunder method
        """
        return self.data != other.data

    def __lt__(self, other):
        """
        overload less than dunder method, only on the data
        """
        return self.data < other.data

    def __le__(self, other):
        """
        overload less than or equal dunder method, only on the data
        """
        return self.data <= other.data

    def __gt__(self, other):
        """
        overload greater than dunder method, only on the data
        """
        return self.data > other.data

    def __ge__(self, other):
        """
        overload greater than or equal dunder method, only on the data
        """
        return self.data >= other.data


class Constant(Variable):
    __doc__ = '\n    clean way to embed scalar values, or constants.\n    '

    def __init__(self, data, gradient=None, constant=True, input_node=False):
        super().__init__(data=data, gradient=gradient, constant=constant, input_node=input_node)


if __name__ == '__main__':
    x = Variable([2, 3, 4])
    print(x.data)
    print(x.gradient)
    new_data = np.ones(3)
    x.set_data(new_data)
    print(x.data)
    new_grad = 43 * np.eye(3)
    x.set_gradient(new_grad)
    print(x)
    print('==== Operators ====')
    print(x + 3)
    print(3 - x)
    print(x / 3)
    print(3 * x)
    print(x + x)
    print(x - x)
    print(x * x)
    print(x / x)
    print(x ** 2)