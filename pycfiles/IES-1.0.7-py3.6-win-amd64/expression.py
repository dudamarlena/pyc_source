# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\strategycontainer\tsp\expression.py
# Compiled at: 2018-01-16 00:14:47
# Size of source mod 2**32: 9851 bytes
"""
NumericalExpression term.
"""
from itertools import chain
import re
from numbers import Number
import numexpr
from numexpr.necompiler import getExprNames
from numpy import full, inf
from .term import Term, ComputableTerm
_VARIABLE_NAME_RE = re.compile('^(x_)([0-9]+)$')
ops_to_methods = {'+':'__add__', 
 '-':'__sub__', 
 '*':'__mul__', 
 '/':'__div__', 
 '%':'__mod__', 
 '**':'__pow__', 
 '&':'__and__', 
 '|':'__or__', 
 '^':'__xor__', 
 '<':'__lt__', 
 '<=':'__le__', 
 '==':'__eq__', 
 '!=':'__ne__', 
 '>=':'__ge__', 
 '>':'__gt__'}
methods_to_ops = {v:k for k, v in ops_to_methods.items()}
ops_to_commuted_methods = {'+':'__radd__', 
 '-':'__rsub__', 
 '*':'__rmul__', 
 '/':'__rdiv__', 
 '%':'__rmod__', 
 '**':'__rpow__', 
 '&':'__rand__', 
 '|':'__ror__', 
 '^':'__rxor__', 
 '<':'__gt__', 
 '<=':'__ge__', 
 '==':'__eq__', 
 '!=':'__ne__', 
 '>=':'__le__', 
 '>':'__lt__'}
unary_ops_to_methods = {'-':'__neg__', 
 '~':'__invert__'}
UNARY_OPS = {
 '-'}
MATH_BINOPS = {'+', '-', '*', '/', '**', '%'}
FILTER_BINOPS = {'&', '|'}
COMPARISONS = {'<', '<=', '!=', '>=', '>', '=='}
NUMEXPR_MATH_FUNCS = {
 'sin',
 'cos',
 'tan',
 'arcsin',
 'arccos',
 'arctan',
 'sinh',
 'cosh',
 'tanh',
 'arcsinh',
 'arccosh',
 'arctanh',
 'log',
 'log10',
 'log1p',
 'exp',
 'expm1',
 'sqrt',
 'abs'}

def _ensure_element(tup, elem):
    """
    Create a tuple containing all elements of tup, plus elem.

    Returns the new tuple and the index of elem in the new tuple.
    """
    try:
        return (
         tup, tup.index(elem))
    except ValueError:
        return (
         tuple(chain(tup, (elem,))), len(tup))


class BadBinaryOperator(TypeError):
    __doc__ = '\n    Called when a bad binary operation is encountered.\n\n    Parameters\n    ----------\n    op : str\n        The attempted operation\n    left : zipline.computable.Term\n        The left hand side of the operation.\n    right : zipline.computable.Term\n        The right hand side of the operation.\n    '

    def __init__(self, op, left, right):
        super(BadBinaryOperator, self).__init__("Can't compute {left} {op} {right}".format(op=op,
          left=(type(left).__name__),
          right=(type(right).__name__)))


def method_name_for_op(op, commute=False):
    """
    Get the name of the Python magic method corresponding to `op`.

    Parameters
    ----------
    op : str {'+','-','*', '/','**','&','|','^','<','<=','==','!=','>=','>'}
        The requested operation.
    commute : bool
        Whether to return the name of an equivalent method after flipping args.

    Returns
    -------
    method_name : str
        The name of the Python magic method corresponding to `op`.
        If `commute` is True, returns the name of a method equivalent to `op`
        with inputs flipped.

    Examples
    --------
    >>> method_name_for_op('+')
    '__add__'
    >>> method_name_for_op('+', commute=True)
    '__radd__'
    >>> method_name_for_op('>')
    '__gt__'
    >>> method_name_for_op('>', commute=True)
    '__lt__'
    """
    if commute:
        return ops_to_commuted_methods[op]
    else:
        return ops_to_methods[op]


def unary_op_name(op):
    return unary_ops_to_methods[op]


def is_comparison(op):
    return op in COMPARISONS


