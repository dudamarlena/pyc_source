# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\backend\numpy_backend.py
# Compiled at: 2020-02-14 03:18:20
# Size of source mod 2**32: 82069 bytes
"""Contains wrapper classes for different backends that are needed by the parser module.

A new backend needs to implement the following methods

Methods
-------
__init__
run
add_var
add_op
add_layer

Currently supported backends:
- Numpy: NumpyBackend.
- Tensorflow: TensorflowBackend.

"""
import time
from typing import Optional, Dict, List, Union, Any, Callable
import numpy as np
from copy import deepcopy
import os, sys
from shutil import rmtree
import warnings
from .funcs import *
from .parser import replace

class NumpyVar(np.ndarray):
    __doc__ = 'Base class for adding variables to the PyRates compute graph. Creates a numpy array with additional attributes\n    for variable identification/retrieval from graph. Should be used as parent class for custom variable classes.\n\n    Parameters\n    ----------\n    vtype\n        Type of the variable. Can be either `constant` or `state_variable`. Constant variables are necessary to perform\n        certain graph optimizations previous to run time.\n    backend\n        Instance of the backend in use.\n    dtype\n        Data-type of the variable. For valid data-types, check the documentation of the backend in use.\n    shape\n        Shape of the variable.\n    value\n        Value of the variable. If scalar, please provide the shape in addition.\n\n    Returns\n    -------\n    NumpyVar\n        Instance of NumpyVar.\n    '

    def __new__(cls, vtype: str, backend: Any, name: str, dtype: Optional[str]=None, shape: Optional[tuple]=None, value: Optional[Any]=None, squeeze: bool=True):
        """Creates new instance of NumpyVar.
        """
        if all([arg is None for arg in [shape, value, dtype]]):
            raise ValueError('Either `value` or `shape` and `dtype` need to be provided')
        else:
            if not shape:
                shape = value.shape if hasattr(value, 'shape') else np.shape(value)
            if dtype or hasattr(value, 'dtype'):
                dtype = value.dtype
            else:
                try:
                    dtype = np.dtype(value)
                except TypeError:
                    dtype = type(value)

                dtype = dtype.name if hasattr(dtype, 'name') else str(dtype)
                dtype = dtype.name if hasattr(dtype, 'name') else str(dtype)
                if dtype in backend.dtypes:
                    dtype = backend.dtypes[dtype]
                else:
                    for dtype_tmp in backend.dtypes:
                        if dtype_tmp in dtype:
                            dtype = backend.dtypes[dtype_tmp]
                            break
                    else:
                        dtype = backend._float_def
                        warnings.warn(f"WARNING! Unknown data type of variable {name}: {dtype}. Datatype will be set to default type: {dtype}.")

                if vtype == 'state_var':
                    if 1 in tuple(shape):
                        if squeeze:
                            idx = tuple(shape).index(1)
                            shape = list(shape)
                            shape.pop(idx)
                            shape = tuple(shape)
                    value = cls._get_value(value, dtype, shape)
                    if squeeze:
                        value = cls.squeeze(value)
                    obj = cls._get_var(value, name, dtype)
                    obj.short_name = name.split('/')[(-1)]
                    obj.name = hasattr(obj, 'name') or name
                else:
                    name = obj.name
        obj.vtype = vtype
        return (
         obj, name)

    def numpy(self):
        """Returns current value of NumpyVar.
        """
        try:
            return self[:]
        except IndexError:
            return self

    @staticmethod
    def _get_value(value, dtype, shape):
        """Defines initial value of variable.
        """
        if value is None:
            return np.zeros(shape=shape, dtype=dtype)
        else:
            if not hasattr(value, 'shape'):
                if type(value) is list:
                    return np.zeros(shape=shape, dtype=dtype) + np.asarray(value, dtype=dtype).reshape(shape)
                else:
                    return np.zeros(shape=shape, dtype=dtype) + value
            else:
                if shape:
                    if value.shape == shape:
                        return value
                    else:
                        if sum(shape) < sum(value.shape):
                            return value.squeeze()
                        idx = ','.join(('None' if s == 1 else ':') for s in shape)
                        return eval(f"value[{idx}]")
                else:
                    return np.asarray(value, dtype=dtype)

    @staticmethod
    def squeeze(var, axis=None):
        return var.squeeze(axis)

    @classmethod
    def _get_var(cls, value, name, dtype):
        """Creates new numpy array from NumpyVar.
        """
        return np.array(value).view(cls)

    def __deepcopy__(self, memodict={}):
        obj = super().__deepcopy__(memodict)
        if not hasattr(obj, 'name'):
            obj.name = self.name
        if not hasattr(obj, 'short_name'):
            obj.short_name = self.short_name
        if not hasattr(obj, 'vtype'):
            obj.vtype = self.vtype
        return obj

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(str(self))


