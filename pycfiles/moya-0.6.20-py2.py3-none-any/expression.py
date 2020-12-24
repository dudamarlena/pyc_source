# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/context/expression.py
# Compiled at: 2017-07-23 09:15:02
"""
Parse and evaluate Moya expressions

This module contains some quite shocking micro-optimizations to offset the extra work when compared to Python expressions.

The optimizations were guided by the mandel.xml benchmark which has improved by many orders of magnitude since the first version.

"""
from __future__ import unicode_literals
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from fs.path import basename
from fs import wildcard
from pyparsing import Word, WordEnd, Empty, nums, Combine, oneOf, opAssoc, operatorPrecedence, QuotedString, Literal, ParserElement, ParseException, Forward, Group, Suppress, Regex, delimitedList, Optional
from .. import __version__
from ..context import dataindex
from ..context.dataindex import parse as parseindex
from ..context.expressiontime import TimeSpan
from ..context.expressionrange import ExpressionRange
from ..context.tools import to_expression, decode_string
from ..context.missing import Missing
from ..moyaexceptions import throw
from ..compat import implements_to_string, text_type, string_types
from ..context.modifiers import ExpressionModifiers
from ..moyaexceptions import MoyaException
from ..errors import LogicError
from operator import methodcaller
import logging, operator, re, sys
from operator import truth
import threading
log = logging.getLogger(b'moya.runtime')
ParserElement.enablePackrat(None)
sys.setrecursionlimit(10000)
VERSION = 2

@implements_to_string
class ExpressionError(Exception):

    def __init__(self, exp, msg=None, col=None, original=None):
        super(ExpressionError, self).__init__()
        self.exp = exp
        self.msg = msg or b''
        self.original = original
        self.col = col

    def __str__(self):
        return self.msg

    def __repr__(self):
        if self.original:
            return b"%s '%s': %s" % (self.msg, self.exp, text_type(self.original))
        else:
            return b"%s '%s'" % (self.msg, self.exp)

    def __moyaconsole__(self, console):
        indent = b''
        console(indent + self.exp, bold=True, fg=b'magenta').nl()
        if self.col:
            console(indent)(b' ' * (self.col - 1) + b'^', bold=True, fg=b'red').nl()


class ExpressionCompileError(ExpressionError):
    pass


@implements_to_string
class ExpressionEvalError(ExpressionError):

    def __str__(self):
        if self.original:
            return b"%s '%s': %s" % (self.msg, self.exp, text_type(self.original))
        else:
            return b"%s '%s'" % (self.msg, self.exp)


class Evaluator(object):
    """Base class mainly to make expressions pickleable"""
    __slots__ = [
     b'col', b'tokens']

    def __init__(self, s, loc, tokens):
        self.col = loc
        self.tokens = tokens.asList()
        self.build(tokens)
        super(Evaluator, self).__init__()

    def build(self, tokens):
        pass

    def eval(self, context):
        raise NotImplementedError

    def __getstate__(self):
        return self.tokens

    def __setstate__(self, state):
        self.tokens = state
        self.build(state)


class EvalConstant(Evaluator):
    """Evaluates a constant"""
    __slots__ = [
     b'key', b'value', b'eval']
    constants = {b'None': None, b'True': True, 
       b'False': False, 
       b'yes': True, 
       b'no': False}

    def build(self, tokens):
        self.key = tokens[0]
        value = self.value = self.constants[self.key]
        self.eval = lambda context: value


class EvalVariable(Evaluator):
    """Class to evaluate a parsed variable"""
    __slots__ = [
     b'eval', b'key', b'_index']

    def build(self, tokens):
        self.key = tokens[0]
        self._index = index = dataindex.parse(self.key)
        if index.from_root or len(index) > 1:
            self.eval = methodcaller(b'__getitem__', self._index)
        else:
            self.eval = methodcaller(b'get_simple', self.key)


class EvalLiteralIndex(Evaluator):
    __slots__ = [
     b'scope', b'indices']

    def build(self, tokens):
        self.scope = tokens[0][0].eval
        self.indices = [ dataindex.parse(t[1:]) for t in tokens[0][1:] ]

    def eval(self, context):
        obj = self.scope(context)
        for index in self.indices:
            with context.data_frame(obj):
                obj = context[index]

        return obj