class NumericalExpression(ComputableTerm):
    __doc__ = '\n    Term binding to a numexpr expression.\n\n    Parameters\n    ----------\n    expr : string\n        A string suitable for passing to numexpr.  All variables in \'expr\'\n        should be of the form "x_i", where i is the index of the corresponding\n        factor input in \'binds\'.\n    binds : tuple\n        A tuple of factors to use as inputs.\n    dtype : np.dtype\n        The dtype for the expression.\n    '
    window_length = 0

    def __new__(cls, expr, binds, dtype):
        return super(NumericalExpression, cls).__new__(cls,
          inputs=binds,
          expr=expr,
          dtype=dtype,
          window_safe=(all(t.window_safe for t in binds)))

    def _init(self, expr, *args, **kwargs):
        self._expr = expr
        return (super(NumericalExpression, self)._init)(*args, **kwargs)

    @classmethod
    def _static_identity(cls, expr, *args, **kwargs):
        return (
         (super(NumericalExpression, cls)._static_identity)(*args, **kwargs),
         expr)

    def _validate(self):
        variable_names, _unused = getExprNames(self._expr, {})
        expr_indices = []
        for name in variable_names:
            if name == 'inf':
                pass
            else:
                match = _VARIABLE_NAME_RE.match(name)
                if not match:
                    raise ValueError('%r is not a valid variable name' % name)
                expr_indices.append(int(match.group(2)))

        expr_indices.sort()
        expected_indices = list(range(len(self.inputs)))
        if expr_indices != expected_indices:
            raise ValueError('Expected %s for variable indices, but got %s' % (
             expected_indices, expr_indices))
        super(NumericalExpression, self)._validate()

    def _compute(self, arrays, dates, assets, mask):
        """
        Compute our stored expression string with numexpr.
        """
        out = full((mask.shape), (self.missing_value), dtype=(self.dtype))
        numexpr.evaluate((self._expr),
          local_dict={'x_%d' % idx:array for idx, array in enumerate(arrays)},
          global_dict={'inf': inf},
          out=out)
        return out

    def _rebind_variables(self, new_inputs):
        """
        Return self._expr with all variables rebound to the indices implied by
        new_inputs.
        """
        expr = self._expr
        for idx, input_ in reversed(list(enumerate(self.inputs))):
            old_varname = 'x_%d' % idx
            temp_new_varname = 'x_temp_%d' % new_inputs.index(input_)
            expr = expr.replace(old_varname, temp_new_varname)

        return expr.replace('_temp_', '_')

    def _merge_expressions(self, other):
        """
        Merge the inputs of two NumericalExpressions into a single input tuple,
        rewriting their respective string expressions to make input names
        resolve correctly.

        Returns a tuple of (new_self_expr, new_other_expr, new_inputs)
        """
        new_inputs = tuple(set(self.inputs).union(other.inputs))
        new_self_expr = self._rebind_variables(new_inputs)
        new_other_expr = other._rebind_variables(new_inputs)
        return (new_self_expr, new_other_expr, new_inputs)

    def build_binary_op(self, op, other):
        """
        Compute new expression strings and a new inputs tuple for combining
        self and other with a binary operator.
        """
        if isinstance(other, NumericalExpression):
            self_expr, other_expr, new_inputs = self._merge_expressions(other)
        else:
            if isinstance(other, Term):
                self_expr = self._expr
                new_inputs, other_idx = _ensure_element(self.inputs, other)
                other_expr = 'x_%d' % other_idx
            else:
                if isinstance(other, Number):
                    self_expr = self._expr
                    other_expr = str(other)
                    new_inputs = self.inputs
                else:
                    raise BadBinaryOperator(op, other)
        return (
         self_expr, other_expr, new_inputs)

    @property
    def bindings(self):
        return {'x_%d' % i:input_ for i, input_ in enumerate(self.inputs)}

    def __repr__(self):
        return "{typename}(expr='{expr}', bindings={bindings})".format(typename=(type(self).__name__),
          expr=(self._expr),
          bindings=(self.bindings))

    def short_repr(self):
        """Short repr to use when rendering Pipeline graphs."""
        return 'Expression: {expr}'.format(typename=(type(self).__name__),
          expr=(self._expr))