class PyRatesOp:
    __doc__ = 'Base class for adding operations on variables to the PyRates compute graph. Should be used as parent class for\n    custom operator classes.\n\n    Parameters\n    ----------\n    op\n        Call-signature of the operation/function.\n    short_name\n        Name of the operation within the equations.\n    name\n        Name of the operation/function.\n    args\n        Arguments to the function.\n\n    '

    def __init__(self, op: str, short_name: str, name, *args, **kwargs) -> None:
        """Instantiates PyRates operator.
        """
        self.op = op
        self.short_name = short_name if short_name in name else name.split('/')[(-1)]
        self.name = name
        self._op_dict = (self.generate_op_str)(op, args, **kwargs)
        self.value = self._op_dict['value']
        self.arg_names, args = self._get_unique_args(self._op_dict['arg_names'], self._op_dict['args'])
        self.input_ops = self._op_dict['input_ops']
        self.is_constant = self._op_dict['is_constant']
        self.shape = ()
        self.dtype = 'float'
        self._callable = lambda x: x
        self.args = ()
        self.build_op(args)

    def eval(self):
        """Evaluates the return values of the PyRates operation.
        """
        result = (self._callable)(*self.args)
        self._check_numerics(result, self.name)
        return result

    def _generate_func(self):
        """Generates a function from operator value and arguments"""
        func_dict = {}
        func = CodeGen()
        func.add_code_line(f"def {self.short_name}(")
        for arg in self._op_dict['arg_names']:
            func.add_code_line(f"{arg},")

        if len(self._op_dict['arg_names']) > 0:
            func.code[-1] = func.code[(-1)][:-1]
        func.add_code_line('):')
        func.add_linebreak()
        func.add_indent()
        func.add_code_line(f"return {self._op_dict['value']}")
        exec(func.generate(), globals(), func_dict)
        return func_dict

    def build_op(self, args):
        """Builds the function of the operator, tests its functionality and stores shape and data-type of the result
        on the instance.
        """
        func_dict = self._generate_func()
        self._callable = func_dict.pop(self.short_name)
        self.args = self._deepcopy(args)
        result = self.eval() if 'no_op' not in self.short_name else self.args[0]
        self.args = args
        self.shape = result.shape if hasattr(result, 'shape') else ()
        self.dtype = result.dtype if hasattr(result, 'dtype') else type(result)

    @classmethod
    def generate_op_str(cls, op, args, **kwargs):
        """Generates the function string, call signature etc.
        """
        results = {'value':None, 
         'args':[],  'arg_names':[],  'is_constant':False,  'input_ops':[]}
        if op == 'no_op':
            if hasattr(args[0], 'short_name'):
                val = args[0].short_name
                arg = [args[0]]
                name = [args[0].short_name]
            else:
                val = str(args[0])
                arg = []
                name = []
            results['value'] = val
            results['args'] = arg
            results['arg_names'] = name
            return results
        else:
            results, results_args, results_arg_names, n_vars = cls._process_args(args, results)
            eval_gen = CodeGen()
            if op in '+-**/*^%<>==>=<=':
                if len(args) == 2:
                    arg1 = cls._arg_to_str(op, args[0], results_args[0], results_arg_names[0])
                    arg2 = cls._arg_to_str(op, args[1], results_args[1], results_arg_names[1])
                    eval_gen.add_code_line(f"{arg1} {op} {arg2}")
                    func_call = False
            else:
                func_call = True
                eval_gen.add_code_line(f"{op}(")
            for i, (key, arg) in enumerate(zip(results_arg_names, results_args)):
                if key != '__no_name__':
                    if type(arg) is str:
                        if func_call:
                            if arg is '(':
                                eval_gen.add_code_line((f"{arg}"))
                            else:
                                eval_gen.add_code_line(f"{arg},")
                            idx = cls._index(results['args'], arg)
                            results['args'].pop(idx)
                            results['arg_names'].pop(idx)
                        elif type(arg) is dict:
                            if func_call:
                                eval_gen.add_code_line(f"{arg['value']},")
                            if func_call:
                                eval_gen.add_code_line(f"{key},")
                    else:
                        if func_call:
                            eval_gen.add_code_line(f"{arg},")
                        if key in results['arg_names']:
                            idx = cls._index(results['arg_names'], key)
                            results['args'].pop(idx)
                            results['arg_names'].pop(idx)

            if func_call:
                eval_gen.code[-1] = eval_gen.code[(-1)][:-1]
                eval_gen.add_code_line(')')
            results['value'] = eval_gen.generate()
            if n_vars == 0:
                results['is_constant'] = True
            return results

    @classmethod
    def _process_args(cls, args, results, constants_to_num=True):
        """Parses arguments to function into argument names that are added to the function call and argument values
        that can used to set up the return line of the function.
        """
        results_args = []
        results_arg_names = []
        n_vars = 0
        for idx, arg in enumerate(args):
            if PyRatesOp.__subclasscheck__(type(arg)):
                results['input_ops'].append(arg.name)
                pop_indices = []
                for arg_tmp in arg.arg_names:
                    if arg_tmp in results['arg_names']:
                        pop_indices.append(arg.arg_names.index(arg_tmp))

                new_args = arg.args.copy()
                new_arg_names = arg.arg_names.copy()
                for i, pop_idx in enumerate(pop_indices):
                    new_args.pop(pop_idx - i)
                    new_arg_names.pop(pop_idx - i)

                results_args.append({'args':new_args,  'value':arg.lhs if 'assign' in arg.short_name else arg.value,  'arg_names':new_arg_names})
                results_arg_names.append(arg.short_name)
                results['args'] += new_args
                results['arg_names'] += new_arg_names
                n_vars += 1
            elif hasattr(arg, 'vtype'):
                if arg.vtype is 'constant':
                    if not arg.shape:
                        if constants_to_num:
                            arg_name = '__no_name__'
                            arg_value = arg.numpy() if hasattr(arg, 'numpy') else arg
                else:
                    arg_name = arg.short_name
                    arg_value = arg
                    n_vars += 1
                results_args.append(arg_value)
                results_arg_names.append(arg_name)
                results['args'].append(arg_value)
                results['arg_names'].append(arg_name)
            elif type(arg) is tuple or type(arg) is list:
                tuple_begin = '('
                results_args.append(tuple_begin)
                results_arg_names.append(tuple_begin)
                results['args'].append(tuple_begin)
                results['arg_names'].append(tuple_begin)
                results, results_args_tmp, results_arg_names_tmp, n_vars_tmp = cls._process_args(arg, results)
                results_args += results_args_tmp
                results_arg_names += results_arg_names_tmp
                n_vars += n_vars_tmp
                tuple_end = ')'
                results_args.append(tuple_end)
                results_arg_names.append(tuple_end)
                results['args'].append(tuple_end)
                results['arg_names'].append(tuple_end)
            else:
                arg_name = '__no_name__'
                results_args.append(arg)
                results_arg_names.append(arg_name)
                results['args'].append(arg)
                results['arg_names'].append(arg_name)

        return (
         results, results_args, results_arg_names, n_vars)

    @staticmethod
    def _get_unique_args(arg_names, args):
        arg_names_unique = np.unique(arg_names)
        for name in arg_names_unique:
            n = arg_names.count(name)
            while n > 1:
                i0 = arg_names.index(name) + 1
                i1 = arg_names[i0:].index(name)
                arg_names.pop(i0 + i1)
                args.pop(i0 + i1)
                n -= 1

        return (
         arg_names, args)

    @staticmethod
    def _check_numerics(vals, name):
        """Checks whether function evaluation leads to any NaNs or infinite values.
        """
        check = []
        try:
            if hasattr(vals, 'shape'):
                vals = vals.numpy().flatten() if hasattr(vals, 'numpy') else vals.flatten()
            else:
                vals = [
                 vals]
            for val in vals:
                check.append(np.isnan(val) or np.isneginf(val))

        except TypeError:
            check.append(np.isnan(vals) or np.isneginf(vals))

        if any(check):
            raise ValueError(f"Result of operation ({name}) contains NaNs or infinite values.")

    @staticmethod
    def _get_arg(arg: Any, arg_reduced: Any, key: str) -> str:
        if key == '__no_name__':
            if arg_reduced > 0:
                return (f"{arg_reduced}")
            return f"({arg_reduced})"
        else:
            if PyRatesOp.__subclasscheck__(type(arg)):
                return (f"{arg.value}")
            return key

    @classmethod
    def _arg_to_str(cls, op: str, arg, arg_reduced, key: str) -> str:
        op_orders = [['+', '-'],
         [
          '*'],
         [
          '/', '%', '>', '<', '==', '<=', '>=', '!='],
         [
          '^', '**']]
        op_order = 0
        for i, ops in enumerate(op_orders):
            if op in ops:
                op_order = i + 1
                break

        arg_order = 5
        if hasattr(arg, 'op'):
            for i, ops in enumerate(op_orders):
                if arg.op in ops:
                    arg_order = i + 1
                    break

        arg_str = cls._get_arg(arg, arg_reduced, key)
        if op_order > arg_order or op_order == arg_order and op_order >= 3:
            if not (arg_str[0] == '(' and arg_str[(-1)] == ')'):
                return f"({arg_str})"
        return arg_str

    @staticmethod
    def _deepcopy(x):
        return deepcopy(x)

    @staticmethod
    def _index(x, y):
        return x.index(y)