@implements_to_string
class EvalRegExp(Evaluator):
    """Class to evaluate a parsed variable"""
    __slots__ = [
     b'regexp', b'_re', b'match']

    def build(self, tokens):
        self.regexp = tokens[0]
        self._re = re.compile(tokens[0])
        self.match = self._re.match

    def __str__(self):
        return b'/%s/' % self.regexp

    def __repr__(self):
        return b'/%s/' % self.regexp

    def eval(self, context):
        return self


@implements_to_string
class EvalTimespan(Evaluator):
    """Evaluate a timespan spec"""
    __slots__ = [
     b'ts']

    def build(self, tokens):
        self.ts = TimeSpan(tokens[0])

    def __str__(self):
        return text_type(self.ts)

    def eval(self, context):
        return self.ts


class EvalCurrentScope(Evaluator):
    """Class to eval the current scope"""
    __slots__ = []

    def eval(self, context):
        return context.obj


class EvalExplicitVariable(Evaluator):
    """Class to evaluate a parsed constant or explicit variable (beginning with $)"""
    __slots__ = [
     b'index']

    def build(self, tokens):
        self.index = parseindex(tokens[1])

    def eval(self, context):
        return context[self.index]


class EvalInteger(Evaluator):
    """Class to evaluate an integer value"""
    __slots__ = [
     b'value', b'eval']

    def build(self, tokens):
        value = self.value = int(tokens[0])
        self.eval = lambda context: value


class EvalReal(Evaluator):
    """Class to evaluate a real number value"""
    __slots__ = [
     b'value', b'eval']

    def build(self, tokens):
        value = self.value = float(tokens[0])
        self.eval = lambda context: value


class EvalTripleString(Evaluator):
    """Class to evaluate a triple quoted string"""
    __slots__ = [
     b'value', b'eval']

    def build(self, tokens, _decode=decode_string):
        value = self.value = _decode(tokens[0][3:-3])
        self.eval = lambda context: value


class EvalString(Evaluator):
    """Class to evaluate a string"""
    __slots__ = [
     b'value', b'eval']

    def build(self, tokens, _decode=decode_string):
        value = self.value = _decode(tokens[0][1:-1])
        self.eval = lambda context: value


class EvalSignOp(Evaluator):
    """Class to evaluate expressions with a leading + or - sign"""
    __slots__ = [
     b'eval_func', b'_eval', b'eval_func']

    def build(self, tokens):
        sign, value = tokens[0]
        if sign == b'+':
            self.eval_func = operator.pos
        elif sign == b'-':
            self.eval_func = operator.neg
        self._eval = value.eval

    def eval(self, context):
        return self.eval_func(self._eval(context))


class EvalNotOp(Evaluator):
    """Class to evaluate expressions with logical NOT"""
    __slots__ = [
     b'_eval', b'eval']

    def build(self, tokens):
        sign, value = tokens[0]
        _eval = self._eval = value.eval
        self.eval = lambda context: not _eval(context)


class EvalList(Evaluator):
    """Class to evaluate a parsed variable"""
    __slots__ = [
     b'list_tokens']

    def build(self, tokens):
        self.list_tokens = [ t.eval for t in tokens ]

    def eval(self, context):
        return [ _eval(context) for _eval in self.list_tokens ]


class EvalSimpleList(Evaluator):
    """Class to evaluate a parsed variable"""
    __slots__ = [
     b'list_tokens']

    def build(self, tokens):
        self.list_tokens = [ t.eval for t in tokens ]

    def eval(self, context):
        return [ _eval(context) for _eval in self.list_tokens ]


class EvalEmptyList(Evaluator):
    __slots__ = []

    def build(self, tokens):
        pass

    def eval(self, context):
        return []


class EvalDict(Evaluator):
    __slots__ = [
     b'_item_eval']

    def build(self, tokens):
        self._item_eval = [ (k.eval, v.eval) for k, v in tokens[0] ]

    def eval(self, context):
        return {k(context):v(context) for k, v in self._item_eval}