class PyRatesAssignOp(PyRatesOp):
    __doc__ = 'Sub-class for assign operations. Typically, an update (2. entry in args) is assigned to a PyRates variable\n    (1. entry in args). An index can be provided as third argument to target certain entries of the variable.\n    '

    def __init__(self, op, short_name, name, *args, **kwargs):
        (super().__init__)(op, short_name, name, *args, **kwargs)
        self.lhs = self._op_dict.pop('lhs')
        self.rhs = self._op_dict.pop('rhs')

    def _generate_func(self):
        func_dict = {}
        func = CodeGen()
        func.add_code_line(f"def {self.short_name}(")
        for arg in self._op_dict['arg_names']:
            func.add_code_line(f"{arg},")

        func.code[-1] = func.code[(-1)][:-1]
        func.add_code_line('):')
        func.add_linebreak()
        func.add_indent()
        func.add_code_line((f"{self._op_dict['value']}"))
        func.add_linebreak()
        func.add_code_line(f"return {self._op_dict['lhs']}")
        exec(func.generate(), globals(), func_dict)
        return func_dict

    @classmethod
    def generate_op_str(cls, op, args, **kwargs):
        """Generates the assign function string, call signature etc.
        """
        results = {'value':None, 
         'args':[],  'arg_names':[],  'is_constant':False,  'input_ops':[],  'lhs':None}
        results_args = []
        results_arg_names = []
        var, upd = args[0:2]
        if len(args) > 2:
            var_idx, results_args, results_arg_names = (cls._extract_var_idx)(op, args, results_args, results_arg_names, **kwargs)
        else:
            var_idx = ''
        var_key = var.short_name if 'assign' not in var.short_name else '__no_name__'
        var_pos = len(results_args)
        results_args.append(var if 'assign' not in var.short_name else {'value': var.lhs})
        results_arg_names.append(var_key)
        if hasattr(upd, 'vtype') and upd.vtype == 'constant' and not upd.shape:
            upd_key = '__no_name__'
            if not PyRatesOp.__subclasscheck__(type(upd)):
                upd = {'value': upd}
        else:
            upd_key = upd.short_name
        upd_pos = len(results_args)
        results_args.append(upd)
        results_arg_names.append(upd_key)
        for idx, (key, arg) in enumerate(zip(results_arg_names, results_args)):
            if PyRatesOp.__subclasscheck__(type(arg)):
                pop_indices = []
                for arg_tmp in arg.arg_names:
                    if arg_tmp in results['arg_names']:
                        pop_indices.append(arg.arg_names.index(arg_tmp))

                new_args = arg.args.copy()
                new_arg_names = arg.arg_names.copy()
                for i, pop_idx in enumerate(pop_indices):
                    new_args.pop(pop_idx - i)
                    new_arg_names.pop(pop_idx - i)

                results_args[idx] = {'args':new_args, 
                 'value':arg.value,  'arg_names':new_arg_names}
                results['input_ops'].append(arg.name)
                results['args'] += new_args
                results['arg_names'] += new_arg_names
            elif key != '__no_name__':
                results['args'].append(arg)
                results['arg_names'].append(key)

        var_str = results_args[var_pos]['value'] if type(results_args[var_pos]) is dict else var_key
        upd_str = results_args[upd_pos]['value'] if type(results_args[upd_pos]) is dict else upd_key
        if op in ('=', '+=', '-=', '*=', '/='):
            assign_line = f"{var_str}{var_idx} {op} {upd_str}"
        else:
            if 'scatter' in op:
                scatter_into_first_dim = args[(-1)]
                if len(args) > 3:
                    if scatter_into_first_dim:
                        assign_line = f"{var_str}.{op}([{var_idx}], [{upd_str}])"
                else:
                    assign_line = f"{var_str}.{op}({var_idx}{upd_str})"
            else:
                assign_line = f"{var_str}{var_idx}.{op}({upd_str})"
        results['value'] = assign_line
        results['lhs'] = var_str
        results['rhs'] = upd_str
        return results

    @classmethod
    def _extract_var_idx(cls, op, args, results_args, results_arg_names, idx_l='[', idx_r=']'):
        if hasattr(args[2], 'vtype'):
            key = args[2].short_name
            if hasattr(args[2], 'value'):
                var_idx = f"{idx_l}{args[2].value}{idx_r}"
            else:
                var_idx = f"{idx_l}{key}{idx_r}"
        elif type(args[2]) is str:
            if len(args) > 3:
                key = args[3].short_name
                var_idx = f"{idx_l}{args[2]}{idx_r}"
                var_idx = var_idx.replace(args[3].short_name, key)
        else:
            var_idx = f"{idx_l}{args[2]}{idx_r}"
            key = '__no_name__'
        if type(args[2]) is str:
            if len(args) > 3:
                results_args.append(args[3])
        else:
            results_args.append(args[2])
        results_arg_names.append(key)
        return (
         var_idx, results_args, results_arg_names)


class PyRatesIndexOp(PyRatesOp):
    __doc__ = 'Sub-class for indexing operations. Typically, an index is provided (2. entry in args) indicating which values to\n     extract from a variable (1. entry in args).\n    '

    @classmethod
    def generate_op_str(cls, op, args, idx_l='[', idx_r=']'):
        """Generates the index function string, call signature etc.
        """
        results = {'value':None, 
         'args':[],  'arg_names':[],  'is_constant':False,  'shape':(),  'dtype':'float32',  'input_ops':[]}
        var_tmp = args[0]
        n_vars = 0
        if PyRatesOp.__subclasscheck__(type(var_tmp)):
            var = var_tmp.lhs if hasattr(var_tmp, 'lhs') else var_tmp.value
            pop_indices = []
            for arg_tmp in var_tmp.arg_names:
                if arg_tmp in results['arg_names']:
                    pop_indices.append(var_tmp.arg_names.index(arg_tmp))

            new_args = var_tmp.args.copy()
            new_arg_names = var_tmp.arg_names.copy()
            for i, pop_idx in enumerate(pop_indices):
                new_args.pop(pop_idx - i)
                new_arg_names.pop(pop_idx - i)

            results['input_ops'].append(var_tmp.name)
            results['args'] += new_args
            results['arg_names'] += new_arg_names
            n_vars += 1
        else:
            if hasattr(var_tmp, 'vtype'):
                if var_tmp.vtype != 'constant' or var_tmp.shape:
                    var = var_tmp.short_name
                    results['args'].append(var_tmp)
                    results['arg_names'].append(var)
                    n_vars += 1
                else:
                    var = var_tmp.numpy()
            else:
                raise ValueError(f"Variable type for indexing not understood: {var_tmp}. Please consider another form of variable declaration or indexing.")
            idx = args[1]
            if PyRatesOp.__subclasscheck__(type(idx)):
                var_idx = f"{idx_l}{idx.lhs if hasattr(idx, 'lhs') else idx.value}{idx_r}"
                pop_indices = []
                for arg_tmp in idx.arg_names:
                    if arg_tmp in results['arg_names']:
                        pop_indices.append(idx.arg_names.index(arg_tmp))

                new_args = idx.args.copy()
                new_arg_names = idx.arg_names.copy()
                for i, pop_idx in enumerate(pop_indices):
                    new_args.pop(pop_idx - i)
                    new_arg_names.pop(pop_idx - i)

                results['input_ops'].append(idx.name)
                results['args'] += new_args
                results['arg_names'] += new_arg_names
                n_vars += 1
            else:
                if hasattr(idx, 'vtype'):
                    key = idx.short_name
                    if idx.vtype != 'constant' or idx.shape:
                        var_idx = f"{idx_l}{key}{idx_r}"
                        results['args'].append(idx)
                        results['arg_names'].append(key)
                        n_vars += 1
                    else:
                        var_idx = f"{idx_l}{idx.numpy()}{idx_r}"
                else:
                    if type(idx) is str or 'int' in str(type(idx)) or 'float' in str(type(idx)):
                        pop_indices = []
                        for i, arg in enumerate(args[2:]):
                            if hasattr(arg, 'short_name'):
                                if arg.short_name in idx:
                                    if hasattr(arg, 'vtype'):
                                        if arg.vtype == 'constant' and sum(arg.shape) < 2:
                                            idx = replace(idx, arg.short_name, (f"{int(arg)}"))
                                            pop_indices.append(i + 2)
                                if hasattr(arg, 'value'):
                                    idx = replace(idx, arg.short_name, arg.value)
                                    pop_indices.append(i + 2)
                                    results['args'] += arg.args
                                    results['arg_names'] += arg.arg_names

                        var_idx = f"{idx_l}{idx}{idx_r}"
                        args = list(args)
                        for idx in pop_indices[::-1]:
                            args.pop(idx)

                        args = tuple(args)
                    else:
                        if type(idx) in (list, tuple):
                            var_idx = f"{list(idx)}"
                        else:
                            raise ValueError(f"Index type not understood: {idx}. Please consider another form of variable indexing.")
        results, results_args, results_arg_names, n_vars_tmp = cls._process_args(args[2:], results)
        n_vars += n_vars_tmp
        results['value'] = f"{var}{var_idx}"
        if n_vars == 0:
            results['is_constant'] = True
        return results


class NumpyBackend(object):
    __doc__ = "Wrapper to numpy. This class provides an interface to all numpy functionalities that may be accessed via pyrates.\n    All numpy variables and operations will be stored in a layered compute graph that can be executed to evaluate the\n    (dynamic) behavior of the graph.\n\n    Parameters\n    ----------\n    ops\n        Additional operations this backend instance can perform, defined as key-value pairs. The key can then be used in\n        every equation parsed into this backend. The value is a dictionary again, with two keys:\n            1) name - the name of the function/operation (used during code generation)\n            2) call - the call signature of the function including import abbreviations (i.e. `np.add` for numpy's add\n            function)\n    dtypes\n        Additional data-types this backend instance can use, defined as key-value pairs.\n    name\n        Name of the backend instance. Used during code generation to create a recognizable file structure.\n    float_default_type\n        Default float precision. If no data-type is indicated for a particular variable, this will be used.\n    imports\n        Can be used to pass additional import statements that are needed for code generation of the custom functions\n        provided via `ops`. Will be added to the top of each generated code file.\n    build_dir\n        Directory in which pyrates builds will be stored.\n\n    "
    idx_l, idx_r = ('[', ']')
    idx_start = 0

    def __init__(self, ops=None, dtypes=None, name='net_0', float_default_type='float32', imports=None, build_dir=None):
        """Instantiates numpy backend, i.e. a compute graph with numpy operations.
        """
        super().__init__()
        self.ops = {'+':{'name':'numpy_add', 
          'call':'np.add'}, 
         '-':{'name':'numpy_subtract', 
          'call':'np.subtract'}, 
         '*':{'name':'numpy_multiply', 
          'call':'np.multiply'}, 
         '/':{'name':'numpy_divide', 
          'call':'np.divide'}, 
         '%':{'name':'numpy_modulo', 
          'call':'np.mod'}, 
         '^':{'name':'numpy_power', 
          'call':'np.power'}, 
         '**':{'name':'numpy_power_float', 
          'call':'np.float_power'}, 
         '@':{'name':'numpy_dot', 
          'call':'np.dot'}, 
         '.T':{'name':'numpy_transpose', 
          'call':'np.transpose'}, 
         '.I':{'name':'numpy_invert', 
          'call':'np.invert'}, 
         '>':{'name':'numpy_greater', 
          'call':'np.greater'}, 
         '<':{'name':'numpy_less', 
          'call':'np.less'}, 
         '==':{'name':'numpy_equal', 
          'call':'np.equal'}, 
         '!=':{'name':'numpy_not_equal', 
          'call':'np.not_equal'}, 
         '>=':{'name':'numpy_greater_equal', 
          'call':'np.greater_equal'}, 
         '<=':{'name':'numpy_less_equal', 
          'call':'np.less_equal'}, 
         '=':{'name':'assign', 
          'call':'='}, 
         '+=':{'name':'assign_add', 
          'call':'+='}, 
         '-=':{'name':'assign_subtract', 
          'call':'-='}, 
         '*=':{'name':'assign_multiply', 
          'call':'*='}, 
         '/=':{'name':'assign_divide', 
          'call':'/='}, 
         'neg':{'name':'negative', 
          'call':'neg_one'}, 
         'sin':{'name':'numpy_sin', 
          'call':'np.sin'}, 
         'cos':{'name':'numpy_cos', 
          'call':'np.cos'}, 
         'tan':{'name':'numpy_tan', 
          'call':'np.tan'}, 
         'atan':{'name':'numpy_atan', 
          'call':'np.arctan'}, 
         'abs':{'name':'numpy_abs', 
          'call':'np.abs'}, 
         'sqrt':{'name':'numpy_sqrt', 
          'call':'np.sqrt'}, 
         'sq':{'name':'numpy_square', 
          'call':'np.square'}, 
         'exp':{'name':'numpy_exp', 
          'call':'np.exp'}, 
         'max':{'name':'numpy_max', 
          'call':'np.maximum'}, 
         'min':{'name':'numpy_min', 
          'call':'np.minimum'}, 
         'argmax':{'name':'numpy_transpose', 
          'call':'np.argmax'}, 
         'argmin':{'name':'numpy_argmin', 
          'call':'np.argmin'}, 
         'round':{'name':'numpy_round', 
          'call':'np.round'}, 
         'sum':{'name':'numpy_sum', 
          'call':'np.sum'}, 
         'mean':{'name':'numpy_mean', 
          'call':'np.mean'}, 
         'concat':{'name':'numpy_concatenate', 
          'call':'np.concatenate'}, 
         'reshape':{'name':'numpy_reshape', 
          'call':'np.reshape'}, 
         'append':{'name':'numpy_append', 
          'call':'np.append'}, 
         'shape':{'name':'numpy_shape', 
          'call':'np.shape'}, 
         'dtype':{'name':'numpy_dtype', 
          'call':'np.dtype'}, 
         'squeeze':{'name':'numpy_squeeze', 
          'call':'np.squeeze'}, 
         'expand':{'name':'numpy_expand', 
          'call':'np.expand_dims'}, 
         'roll':{'name':'numpy_roll', 
          'call':'np.roll'}, 
         'cast':{'name':'numpy_cast', 
          'call':'np.asarray'}, 
         'randn':{'name':'numpy_randn', 
          'call':'np.randn'}, 
         'ones':{'name':'numpy_ones', 
          'call':'np.ones'}, 
         'zeros':{'name':'numpy_zeros', 
          'call':'np.zeros'}, 
         'range':{'name':'numpy_arange', 
          'call':'np.arange'}, 
         'softmax':{'name':'pyrates_softmax', 
          'call':'pr_softmax'}, 
         'sigmoid':{'name':'pyrates_sigmoid', 
          'call':'pr_sigmoid'}, 
         'tanh':{'name':'numpy_tanh', 
          'call':'np.tanh'}, 
         'index':{'name':'pyrates_index', 
          'call':'pyrates_index'}, 
         'mask':{'name':'pyrates_mask', 
          'call':'pr_mask'}, 
         'group':{'name':'pyrates_group', 
          'call':'pr_group'}, 
         'asarray':{'name':'numpy_asarray', 
          'call':'np.asarray'}, 
         'no_op':{'name':'pyrates_identity', 
          'call':'pr_identity'}, 
         'interpolate':{'name':'pyrates_interpolate', 
          'call':'pr_interp'}, 
         'interpolate_1d':{'name':'pyrates_interpolate_1d', 
          'call':'pr_interp_1d'}, 
         'interpolate_nd':{'name':'pyrates_interpolate_nd', 
          'call':'pr_interp_nd'}}
        if ops:
            self.ops.update(ops)
        self.dtypes = {'float16':np.float16, 
         'float32':np.float32, 
         'float64':np.float64, 
         'int16':np.int16, 
         'int32':np.int32, 
         'int64':np.int64, 
         'uint16':np.uint16, 
         'uint32':np.uint32, 
         'uint64':np.uint64, 
         'complex64':np.complex64, 
         'complex128':np.complex128, 
         'bool':np.bool}
        if dtypes:
            self.dtypes.update(dtypes)
        self.vars = dict()
        self.layers = [[]]
        self.state_vars = []
        self.lhs_vars = []
        self.var_counter = {}
        self.op_counter = {}
        self.layer = 0
        self.op_indices = {}
        self._float_def = self.dtypes[float_default_type]
        self.name = name
        self._base_layer = 0
        self._input_layer_added = False
        self._imports = ['import numpy as np', 'from pyrates.backend.funcs import *']
        if imports:
            for imp in imports:
                if imp not in self._imports:
                    self._imports.append(imp)

        orig_dir = os.getcwd()
        if build_dir:
            os.makedirs(build_dir, exist_ok=True)
        dir_name = f"{build_dir}/pyrates_build" if build_dir else 'pyrates_build'
        try:
            os.mkdir(dir_name)
        except FileExistsError:
            pass
        except FileNotFoundError as e:
            raise e

        os.chdir(dir_name)
        try:
            os.mkdir(self.name)
        except FileExistsError:
            rmtree(self.name)
            os.mkdir(self.name)

        for key in sys.modules.copy():
            if self.name in key:
                del sys.modules[key]

        os.chdir(self.name)
        net_dir = os.getcwd()
        self._build_dir = net_dir
        sys.path.append(net_dir)
        self._build_dir = net_dir
        self._orig_dir = orig_dir

    def run(self, T: float, dt: float, outputs: Optional[dict]=None, inputs: Optional[list]=None, dts: Optional[int]=None, solver: str='euler', out_dir: Optional[str]=None, profile: bool=False, **kwargs) -> tuple:
        """Executes all operations in the backend graph for a given number of steps.

        Parameters
        ----------
        T
            Simulation time.
        dt
            Simulation step size.
        outputs
            Variables in the graph to store the history from.
        inputs
            Extrinsic, time-dependent inputs to graph input variables.
        dts
            Sampling step-size.
        solver
            Type of the numerical solver to use.
        out_dir
            Directory to write the session log into.
        profile
            If true, the total graph execution time will be printed and returned.

        Returns
        -------
        Union[Tuple[Dict[str, tf.Variable]], Tuple[dict, float]]
            If `profile` was requested, a tuple is returned that contains
                1) the results dictionary
                2) the simulation time.
            If not, a tuple containing only the results dictionary is returned which contains a numpy array with results
             for each output key that was provided via `outputs`. This allows to call the run functioon like this:
             `output, *time = run(*args, **kwargs)`

        """
        if not dts:
            dts = dt
        else:
            if out_dir:
                pass
            if profile:
                t0 = time.time()
            continuous = 'scipy' in solver
            t = self.add_input_layer(inputs=inputs, T=T, continuous=continuous)
            decorator = kwargs.pop('decorator', None)
            decorator_kwargs = kwargs.pop('decorator_kwargs', {})
            rhs_func, args, state_vars, var_map = (self.compile)(self._build_dir, decorator=decorator, **decorator_kwargs)
            output_indices = []
            if outputs:
                for out_key, out_vars in outputs.items():
                    for n, (idx, _) in enumerate(out_vars):
                        output_indices.append([i - self.idx_start for i in idx] if type(idx) is list else idx - self.idx_start)
                        outputs[out_key][n][0] = len(output_indices) - 1

            else:
                for i in range(len(self.state_vars)):
                    output_indices.append(i)
                    out_key = self.state_vars[i]
                    if len(self.vars[out_key].shape) > 0:
                        outputs[out_key] = [
                         (
                          i, [f"{out_key}_{j}" for j in range(self.vars[out_key].shape[0])])]
                    else:
                        outputs[out_key] = [
                         (
                          i, [out_key])]

        func_args = self._process_func_args(args, var_map, dt)
        times, results = (self._solve)(rhs_func=rhs_func, func_args=func_args, T=T, dt=dt, dts=dts, t=t, solver=solver, output_indices=output_indices, **kwargs)
        for i, (out_key, out_vars) in enumerate(outputs.items()):
            node_col = []
            for _, node_keys in out_vars:
                node_col += node_keys

            outputs[out_key] = (
             np.asarray(results[i]), node_col)

        if profile:
            sim_time = time.time() - t0
            return (
             outputs, times, sim_time)
        else:
            return (
             outputs, times)

    def add_var(self, vtype: str, name: Optional[str]=None, value: Optional[Any]=None, shape: Optional[Union[(tuple, list, np.shape)]]=None, dtype: Optional[Union[(str, np.dtype)]]=None, **kwargs) -> NumpyVar:
        """Adds a variable to the backend.

        Parameters
        ----------
        vtype
            Variable type. Can be
                - `state_var` for variables that can change over time.
                - `constant` for non-changing variables.
        name
            Name of the variable.
        value
            Value of the variable. Not needed for placeholders.
        shape
            Shape of the variable.
        dtype
            Datatype of the variable.
        kwargs
            Additional keyword arguments.

        Returns
        -------
        PyRatesVar
            Handle for the numpy variable.

        """
        scope = kwargs.pop('scope', None)
        if scope:
            name = f"{scope}/{name}"
        if name in self.vars:
            return self.get_var(name)
        else:
            var, name = self._create_var(vtype=vtype, dtype=dtype, shape=shape, value=value, name=name, squeeze=(kwargs.pop('squeeze', True)))
            if var.short_name in self.var_counter and name not in self.vars:
                rename = True if var.short_name not in ('y', 'y_delta', 't', 'times') else False
                if var.vtype == 'constant':
                    if rename:
                        for var_tmp in self.vars.values():
                            rename = not self._compare_vars(var, var_tmp)
                            if rename:
                                break

                if rename:
                    name_old = var.short_name
                    name_new = f"{name_old}_{self.var_counter[name_old]}"
                    var.short_name = name_new
                    self.var_counter[name_old] += 1
            else:
                self.var_counter[var.short_name] = 0
            self.vars[name] = var
            return var

    def remove_var(self, name: str) -> NumpyVar:
        """Removes variable from backend and returns it.

        Parameters
        ----------
        name
            Variable name.

        Returns
        -------
        NumpyVar

        """
        if name in self.var_counter:
            self.var_counter[name] -= 1
            if self.var_counter[name] < 0:
                self.var_counter.pop(name)
        if name in self.vars:
            return self.vars.pop(name)
        else:
            return

    def add_op(self, op_name: str, *args, **kwargs) -> Union[(PyRatesOp, NumpyVar)]:
        """Add operation to the backend.

        Parameters
        ----------
        op_name
            Key of the operation. Needs to be a key of `backend.ops`.
        args
            Positional arguments to be passed to the operation.
        kwargs
            Keyword arguments to be passed to the operation, except for scope and dependencies, which are
            extracted before.

        Returns
        -------
        Union[PyRatesOp, PyRatesVar]
            Handle for the lambda-numpy function

        """
        scope = kwargs.pop('scope', None)
        name = kwargs.pop('name', None)
        if name:
            if scope:
                name = f"{scope}/{name}"
        else:
            if scope:
                name = f"{scope}/assign" if '=' in op_name else f"{scope}/{self.ops[op_name]['name']}"
            else:
                name = 'assign' if '=' in op_name else (f"{self.ops[op_name]['name']}")
            if name in self.op_counter:
                name_old = name
                name = f"{name}_{self.op_counter[name]}"
                self.op_counter[name_old] += 1
            else:
                self.op_counter[name] = 0
        dependencies = kwargs.pop('dependencies', [])
        if dependencies:
            found = False
            for dep in dependencies:
                if dep.name == name:
                    found = True
                    break

            if found:
                self.add_layer()
        try:
            op = (self._create_op)(op_name, name, *args)
            in_shape = []
            expand_ops = ('@', 'index', 'concat', 'expand', 'stack', 'group', 'asarray',
                          'interpolate', 'interpolate_nd')
            if op_name not in expand_ops:
                for arg in args:
                    if hasattr(arg, 'shape'):
                        in_shape.append(sum(tuple(arg.shape)))
                    else:
                        if type(arg) in (tuple, list):
                            if hasattr(arg[0], 'shape'):
                                in_shape.append(sum(tuple(arg[0].shape)))
                            else:
                                in_shape.append(sum(arg))
                        else:
                            in_shape.append(1)

                if hasattr(op, 'shape'):
                    if sum(tuple(op.shape)) > max(in_shape):
                        arg1, arg2 = self.broadcast(args[0], args[1])
                        op = (self._create_op)(op_name, name, arg1, arg2, *args[2:])
        except Exception:
            if type(args[0]) in (tuple, list):
                if len(args[0]) > 1:
                    args_tmp = self.broadcast(args[0][0], args[0][1])
                    args_tmp = (args_tmp[0], args_tmp[1]) + tuple(args[0][2:])
                    args_new = args_tmp + args[1:]
            elif '=' in op_name:
                if len(args) > 2:
                    arg1_tmp = self._create_op('index', 'test_idx', args[0], args[2])
                    args_tmp = self.broadcast(arg1_tmp, args[1])
                    args_new = (args[0], args_tmp[1], args[2])
            else:
                args_tmp = self.broadcast(args[0], args[1])
                args_new = args_tmp + args[2:]
            op = (self._create_op)(op_name, name, *args_new)

        for op_name_tmp in op.input_ops:
            if 'assign' not in op_name_tmp:
                idx_1, idx_2 = self.op_indices[op_name_tmp]
                self._set_op(None, idx_1, idx_2)

        if op.is_constant and op_name != 'no_op':
            new_var = op.eval()
            if hasattr(new_var, 'shape'):
                name = f"{name}_evaluated"
                return self.add_var(vtype='constant', name=name, value=new_var)
            return new_var
        else:
            self._add_op(op)
            self.op_indices[op.name] = (self.layer, len(self.get_current_layer()) - 1)
            return op

    def add_layer(self, to_beginning=False) -> None:
        """Adds a new layer to the backend and sets cursor to that layer.

        Parameters
        ----------
        to_beginning
            If true, layer is appended to the beginning of the layer stack instead of the end

        Returns
        -------
        None

        """
        if to_beginning:
            self.layers = [[]] + self.layers
            self._base_layer += 1
            self.layer = -self._base_layer
        else:
            self.layer = len(self.layers) - self._base_layer
            self.layers.append([])

    def add_output_layer(self, outputs, sampling_steps, out_shapes) -> dict:
        """

        Parameters
        ----------
        outputs
        sampling_steps
        out_shapes

        Returns
        -------

        """
        output_col = {}
        if self._output_layer_added:
            out_idx = self.get_var('output_collection/out_var_idx')
            self.top_layer()
        else:
            self.add_layer()
            self._output_layer_added = True
            out_idx = self.add_var(vtype='state_var', name='out_var_idx', dtype='int32', shape=(1, ), value=0, scope='output_collection')
            self.next_layer()
            self.add_op('+=', out_idx, np.ones((1, ), dtype='int32'), scope='output_collection')
            self.previous_layer()
        for i, var_col in enumerate(outputs):
            shape = (
             sampling_steps + 1, len(var_col)) + out_shapes[i]
            key = f"output_col_{i}"
            output_col[key] = self.add_var(vtype='state_var', name=f"out_col_{i}", scope='output_collection', value=np.zeros(shape, dtype=(self._float_def)))
            var_stack = self.stack_vars(var_col)
            self.add_op('=', (output_col[key]), var_stack, out_idx, scope='output_collection')

        return output_col

    def add_input_layer(self, inputs: list, T: float, continuous=True) -> NumpyVar:
        """

        Parameters
        ----------
        inputs
        T
        continuous

        Returns
        -------

        """
        if self._input_layer_added:
            self.bottom_layer()
        else:
            self.add_layer(to_beginning=True)
        t = self.add_var('state_var', name='t', value=0.0, dtype=(self._float_def), shape=())
        self.lhs_vars.append(t.short_name)
        if inputs:
            if continuous:
                from scipy.interpolate import interp1d
                time = np.linspace(0, T, inputs[0][0].shape[0])
                for inp, target_var, idx in inputs:
                    in_name = f"{inp.short_name}_inp" if hasattr(inp, 'short_name') else 'var_inp'
                    if len(inp.shape) > 1:
                        inp = inp.squeeze()
                    f = interp1d(time, inp, axis=0, copy=False, kind='linear')
                    f.shape = inp.shape[1:]
                    f.vtype = 'state_var'
                    f.short_name = in_name
                    f.name = f"network_inputs/{in_name}"
                    self.vars[f.name] = f
                    in_var_interp = self.add_op('interpolate', f, t, scope='network_inputs')
                    if idx:
                        self.add_op('=', target_var, in_var_interp, idx, scope='network_inputs')
                    else:
                        self.add_op('=', target_var, in_var_interp, scope='network_inputs')

            else:
                time_step_idx = self.add_var(vtype='state_var', name='in_var_idx', dtype='int32', shape=(1, ), value=0, scope='network_inputs')
                for inp, target_var, idx in inputs:
                    in_name = f"{inp.short_name}_inp" if hasattr(inp, 'short_name') else 'var_inp'
                    in_var = self.add_var(vtype='state_var', name=in_name, scope='network_inputs', value=inp)
                    in_var_indexed = self.add_op('index', in_var, time_step_idx, scope='network_inputs')
                    if idx:
                        self.add_op('=', target_var, in_var_indexed, idx, scope='network_inputs')
                    else:
                        self.add_op('=', target_var, in_var_indexed, scope='network_inputs')

                time_step = self.add_var('constant', name='time_step_increment', value=np.ones((1, ), dtype='int32'), scope='network_inputs')
                self.add_op('+=', time_step_idx, time_step, scope='network_inputs')
        return t

    def next_layer(self) -> None:
        """Jump to next layer in stack. If we are already at end of layer stack, add new layer to the stack and jump to
        that.
        """
        if self._base_layer + self.layer == len(self.layers) - 1:
            self.add_layer()
        else:
            self.layer += 1

    def previous_layer(self) -> None:
        """Jump to previous layer in stack. If we are already at beginning of layer stack, add new layer to beginning of
        the stack and jump to that.
        """
        if self.layer == -self._base_layer:
            self.add_layer(to_beginning=True)
        else:
            self.layer -= 1

    def goto_layer(self, idx: int) -> None:
        """Jump to layer indicated by index.

        Parameters
        ----------
        idx
            Position of layer to jump towards.

        Returns
        -------
        None

        """
        self.layer = idx

    def remove_layer(self, idx) -> None:
        """Removes layer at index from stack.

        Parameters
        ----------
        idx
            Position of layer in graph.

        """
        self.layers.pop(self._base_layer + idx)
        if idx <= self._base_layer:
            self._base_layer -= 1

    def top_layer(self) -> int:
        """Jump to top layer of the stack.
        """
        self.layer = len(self.layers) - 1 - self._base_layer
        return self.layer

    def bottom_layer(self) -> int:
        """Jump to bottom layer of the stack.
        """
        self.layer = -self._base_layer
        return self.layer

    def get_current_layer(self) -> list:
        """Get operations in current layer.
        """
        return self.layers[(self._base_layer + self.layer)]

    def clear(self) -> None:
        """Removes all layers, variables and operations from graph. Deletes build directory.
        """
        self.vars.clear()
        self.layers = [[]]
        self.op_counter = 0
        self.var_counter = 0
        self.layer = 0
        rmtree(self._build_dir)
        if 'rhs_func' in sys.modules:
            del sys.modules['rhs_func']

    def get_layer(self, idx) -> list:
        """Retrieve layer from graph.

        Parameters
        ----------
        idx
            Position of layer in stack.

        """
        return self.layers[(self._base_layer + idx)]

    def get_var(self, name):
        """Retrieve variable from graph.

        Parameters
        ----------
        name
            Identifier of the variable.

        Returns
        -------
        NumpyVar
            Variable from graph.

        """
        return self.vars[name]

    def eval_var(self, var) -> np.ndarray:
        """Get value of variable.

        Parameters
        ----------
        var
            Identifier of variable in graph.

        Returns
        -------
        np.ndarray
            Current value of the variable.

        """
        return self.vars[var].numpy()

    def compile(self, build_dir: Optional[str]=None, decorator: Optional[Callable]=None, **kwargs) -> tuple:
        """Compile the graph layers/operations. Creates python files containing the functions in each layer.

        Parameters
        ----------
        build_dir
            Directory in which to create the file structure for the simulation.
        decorator
            Decorator function that should be applied to the right-hand side evaluation function.
        kwargs
            decorator keyword arguments

        Returns
        -------
        tuple
            Contains tuples of layer run functions and their respective arguments.

        """
        os.chdir(self._build_dir)
        new_layer_idx = 0
        for layer_idx, layer in enumerate(self.layers.copy()):
            for op in layer.copy():
                if op is None:
                    layer.pop(layer.index(op))

            if len(layer) == 0:
                self.layers.pop(new_layer_idx)
            else:
                new_layer_idx += 1

        if 'rhs_func' in sys.modules:
            del sys.modules['rhs_func']
        state_vars, params, var_map = self._process_vars()
        y = self.get_var('y')
        for key, (vtype, idx) in var_map.items():
            var = self.get_var(key)
            if vtype == 'state_var' and var.short_name != 'y':
                var.args[0] = y
                var.build_op(var.args)

        func_gen = CodeGen()
        for import_line in self._imports:
            func_gen.add_code_line(import_line)
            func_gen.add_linebreak()

        func_gen.add_linebreak()
        func_gen.add_code_line('def rhs_eval(t, y, params):')
        func_gen.add_linebreak()
        func_gen.add_indent()
        func_gen.add_linebreak()
        args = [None for _ in range(len(params))]
        func_gen.add_code_line('# declare constants')
        func_gen.add_linebreak()
        updates, indices = [], []
        i = 0
        for key, (vtype, idx) in var_map.items():
            if vtype == 'constant':
                var = params[idx][1]
                func_gen.add_code_line(f"{var.short_name} = params[{idx}]")
                func_gen.add_linebreak()
                args[idx] = var
                if var.short_name != 'y_delta':
                    updates.append((f"{var.short_name}"))
                    indices.append(i)
                    i += 1

        func_gen.add_linebreak()
        func_gen.add_code_line('# extract state variables from input vector')
        func_gen.add_linebreak()
        for key, (vtype, idx) in var_map.items():
            var = self.get_var(key)
            if vtype == 'state_var':
                func_gen.add_code_line(f"{var.short_name} = {var.value}")
                func_gen.add_linebreak()

        func_gen.add_linebreak()
        func_gen.add_code_line('# calculate right-hand side update of equation system')
        func_gen.add_linebreak()
        arg_updates = []
        for i, layer in enumerate(self.layers):
            for j, op in enumerate(layer):
                lhs = op.value.split('=')[0]
                lhs = lhs.replace(' ', '')
                find_arg = [arg == lhs for arg in updates]
                if any(find_arg):
                    idx = find_arg.index(True)
                    arg_updates.append((updates[idx], indices[idx]))
                func_gen.add_code_line(op.value)
                func_gen.add_linebreak()

        func_gen.add_linebreak()
        func_gen.add_code_line('# update system parameters')
        func_gen.add_linebreak()
        for upd, idx in arg_updates:
            update_str = f"params[{idx}] = {upd}"
            if f"    {update_str}" not in func_gen.code:
                func_gen.add_code_line(update_str)
                func_gen.add_linebreak()

        func_gen.add_code_line(f"return {self.vars['y_delta'].short_name}")
        func_gen.add_linebreak()
        with open('rhs_func.py', 'w') as (f):
            f.writelines(func_gen.code)
            f.close()
        exec('from rhs_func import rhs_eval', globals())
        rhs_eval = globals().pop('rhs_eval')
        os.chdir(self._orig_dir)
        if decorator:
            rhs_eval = decorator(rhs_eval, **kwargs)
        return (rhs_eval, args, state_vars, var_map)

    def broadcast(self, op1: Any, op2: Any, **kwargs) -> tuple:
        """Tries to match the shapes of op1 and op2 such that op can be applied.

        Parameters
        ----------
        op1
            First argument to the operation.
        op2
            Second argument to the operation.
        kwargs
            Additional keyword arguments to be passed to the backend.

        Returns
        -------
        tuple
            Broadcasted op1 and op2.

        """
        if not self._compare_shapes(op1, op2):
            adjust_first = True if hasattr(op2, 'short_name') else False
            op1_tmp, op2_tmp = self._match_shapes(op1, op2, adjust_second=adjust_first)
            if not self._compare_shapes(op1_tmp, op2_tmp):
                op1_tmp, op2_tmp = self._match_shapes(op1_tmp, op2_tmp, adjust_second=(not adjust_first))
            if self._compare_shapes(op1_tmp, op2_tmp):
                op1, op2 = op1_tmp, op2_tmp
        return (
         op1, op2)

    def apply_idx(self, var: Any, idx: Any, update: Optional[Any]=None, update_type: str=None, *args) -> Any:
        """Applies index to a variable. IF update is passed, variable is updated at positions indicated by index.

        Parameters
        ----------
        var
            Variable to index/update
        idx
            Index to variable
        update
            Update to variable entries
        update_type
            Type of lhs update (e.g. `=` or `+=`)

        Returns
        -------
        Any
            Updated/indexed variable.

        """
        if update is None:
            return (self.add_op)('index', var, idx, *args)
        else:
            if not update_type:
                update_type = '='
            return (self.add_op)(update_type, var, update, idx, *args)

    def stack_vars(self, vars: tuple, **kwargs) -> np.ndarray:
        """Group variables into a stack, with the number of variables being the first dimension of the stack.

        Parameters
        ----------
        vars
            Variables to stack together. Should have the same shapes.
        kwargs
            Additional keyword arguments (Ignored in this version of the backend).

        Returns
        -------
        np.ndarray
            Stacked variables.

        """
        return self.add_op('asarray', vars)

    def to_file(self, fn: str):
        """Writes backend to file

        Parameters
        ----------
        fn

        Returns
        -------

        """
        pass

    def from_file(self, fn: str):
        """

        Parameters
        ----------
        fn

        Returns
        -------

        """
        pass

    @staticmethod
    def eval(ops: list) -> list:
        """Evaluates each operation in list.

        Parameters
        ----------
        ops
            List of operations to evaluate.

        """
        return [op.numpy() for op in ops]

    @staticmethod
    def eval_layer(layer: tuple) -> Any:
        """Evaluate layer run function (can only be used after compilation has been performed).

        Parameters
        ----------
        layer
            Layer tuple as returned by `compile`.

        Returns
        -------
        Any
            Result of layer evaluation.

        """
        return (layer[0])(*layer[1])

    def _set_op(self, op, idx1, idx2):
        self.layers[(self._base_layer + idx1)][idx2] = op

    def _add_op(self, op, layer=None):
        if layer is None:
            self.get_current_layer().append(op)
        else:
            self.get_layer(layer).append(op)

    def _solve(self, rhs_func, func_args, T, dt, dts, t, solver, output_indices, **kwargs):
        """

        Parameters
        ----------
        rhs_func
        func_args
        state_vars
        T
        dt
        dts
        t
        solver
        output_indices
        kwargs

        Returns
        -------

        """
        if solver == 'euler':
            times, results = self._integrate(rhs_func=rhs_func, func_args=func_args, T=T, dt=dt, dts=dts, t=t, output_indices=output_indices)
        else:
            if solver == 'scipy':
                from scipy.integrate import solve_ivp
                fun = lambda t, y: rhs_func(t, y, func_args)
                if dts:
                    times = np.arange(0, T, dts)
                    kwargs['t_eval'] = times
                outputs = solve_ivp(fun=fun, t_span=(float(t.numpy()), T), y0=self.vars['y'], first_step=dt, **kwargs)
                results = [outputs['y'].T[:, idx] for idx in output_indices]
                times = outputs['t']
                self.vars['y'] = outputs['y'].T[:, -1]
            else:
                raise ValueError(f"Invalid solver type: {solver}. See docstring of `CircuitIR.run` for valid solver types.")
        return (
         times, results)

    def _integrate(self, rhs_func, func_args, T, dt, dts, t, output_indices):
        sampling_step = int(np.round((dts / dt), decimals=0))
        sampling_steps = int(np.round((T / dts), decimals=0))
        steps = int(np.round((T / dt), decimals=0))
        results = []
        for i, idx in enumerate(output_indices):
            if type(idx) is tuple:
                var_dim = idx[1] - idx[0]
            else:
                if type(idx) is list:
                    if all(np.diff(idx, n=1) == 1):
                        output_indices[i] = (
                         idx[0], idx[(-1)] + 1)
                        var_dim = idx[(-1)] + 1 - idx[0]
                    else:
                        var_dim = len(idx)
                else:
                    var_dim = 1
            results.append(np.zeros((sampling_steps, var_dim)))

        state_vars = self.vars['y']
        sampling_idx = 0
        for i in range(steps):
            deltas = rhs_func(t, state_vars, func_args)
            t += dt
            state_vars += dt * deltas
            if i % sampling_step == 0:
                for idx1, idx2 in enumerate(output_indices):
                    results[idx1][sampling_idx, :] = state_vars[idx2[0]:idx2[1]] if type(idx2) is tuple else state_vars[idx2]

                sampling_idx += 1

        self.vars['y'] = state_vars
        times = np.arange(0, T, dts)
        return (
         times, results)

    def _match_shapes(self, op1: Any, op2: Any, adjust_second: bool=True) -> tuple:
        """Re-shapes op1 and op2 such that they can be combined via mathematical operations.

        Parameters
        ----------
        op1
            First operator.
        op2
            Second operator.
        adjust_second
            If true, the second operator will be re-shaped according to the shape of the first operator. If false,
            it will be done the other way around.

        Returns
        -------
        tuple
            The re-shaped operators.

        """
        if not hasattr(op1, 'shape'):
            op1 = self.add_var(vtype='constant', value=op1, name='c')
        else:
            if not hasattr(op2, 'shape'):
                op2 = self.add_var(vtype='constant', value=op2, name='c')
            else:
                if adjust_second:
                    op_adjust = op2
                    op_target = op1
                else:
                    op_adjust = op1
                    op_target = op2
            if len(op_target.shape) > len(op_adjust.shape):
                target_shape = op_target.shape
                idx = list(target_shape).index(1) if 1 in op_target.shape else len(target_shape) - 1
                op_adjust = self.add_op('expand', op_adjust, idx)
            elif len(op_adjust.shape) > len(op_target.shape) and 1 in op_adjust.shape or len(op_target.shape) == 2 and len(op_adjust.shape) == 2 and op_target.shape[1] != op_adjust.shape[0] and 1 in op_adjust.shape:
                old_shape = list(op_adjust.shape)
                idx = ','.join(['0' if s == 1 else ':' for s in old_shape])
                op_adjust = self.add_op('index', op_adjust, idx)
        if adjust_second:
            return (op_target, op_adjust)
        else:
            return (
             op_adjust, op_target)

    def _match_dtypes(self, op1: Any, op2: Any) -> tuple:
        """Match data types of two operators/variables.
        """
        if issubclass(type(op1), PyRatesOp):
            if issubclass(type(op2), PyRatesOp):
                for acc in ('16', '32', '64', '128'):
                    if acc in op2.dtype:
                        return (
                         self.add_op('cast', op1, op2.dtype), op2)

            return (
             op1, self.add_op('cast', op2, op1.dtype))
        else:
            if issubclass(type(op2), PyRatesOp):
                return (self.add_op('cast', op1, op2.dtype), op2)
            else:
                if hasattr(op1, 'numpy') or type(op1) is np.ndarray:
                    return (
                     op1, self.add_op('cast', op2, op1.dtype))
                if hasattr(op2, 'numpy') or type(op2) is np.ndarray:
                    return (
                     self.add_op('cast', op1, op2.dtype), op2)
            return (
             op1, self.add_op('cast', op2, str(type(op1))))

    def _create_var(self, vtype, dtype, shape, value, name, squeeze=True):
        return NumpyVar(vtype=vtype, dtype=dtype, shape=shape, value=value, name=name, backend=self, squeeze=squeeze)

    def _create_op(self, op, name, *args):
        if not self.ops[op]['call']:
            raise NotImplementedError(f"The operator `{op}` is not implemented for this backend ({self.name}). Please consider passing the required operation to the backend initialization or choose another backend.")
        if op in ('=', '+=', '-=', '*=', '/='):
            if len(args) > 2:
                if hasattr(args[2], 'shape'):
                    if len(args[2].shape) > 1:
                        if 'bool' not in str(type(args[2])):
                            args_tmp = list(args)
                            if not hasattr(args_tmp[2], 'short_name'):
                                idx = self.add_var(vtype='state_var', name='idx', value=(args_tmp[2]))
                            else:
                                idx = args_tmp[2]
                            var, upd, idx = self._process_update_args_old(args[0], args[1], idx)
                            idx_str = ','.join([f"{idx.short_name}[:,{i}]" for i in range(idx.shape[1])])
                            args = (var, upd, idx_str, idx)
            return PyRatesAssignOp(self.ops[op]['call'], self.ops[op]['name'], name, *args, **{'idx_l':self.idx_l, 
             'idx_r':self.idx_r})
        if op is 'index':
            return PyRatesIndexOp(self.ops[op]['call'], self.ops[op]['name'], name, *args, **{'idx_l':self.idx_l,  'idx_r':self.idx_r})
        else:
            if op is 'cast':
                args = list(args)
                for dtype in self.dtypes:
                    if dtype in str(args[1]):
                        args[1] = f"np.{dtype}"
                        break

                args = tuple(args)
            return PyRatesOp(self.ops[op]['call'], self.ops[op]['name'], name, *args)

    def _process_update_args_old(self, var, update, idx):
        """Preprocesses the index and a variable update to match the variable shape.

        Parameters
        ----------
        var
        update
        idx

        Returns
        -------
        tuple
            Preprocessed index and re-shaped update.

        """
        shape = var.shape
        if idx.shape[0] != update.shape[0]:
            if update.shape[0] == 1:
                if len(update.shape) == 1:
                    idx = self.add_op('reshape', idx, tuple(idx.shape) + (1, ))
            else:
                if idx.shape[0] == 1:
                    update = self.add_op('reshape', update, (1, ) + tuple(update.shape))
                elif len(update.shape) > len(idx.shape):
                    if 1 in update.shape:
                        singleton = list(update.shape).index(1)
                        update = self.add_op('squeeze', update, singleton)
                else:
                    raise ValueError(f"Invalid indexing. Operation of shape {shape} cannot be updated with updates of shapes {update.shape} at locations indicated by indices of shape {idx.shape}.")
        if len(idx.shape) < 2:
            idx = self.add_op('reshape', idx, tuple(idx.shape) + (1, ))
        shape_diff = len(shape) - idx.shape[1]
        if shape_diff < 0:
            raise ValueError(f"Invalid index shape. Operation has shape {shape}, but received an index of length {idx.shape[1]}")
        update_dim = 0
        if len(update.shape) > 1:
            update_dim = len(update.shape[1:])
            if update_dim > shape_diff:
                singleton = -1 if update.shape[(-1)] == 1 else list(update.shape).index(1)
                update = self.add_op('squeeze', update, singleton)
                if len(update.shape) > 1:
                    update_dim = len(update.shape[1:])
        shape_diff = int(shape_diff) - update_dim
        if shape_diff > 0:
            indices = []
            indices.append(idx)
            for i in range(shape_diff):
                indices.append(self.add_op('zeros', tuple(idx.shape), idx.dtype))

            idx = self.add_op('concat', indices, 1)
        return (var, update, idx)

    def _process_update_args(self, var, update, idx=None):
        """Preprocesses the index and a variable update to match the variable shape.

        Parameters
        ----------
        var
        update
        idx

        Returns
        -------
        tuple
            Preprocessed index and re-shaped update.

        """
        shape = var.shape
        scatter_into_first_dim = False
        if len(shape) == len(update.shape):
            if shape != update.shape:
                update = self.add_op('squeeze', update)
        if shape[0] == idx.shape[0]:
            if len(shape) > 1:
                if sum(idx.shape) > 1:
                    idx = self.add_op('index', idx, ':, None')
        if update.shape == shape[1:] or update.shape == shape[:-1]:
            scatter_into_first_dim = True
        return (var, update, idx, scatter_into_first_dim)

    def _process_vars(self):
        """

        Returns
        -------

        """
        state_vars, constants, var_map = [], [], {}
        s_idx, c_idx, s_len = (0, 0, 0)
        for key, var in self.vars.items():
            key, state_var = self._is_state_var(key)
            if state_var:
                state_vars.append((key, var))
                var_map[key] = ('state_var', (s_idx, s_len))
                s_idx += 1
                s_len += 1
            else:
                if var.vtype == 'constant' or var.short_name not in self.lhs_vars and key != 'y':
                    constants.append((key, var))
                    var_map[key] = ('constant', c_idx)
                    c_idx += 1

        return (
         state_vars, constants, var_map)

    def _is_state_var(self, key):
        return (
         key, key in self.state_vars)

    @staticmethod
    def _process_func_args(args, var_map, dt):
        for key, var_info in var_map.items():
            if 'times' in key:
                args[var_info[1]] -= dt

        return list(args)

    @staticmethod
    def _compare_vars(v1, v2):
        if v1.short_name == v2.short_name:
            if v1.shape == v2.shape:
                if sum(v1.shape) > 1:
                    return all(v1.flatten() != v2.flatten())
                return v2 != v1

    @staticmethod
    def _compare_shapes(op1: Any, op2: Any, index=False) -> bool:
        """Checks whether the shapes of op1 and op2 are compatible with each other.

        Parameters
        ----------
        op1
            First operator.
        op2
            Second operator.

        Returns
        -------
        bool
            If true, the shapes of op1 and op2 are compatible.

        """
        if hasattr(op1, 'shape'):
            if hasattr(op2, 'shape'):
                if op1.shape == op2.shape:
                    return True
                else:
                    if len(op1.shape) > 1:
                        if len(op2.shape) > 1:
                            return True
                    if len(op1.shape) == 0:
                        if len(op2.shape) == 0:
                            return True
                    return False
        else:
            return True

    @staticmethod
    def _deepcopy(x):
        return deepcopy(x)


class CodeGen:
    __doc__ = 'Generates python code. Can add code lines, line-breaks, indents and remove indents.\n    '

    def __init__(self):
        self.code = []
        self.lvl = 0

    def generate(self):
        """Generates a single code string from its history of code additions.
        """
        return ''.join(self.code)

    def add_code_line(self, code_str):
        """Add code line string to code.
        """
        self.code.append('\t' * self.lvl + code_str)

    def add_linebreak(self):
        """Add a line-break to the code.
        """
        self.code.append('\n')

    def add_indent(self):
        """Add an indent to the code.
        """
        self.lvl += 1

    def remove_indent(self):
        """Remove an indent to the code.
        """
        if self.lvl == 0:
            raise SyntaxError('internal error in code generator')
        self.lvl -= 1