class ExpFunction(object):
    __slots__ = [
     b'context', b'text', b'_eval', b'_context']

    def __init__(self, context, text, eval):
        self.context = context
        self.text = text
        self._eval = eval
        self._context = None
        return

    def __repr__(self):
        return b'<expression>'

    def __moyacall__(self, params):
        with self.context.data_scope(params):
            return self._eval(self.context)


class EvalFunction(Evaluator):
    __slots__ = [
     b'_eval']

    def build(self, tokens):
        self._eval = tokens[0][0].eval

    def eval(self, context):
        return ExpFunction(context, b'', self._eval)


class EvalKeyPairDict(Evaluator):
    __slots__ = [
     b'_item_eval']

    def build(self, tokens):
        self._item_eval = [ (k, v.eval) for k, v in tokens ]

    def eval(self, context):
        return {k:v(context) for k, v in self._item_eval}


class EvalEmptyDict(Evaluator):
    __slots__ = []

    def build(self, tokens):
        pass

    def eval(self, context):
        return {}


class EvalModifierOp(Evaluator):
    """Class to evaluate expressions with a leading filter function"""
    __slots__ = [
     b'value', b'_eval', b'eval', b'filter_func']
    modifiers = ExpressionModifiers()

    def build(self, tokens):
        _filter, value = tokens[0]
        self.value = value
        _eval = self._eval = value.eval
        try:
            filter_func = self.filter_func = getattr(self.modifiers, _filter[:-1])
        except AttributeError:
            raise ValueError(b"unknown modifier '%s'" % _filter)

        self.eval = lambda context: filter_func(context, _eval(context))


class EvalFilterOp(Evaluator):
    __slots__ = [
     b'value', b'_eval', b'operator_eval']

    def build(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        self.operator_eval = [ (op, val.eval) for op, val in pairs(self.value[1:]) ]

    def eval(self, context):
        prod = self._eval(context)
        app = context.get(b'.app', None)
        for op, _eval in self.operator_eval:
            filter_obj = _eval(context)
            if isinstance(filter_obj, text_type) and b'.filters' in context:
                filter_obj = context[b'.filters'].lookup(app, filter_obj)
            if hasattr(filter_obj, b'__moyafilter__'):
                prod = filter_obj.__moyafilter__(context, app, prod, {})
            elif callable(filter_obj):
                prod = filter_obj(prod)
            else:
                raise ValueError((b'{} may not be used as a filter').format(to_expression(context, filter_obj)))

        return prod


class EvalSliceOp(Evaluator):
    __slots__ = [
     b'value_eval', b'slice_eval']

    def build(self, tokens):
        self.value_eval = tokens[0][0].eval
        self.slice_eval = [ t.eval if t is not None else (lambda c: None) for t in tokens[0][1] ]
        if len(self.slice_eval) == 2:
            self.slice_eval.append(lambda context: None)
        if len(self.slice_eval) > 3:
            raise ValueError(b'Slice syntax takes at most 3 values, i.e. value[start:stop:step]')
        return

    def eval(self, context):
        obj = self.value_eval(context)
        slice_indices = [ _eval(context) for _eval in self.slice_eval ]
        start, stop, step = ((None if _s == b'' else _s) for _s in slice_indices)
        try:
            if hasattr(obj, b'slice'):
                return obj.slice(start, stop, step)
            else:
                return obj[start:stop:step]

        except TypeError:
            _vars = (
             context.to_expr(start) if start is not None else b'',
             context.to_expr(stop) if stop is not None else b'',
             context.to_expr(step) if step is not None else b'')
            raise ValueError((b'unable to perform slice operation [{}:{}:{}]').format(*_vars))

        return


class EvalBraceOp(Evaluator):
    __slots__ = [
     b'value_eval', b'index_eval']

    def build(self, tokens):
        self.value_eval = tokens[0][0].eval
        self.index_eval = [ (t[0], t[1].eval) for t in tokens[0][1:] ]

    def eval(self, context):
        obj = self.value_eval(context)
        for brace, eval in self.index_eval:
            index = eval(context)
            if brace == b'[':
                if getattr(index, b'moya_missing', False):
                    raise ValueError((b'unable to look up missing index {!r}').format(index))
                if hasattr(obj, b'__moyacontext__'):
                    obj = obj.__moyacontext__(context)
                if hasattr(index, b'__moyacall__'):
                    for value in obj:
                        if index.__moyacall__(value):
                            return value

                    return Missing(text_type(index))
                try:
                    if hasattr(obj, b'__getitem__'):
                        obj = obj[index]
                    else:
                        obj = getattr(obj, index)
                except Exception:
                    obj = Missing(text_type(index))

            else:
                if isinstance(obj, text_type) and b'.filters' in context:
                    obj = context[b'.filters'].lookup(context.get(b'.app', None), obj)
                if hasattr(obj, b'__moyacall__'):
                    obj = obj.__moyacall__(index)
                else:
                    raise ValueError((b'{} does not accept parameters').format(to_expression(context, obj)))

        return obj


def pairs(tokenlist):
    """Converts a list in to a sequence of paired values"""
    return zip(tokenlist[::2], tokenlist[1::2])


class EvalMultOp(Evaluator):
    """Class to evaluate multiplication and division expressions"""
    __slots__ = [
     b'value', b'_eval', b'operator_eval', b'eval']
    ops = {b'*': operator.mul, b'/': operator.truediv, 
       b'//': operator.floordiv, 
       b'%': operator.mod, 
       b'bitand': operator.and_, 
       b'bitor': operator.or_, 
       b'bitxor': operator.xor}

    def build(self, tokens):
        self.value = tokens[0]
        _eval = self._eval = self.value[0].eval
        ops = self.ops
        operator_eval = self.operator_eval = [ (ops[op], val.eval) for op, val in pairs(self.value[1:]) ]
        if len(self.operator_eval) == 1:
            op_func, rhs_eval = self.operator_eval[0]
            self.eval = lambda context: op_func(_eval(context), rhs_eval(context))
        else:

            def eval(context):
                prod = _eval(context)
                for op_func, rhs_eval in operator_eval:
                    prod = op_func(prod, rhs_eval(context))

                return prod

            self.eval = eval


class EvalAddOp(Evaluator):
    """Class to evaluate addition and subtraction expressions"""
    __slots__ = [
     b'operator_eval', b'value', b'_eval', b'eval']
    ops = {b'+': operator.add, b'-': operator.sub}

    def build(self, tokens):
        self.value = tokens[0]
        _eval = self._eval = self.value[0].eval
        ops = self.ops
        operator_eval = self.operator_eval = [ (ops[op], val.eval) for op, val in pairs(self.value[1:]) ]
        if len(self.operator_eval) == 1:
            op_func, rhs_eval = self.operator_eval[0]
            self.eval = lambda context: op_func(_eval(context), rhs_eval(context))
        else:

            def eval(context):
                prod = _eval(context)
                for op_func, rhs_eval in operator_eval:
                    prod = op_func(prod, rhs_eval(context))

                return prod

            self.eval = eval


class EvalRangeOp(Evaluator):
    __slots__ = [
     b'_evals']

    def build(self, tokens):
        self._evals = [ t.eval for t in tokens[0][0::2] ]

    def eval(self, context):
        a, b = self._evals
        return ExpressionRange.create(context, a(context), b(context), inclusive=True)


class EvalExclusiveRangeOp(Evaluator):
    __slots__ = [
     b'_evals']

    def build(self, tokens):
        self._evals = [ t.eval for t in tokens[0][0::2] ]

    def eval(self, context):
        a, b = self._evals
        return ExpressionRange.create(context, a(context), b(context), inclusive=False)


class EvalTernaryOp(Evaluator):
    __slots__ = [
     b'evals']

    def build(self, tokens):
        self.evals = [ t.eval for t in tokens[0][::2] ]

    def eval(self, context):
        condition, truthy, falsey = self.evals
        if condition(context):
            return truthy(context)
        else:
            return falsey(context)


def _match_re(a, b):
    if isinstance(b, EvalRegExp):
        return truth(b.match(text_type(a)))
    return truth(re.match(b, text_type(a)))


def wildcard_match(name, pattern):
    if isinstance(pattern, list):
        return wildcard.match_any(pattern, name)
    else:
        return wildcard.match(pattern, name)


def _in_operator(a, b):
    try:
        return a in b
    except:
        return False


def _str_in(value, seq):
    """Return True if the string representation of a value equals a
    string representation of any value in a sequence"""
    try:
        str_value = text_type(value)
        return any(str_value == text_type(value) for value in seq)
    except:
        return False


class EvalComparisonOp(Evaluator):
    """Class to evaluate comparison expressions"""
    __slots__ = [
     b'value', b'_eval', b'operator_eval']
    opMap = {b'<': operator.lt, 
       b'lt': operator.lt, 
       b'<=': operator.le, 
       b'lte': operator.le, 
       b'>': operator.gt, 
       b'gt': operator.gt, 
       b'>=': operator.ge, 
       b'gte': operator.ge, 
       b'!=': operator.ne, 
       b'==': operator.eq, 
       b'~=': lambda a, b: text_type(a).lower() == text_type(b).lower(), 
       b'^=': lambda a, b: text_type(a).startswith(text_type(b)), 
       b'$=': lambda a, b: text_type(a).endswith(text_type(b)), 
       b'is': operator.is_, 
       b'is not': operator.is_not, 
       b'in': _in_operator, 
       b'not in': lambda a, b: not _in_operator(a, b), 
       b'instr': _str_in, 
       b'not instr': lambda a, b: not _str_in(a, b), 
       b'matches': _match_re, 
       b'fnmatches': wildcard_match}

    def build(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        self.operator_eval = [ (self.opMap[op], val.eval) for op, val in pairs(self.value[1:]) ]

    def eval(self, context):
        val1 = self._eval(context)
        for op_func, _eval in self.operator_eval:
            val2 = _eval(context)
            val1 = op_func(val1, val2)
            if not val1:
                return False

        return True


class EvalFormatOp(Evaluator):
    __slots__ = [
     b'value', b'_eval', b'evals']

    def build(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        self.evals = [ val.eval for op, val in pairs(self.value[1:]) ]

    def eval(self, context):
        val1 = self._eval(context)
        for _eval in self.evals:
            fmt = _eval(context)
            if not isinstance(fmt, string_types):
                raise ValueError((b'format should be a string, not {!r}').format(fmt))
            return format(val1, fmt)

        return val1


class EvalLogicOpOR(Evaluator):
    __slots__ = [
     b'value', b'_eval', b'operator_eval']

    def build(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        self.operator_eval = [ val.eval for op, val in pairs(self.value[1:]) ]

    def eval(self, context):
        val1 = self._eval(context)
        if val1:
            return val1
        for _eval in self.operator_eval:
            val2 = _eval(context)
            val1 = val1 or val2
            if val1:
                return val1

        return val1


class EvalLogicOpAND(Evaluator):
    __slots__ = [
     b'value', b'_eval', b'operator_eval']

    def build(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        self.operator_eval = [ val.eval for op, val in pairs(self.value[1:]) ]

    def eval(self, context):
        val1 = self._eval(context)
        if not val1:
            return val1
        for _eval in self.operator_eval:
            val2 = _eval(context)
            val1 = val1 and val2
            if not val1:
                return val1

        return val1


word_characters = b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789'
expr = Forward()
integer = Word(nums)
real = Combine(Word(nums) + b'.' + Word(nums))
constant = oneOf(b'True False None yes no') + WordEnd(word_characters)
simple_variable = Regex(b'([a-zA-Z0-9_]+)')
variable = Regex(b'([a-zA-Z0-9\\._]+)')
explicit_variable = b'$' + Regex(b'([a-zA-Z0-9\\._]+)')
current_scope = Literal(b'$$')
triple_string = QuotedString(b"'''", escChar=None, unquoteResults=False) | QuotedString(b'"""', escChar=None, unquoteResults=False)
string = QuotedString(b'"', escChar=b'\\', unquoteResults=False) | QuotedString(b"'", escChar=b'\\', unquoteResults=False)
regexp = QuotedString(b'/', escChar=None)
timespan = Combine(Word(nums) + oneOf(b'ms s m h d'))
current_scope_operand = current_scope
variable_operand = variable
explicit_variable_operand = explicit_variable
integer_operand = integer
real_operand = real
number_operand = real | integer
triple_string_operand = triple_string
string_operand = string
groupop = Literal(b',')
signop = oneOf(b'+ -')
multop = oneOf(b'* / // % bitand bitor')
filterop = oneOf(b'|')
plusop = oneOf(b'+ -')
notop = Literal(b'not') + WordEnd(word_characters)
rangeop = Literal(b'..')
exclusiverangeop = Literal(b'...')
ternaryop = ('?', ':')
current_scope_operand.setParseAction(EvalCurrentScope)
variable_operand.setParseAction(EvalVariable)
explicit_variable_operand.setParseAction(EvalExplicitVariable)
integer_operand.setParseAction(EvalInteger)
real_operand.setParseAction(EvalReal)
triple_string.setParseAction(EvalTripleString)
string_operand.setParseAction(EvalString)
constant.setParseAction(EvalConstant)
regexp.setParseAction(EvalRegExp)
timespan.setParseAction(EvalTimespan)
modifier = Regex(b'([a-zA-Z][a-zA-Z0-9_]*)\\:')
simple_list_operand = Group(delimitedList(expr))
simple_list_operand.setParseAction(EvalSimpleList)
list_operand = Suppress(b'[') + delimitedList(expr) + Suppress(b']')
list_operand.setParseAction(EvalList)
empty_list_operand = Literal(b'[]')
empty_list_operand.setParseAction(EvalEmptyList)
dict_item = Group(expr + Suppress(Literal(b':')) + expr)
dict_operand = Group(Suppress(b'{') + delimitedList(dict_item) + Suppress(b'}'))
dict_operand.setParseAction(EvalDict)
empty_dict_operand = Literal(b'{}')
empty_dict_operand.setParseAction(EvalEmptyDict)
function_operand = Group(Suppress(b'`') + expr + Suppress(b'`'))
function_operand.setParseAction(EvalFunction)
key_pair = Group(Regex(b'([a-zA-Z0-9_]+)') + Suppress(Literal(b'=') + WordEnd(b'=!+-*/')) + expr)
key_pair_dict_operand = delimitedList(key_pair)
key_pair_dict_operand.setParseAction(EvalKeyPairDict)
callop = Group(b'(' + expr + Suppress(b')'))
index = Group(b'[' + expr + Suppress(b']'))
_slice = Group(Suppress(b'[') + delimitedList(Optional(expr, default=None), b':') + Suppress(b']'))
braceop = callop | index
sliceop = _slice
literalindex = Regex(b'\\.([a-zA-Z0-9\\._]+)')
operand = timespan | real_operand | integer_operand | triple_string_operand | string_operand | regexp | constant | function_operand | key_pair_dict_operand | current_scope_operand | explicit_variable_operand | variable_operand | empty_list_operand | empty_dict_operand | list_operand | dict_operand
comparisonop = oneOf(b'< <= > >= != == ~= ^= $=') | Literal(b'not in') + WordEnd() | Literal(b'not instr') + WordEnd() | Literal(b'is not') + WordEnd() | oneOf(b'is in instr lt lte gt gte matches fnmatches') + WordEnd()
logicopOR = Literal(b'or') + WordEnd()
logicopAND = Literal(b'and') + WordEnd()
formatop = Literal(b'::')
expr << operatorPrecedence(operand, [
 (
  signop, 1, opAssoc.RIGHT, EvalSignOp),
 (
  exclusiverangeop, 2, opAssoc.LEFT, EvalExclusiveRangeOp),
 (
  rangeop, 2, opAssoc.LEFT, EvalRangeOp),
 (
  braceop, 1, opAssoc.LEFT, EvalBraceOp),
 (
  sliceop, 1, opAssoc.LEFT, EvalSliceOp),
 (
  literalindex, 1, opAssoc.LEFT, EvalLiteralIndex),
 (
  modifier, 1, opAssoc.RIGHT, EvalModifierOp),
 (
  formatop, 2, opAssoc.LEFT, EvalFormatOp),
 (
  multop, 2, opAssoc.LEFT, EvalMultOp),
 (
  plusop, 2, opAssoc.LEFT, EvalAddOp),
 (
  filterop, 2, opAssoc.LEFT, EvalFilterOp),
 (
  comparisonop, 2, opAssoc.LEFT, EvalComparisonOp),
 (
  notop, 1, opAssoc.RIGHT, EvalNotOp),
 (
  logicopAND, 2, opAssoc.LEFT, EvalLogicOpAND),
 (
  logicopOR, 2, opAssoc.LEFT, EvalLogicOpOR),
 (
  ternaryop, 3, opAssoc.LEFT, EvalTernaryOp)])

class DummyLock(object):
    """Replacement for real lock that does nothing"""

    def __enter__(self):
        pass

    def __exit__(self, *args, **kwargs):
        pass


class Function(object):
    __slots__ = [
     b'expression', b'scope']

    def __init__(self, expression, scope=None):
        self.expression = expression
        if scope is None:
            scope = {}
        self.scope = scope
        return

    def __repr__(self):
        return (b'<function "{}">').format(self.expression.exp)

    def __call__(self, context, **params):
        with context.data_frame(params):
            with context.data_scope(self.scope):
                return self.expression.eval(context)

    def call(self, context, params):
        with context.data_frame(params):
            with context.data_scope(self.scope):
                return self.expression.eval(context)

    def get_callable(self, context):

        def call(params):
            with context.data_frame(params):
                with context.data_scope(self.scope):
                    return self.expression.eval(context)

        return call

    def get_scope_callable(self, context):

        def callscope(scope):
            with context.data_scope(scope):
                return self.expression.eval(context)

        return callscope


@implements_to_string
class Expression(object):
    """Evaluate an arithmetic expression of context values"""
    exp_cache = {}
    new_expressions = set()
    _lock = threading.RLock()

    def __init__(self, exp):
        self.exp = exp
        self.compiled_exp = None
        self._eval = self._lazy_compile_eval
        self.new_expressions.add(exp)
        return

    def _lazy_compile_eval(self, context):
        self.compile()
        return self._eval(context)

    def compile(self):
        self.compiled_exp = self.compile_cache(self.exp)
        self._eval = self.compiled_exp[0].eval
        return self

    def eval(self, context):
        try:
            obj = self._eval(context)
            if hasattr(obj, b'__moyacontext__'):
                return obj.__moyacontext__(context)
            return obj
        except (ExpressionError, MoyaException, LogicError):
            raise
        except ArithmeticError as e:
            if isinstance(e, ZeroDivisionError):
                throw(b'math.division-error', (b"Can't divide by zero in '{}'").format(self.exp), diagnosis=b'Check your math')
            else:
                throw(b'math.arithmetic-error', text_type(e))
        except Exception as e:
            if context[b'.develop']:
                print((b'In expression.eval {!r}').format(self))
                import traceback
                traceback.print_exc(e)
            raise ExpressionEvalError(self.exp, original=e)

    def make_function(self, context=None):
        """Returns a callable from this expression"""
        return Function(self, context.obj if context else None)

    def __repr__(self):
        return b'Expression(%r)' % self.exp

    def __str__(self):
        return self.exp

    def __getstate__(self):
        self.compiled_exp = self.compile_cache(self.exp)
        return (self.exp, self.compiled_exp)

    def __setstate__(self, state):
        """Bit of magic to lazily compile expressions after unpickling"""
        self.exp, self.compiled_exp = state
        self.exp_cache[self.exp] = self.compiled_exp
        self._eval = self.compiled_exp[0].eval

    @classmethod
    def insert_expressions(cls, expressions):
        exp_cache = cls.exp_cache
        for expression in expressions:
            if expression.exp not in exp_cache:
                exp_cache[expression.exp] = expression.compiled_exp

    @classmethod
    def dump(cls, cache):
        name = (b'expcache.{}.{}').format(VERSION, __version__)
        cache.set(name, cls.exp_cache)

    @classmethod
    def load(cls, cache):
        name = (b'expcache.{}.{}').format(VERSION, __version__)
        exp = cache.get(name, None)
        if exp is not None:
            cls.exp_cache.update(exp)
            return True
        else:
            return False

    @classmethod
    def get_eval(cls, exp, context):
        with cls._lock:
            try:
                compiled_exp = cls.exp_cache[exp]
            except KeyError:
                try:
                    compiled_exp = cls.exp_cache[exp] = expr.parseString(exp, parseAll=True).asList()
                except ParseException as e:
                    raise ExpressionCompileError(exp, (b'unable to parse expression "{}"').format(exp), col=e.col, original=e)

            return compiled_exp[0].eval(context)

    @classmethod
    def compile_cache(cls, exp):
        with cls._lock:
            try:
                return cls.exp_cache[exp]
            except KeyError:
                try:
                    compiled_exp = cls.exp_cache[exp] = expr.parseString(exp, parseAll=True).asList()
                    return compiled_exp
                except ParseException as e:
                    raise ExpressionCompileError(exp, (b'unable to parse expression "{}"').format(exp), col=e.col, original=e)

    @classmethod
    def get_new_expressions(cls):
        """Get new expressions added since last call to `get_new_expressions`"""
        expressions = [ Expression(exp) for exp in cls.new_expressions ]
        cls.new_expressions.clear()
        return expressions

    @classmethod
    def scan(cls, exp):
        """Parse as much of the string as possible, return a tuple containing
        the parsed string, and the unparsed string.

        """
        with cls._lock:
            scan = expr.scanString(exp, maxMatches=1)
            try:
                compiled_exp, start, end = next(scan)
            except StopIteration:
                return (
                 b'', exp)

            if start != 0:
                return (b'', exp)
            expression = exp[start:end]
            cls.exp_cache[expression] = compiled_exp.asList()
            return (expression, exp[end:])

    _re_substitute_context = re.compile(b'\\$\\{(.*?)\\}')

    @classmethod
    def extract(cls, text):
        """Extract and compile expression in substitution syntax"""
        text = text_type(text)
        if not text:
            return
        with cls._lock:
            for exp in cls._re_substitute_context.findall(text):
                try:
                    cls.compile_cache(exp)
                except:
                    log.error(b"expression '%s' failed to parse", exp)


class DefaultExpression(object):
    """An object that may be used where an Expression is used,
    but returns a pre-determined value.

    """

    def __init__(self, return_value=None):
        self.return_value = return_value

    def __repr__(self):
        return b'DefaultExpression(%r)' % self.return_value

    def eval(self, context):
        return self.return_value


class TrueExpression(DefaultExpression):
    """A default expression that returns True"""

    def eval(self, context):
        return True


class FalseExpression(DefaultExpression):
    """A default expression that returns False"""

    def eval(self, context):
        return False


def main():
    from context import Context
    c = Context()
    c[b'foo'] = 5
    c[b'word'] = b'apple'
    c[b'number'] = b'100'
    c[b'bar'] = dict(a=2, b=3)

    def call(v):
        return v.split(b',')

    c[b'filter'] = call
    e = Expression(b'upper:("Hello " + "World")', c)
    print(e())
    e = Expression(b'exists:"foo"', c)
    print(e())
    e = Expression(b'strip:last:("foo, bar, baz"|.filter)', c)
    print(e())
    e = Expression(b'"500" matches /\\d+/', c)
    print(e())
    e = Expression(b'not(1>1)', c)
    print(e())
    e = Expression(b'not ("500" matches /\\d+/)', c)
    print(e())
    e = Expression(b'bar["a"]', c)
    print(e())


if __name__ == b'__main__':
    from moya.context import Context
    c = Context({b'name': b'Will'})
    c[b'.develop'] = True
    print(c.eval(b'{upper:name}'))
    print(c.eval(b'{upper:name}(name="will")'))
    exp = b"list:map:[['one', 'two', 'three'], {upper:$$}]"
    print(c.eval(exp))