# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/dbexpression.py
# Compiled at: 2017-07-25 13:55:45
from __future__ import unicode_literals
from __future__ import print_function
from .context import dataindex
from .context.tools import to_expression
from .compat import implements_to_string, text_type
from .context.missing import is_missing
from .interface import unproxy
from pyparsing import Word, WordEnd, nums, alphas, Combine, oneOf, opAssoc, operatorPrecedence, QuotedString, Literal, ParserElement, ParseException, Forward, Group, Suppress, Optional, Regex
from sqlalchemy import and_, or_, func, not_
import operator, re, threading

def dbobject(obj):
    return getattr(obj, b'__moyadbobject__', lambda : obj)()


@implements_to_string
class DBExpressionError(Exception):
    hide_py_traceback = True
    error_type = b'Database expression error'

    def __init__(self, exp, msg=None, col=None):
        self.exp = exp
        self.msg = msg or b''
        self.col = col

    def __str__(self):
        return self.msg

    def __moyaconsole__(self, console):
        indent = b''
        console(indent + self.exp, bold=True, fg=b'magenta').nl()
        if self.col:
            console(indent)(b' ' * (self.col - 1) + b'^', bold=True, fg=b'red').nl()


class DBEvalError(Exception):
    pass


def pairs(tokenlist):
    """Converts a list in to a sequence of paired values"""
    return zip(tokenlist[::2], tokenlist[1::2])


class ExpressionContext(object):

    def __init__(self, exp):
        self.exp = exp
        self._joins = []
        super(ExpressionContext, self).__init__()

    def __repr__(self):
        return (b"<expressioncontext '{}'>").format(self.exp)

    def add_joins(self, joins):
        self._joins.append(joins)

    def process_qs(self, qs):
        for j in self._joins:
            if isinstance(j, (tuple, list)):
                qs = qs.join(*j)
            else:
                qs = qs.join(j)

        return qs


class ExpressionModifiers(object):

    def abs(self, context, v):
        return func.abs(v)

    def count(self, context, v):
        return func.count(v)

    def sum(self, context, v):
        return func.sum(v)

    def min(self, context, v):
        return func.min(v)

    def max(self, context, v):
        return func.max(v)

    def lower(self, context, v):
        return func.lower(v)


class EvalModifierOp(object):
    modifiers = ExpressionModifiers()

    def __init__(self, tokens):
        filter, value = tokens[0]
        self.value = value
        self._eval = value.eval
        try:
            self.filter_func = getattr(self.modifiers, filter[:-1])
        except AttributeError:
            raise DBEvalError(b"unknown filter type '%s'" % filter)

    def eval(self, archive, context, app, exp_context):
        return self.filter_func(context, self._eval(archive, context, app, exp_context))


class EvalMultOp(object):
    """Class to evaluate multiplication and division expressions"""
    ops = {b'*': operator.imul, b'/': operator.itruediv, 
       b'//': operator.ifloordiv, 
       b'%': operator.imod}

    def __init__(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        ops = self.ops
        self.operator_eval = [ (ops[op], val.eval) for op, val in pairs(self.value[1:]) ]

    def eval(self, archive, context, app, exp_context):
        prod = self._eval(archive, context, app, exp)
        for op_func, _eval in self.operator_eval:
            prod = op_func(prod, _eval(archive, context, app, exp_context))

        return prod


class EvalAddOp(object):
    """Class to evaluate addition and subtraction expressions"""
    ops = {b'+': operator.add, b'-': operator.sub}

    def __init__(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        ops = self.ops
        self.operator_eval = [ (ops[op], val.eval) for op, val in pairs(self.value[1:]) ]

    def eval(self, archive, context, app, exp_context):
        sum = self._eval(archive, context, app, exp_context)
        for op_func, _eval in self.operator_eval:
            sum = op_func(sum, _eval(archive, context, app, exp_context))

        return sum


class EvalConstant(object):
    """Evaluates a constant"""
    constants = {b'None': None, b'True': True, 
       b'False': False, 
       b'yes': True, 
       b'no': False}

    def __init__(self, tokens):
        self.key = tokens[0]
        self.value = self.constants[self.key]

    def eval(self, archive, context, app, exp_context):
        return self.value


class EvalInteger(object):
    """Class to evaluate an integer value"""

    def __init__(self, tokens):
        self.value = int(tokens[0])

    def eval(self, archive, context, app, exp_context):
        return self.value


class EvalReal(object):
    """Class to evaluate a real number value"""

    def __init__(self, tokens):
        self.value = float(tokens[0])

    def eval(self, archive, context, app, exp_context):
        return self.value


class EvalString(object):
    """Class to evaluate a string"""

    def __init__(self, tokens):
        self.value = tokens[0]

    def eval(self, archive, context, app, exp_context):
        return self.value


def qs(value):
    if hasattr(value, b'__moyadbobject__'):
        value = value.__moyadbobject__()
    if hasattr(value, b'_get_query_set'):
        value = value._get_query_set()
    if isinstance(value, list):
        return [ getattr(v, b'id', v) for v in value ]
    return value


class EvalVariable(object):
    """Class to evaluate a parsed variable"""

    def __init__(self, tokens):
        key = tokens[0]
        self.index = dataindex.parse(key)

    def eval(self, archive, context, app, exp_context):
        value = context[self.index]
        if is_missing(value):
            raise DBEvalError((b"Database expression value '{}' is missing from the context").format(self.index))
        return dbobject(unproxy(value))


class EvalModelReference(object):
    """Gets a model reference"""
    _ref_model_ref = re.compile(b'^(.*?#.*?)(?:\\.(.*?))?$')

    def __init__(self, tokens):
        self.index = tokens[0]

    def eval(self, archive, context, app, exp_context):
        model_ref, index = self._ref_model_ref.match(self.index).groups()
        app = app or context.get(b'.app', None)
        if app is None:
            raise DBEvalError((b"unable to get app from '{}'").format(self.index))
        if index is None:
            app, model_element = app.get_element(model_ref)
            try:
                table_class = model_element.get_table_class(app)
            except Exception as e:
                raise DBEvalError(str(e))

            return table_class
        index = list(dataindex.parse(index))
        app, model_element = app.get_element(model_ref)
        try:
            table_class = model_element.get_table_class(app)
        except Exception as e:
            raise DBEvalError(str(e))

        try:
            model_reference_result = table_class._get_index(archive, context, app, exp_context, index)
        except (KeyError, AttributeError):
            raise DBEvalError((b'no column or object called "{}"').format(self.index))
        else:
            return model_reference_result

        return


class EvalComparisonOp(object):
    """Class to evaluate comparison expressions"""

    @classmethod
    def match_re(cls, a, b):
        return bool(b.match(a))

    @classmethod
    def escape_like(cls, like, _should_escape=(b'\\%_').__contains__):
        """escape LIKE comparisons"""
        if not isinstance(like, text_type):
            return like
        return (b'').join((b'\\' + c if _should_escape(c) else c) for c in like)

    def in_(context, a, b):
        if hasattr(b, b'__moyadbsubselect__'):
            sub_b = b.__moyadbsubselect__(context)
            if sub_b is not None:
                b = sub_b
        a = qs(a)
        try:
            return a.in_(qs(b))
        except:
            raise DBEvalError(b"db expression 'in' operator works on columns only (did you mean .id)?")

        return

    def notin_(context, a, b):
        if hasattr(b, b'__moyadbsubselect__'):
            sub_b = b.__moyadbsubselect__(context)
            if sub_b is not None:
                b = sub_b
        a = qs(a)
        try:
            return a.notin_(qs(b))
        except:
            raise DBEvalError(b"db expression 'not in' operator works on columns only (did you mean .id)?")

        return

    def contains_(context, a, b):
        try:
            return qs(a).contains(qs(b))
        except:
            raise DBEvalError((b"value {} is an invalid operand for the 'contains' operator").format(to_expression(context, b)))

    def icontains_(context, a, b):
        if not isinstance(b, text_type):
            raise DBEvalError((b'icontains right hand side should be a string, not {}').format(context.to_expr(b)))
        b = (b'%{}%').format(EvalComparisonOp.escape_like(b))
        try:
            return qs(a).like(b)
        except:
            raise DBEvalError((b"{} may not be used with 'icontains' operator").format(context.to_expr(a)))

    def ieq(context, a, b):
        if not isinstance(b, text_type):
            raise DBEvalError((b'case insensitive equality operator (~=) right hand side should be a string, not {}').format(context.to_expr(b)))
        return qs(a).ilike(EvalComparisonOp.escape_like(b), escape=b'\\')

    opMap = {b'<': lambda c, a, b: qs(a) < qs(b), 
       b'lt': lambda c, a, b: qs(a) < qs(b), 
       b'<=': lambda c, a, b: qs(a) <= qs(b), 
       b'lte': lambda c, a, b: qs(a) <= qs(b), 
       b'>': lambda c, a, b: qs(a) > qs(b), 
       b'gt': lambda c, a, b: qs(a) > qs(b), 
       b'>=': lambda c, a, b: qs(a) >= qs(b), 
       b'gte': lambda c, a, b: qs(a) >= qs(b), 
       b'!=': lambda c, a, b: qs(a) != qs(b), 
       b'==': lambda c, a, b: qs(a) == qs(b), 
       b'like': lambda c, a, b: qs(a).like(qs(b)), 
       b'ilike': lambda c, a, b: qs(a).ilike(qs(b)), 
       b'~=': ieq, 
       b'^=': lambda c, a, b: qs(a).startswith(qs(b)), 
       b'$=': lambda c, a, b: qs(a).endswith(qs(b)), 
       b'in': in_, 
       b'not in': notin_, 
       b'contains': contains_, 
       b'icontains': icontains_}

    def __init__(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        self.operator_eval = [ (self.opMap[op], val.eval) for op, val in pairs(self.value[1:]) ]

    def eval(self, archive, context, app, exp_context):
        val1 = self._eval(archive, context, app, exp_context)
        for op_func, _eval in self.operator_eval:
            val2 = _eval(archive, context, app, exp_context)
            val1 = op_func(context, val1, val2)

        return val1


class EvalLogicOpAND(object):

    def __init__(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        self.operator_eval = [ val.eval for op, val in pairs(self.value[1:]) ]

    def eval(self, archive, context, app, exp_context):
        val1 = self._eval(archive, context, app, exp_context)
        for _eval in self.operator_eval:
            val2 = _eval(archive, context, app, exp_context)
            val1 = and_(val1, val2)

        return val1


class EvalLogicOpOR(object):

    def __init__(self, tokens):
        self.value = tokens[0]
        self._eval = self.value[0].eval
        self.operator_eval = [ val.eval for op, val in pairs(self.value[1:]) ]

    def eval(self, archive, context, app, exp_context):
        val1 = self._eval(archive, context, app, exp_context)
        for _eval in self.operator_eval:
            val2 = _eval(archive, context, app, exp_context)
            val1 = or_(val1, val2)

        return val1


class EvalGroupOp(object):

    def __init__(self, tokens):
        self._evals = [ t.eval for t in tokens[0][0::2] ]

    def eval(self, archive, context, app, exp_context):
        val = [ eval(archive, context, app, exp_context) for eval in self._evals ]
        return val


class EvalNotOp(object):
    """Class to evaluate expressions with logical NOT"""

    def __init__(self, tokens):
        self._eval = tokens[0][1].eval

    def eval(self, archive, context, app, exp_context):
        return not_(self._eval(archive, context, app, exp_context))


integer = Word(nums)
real = Combine(Word(nums) + b'.' + Word(nums))
constant = (Literal(b'True') | Literal(b'False') | Literal(b'None') | Literal(b'yes') | Literal(b'no')) + WordEnd()
model_reference = Regex(b'([\\w\\.]*#[\\w\\.]+)')
variable = Regex(b'([a-zA-Z0-9\\._]+)')
string = QuotedString(b'"', escChar=b'\\') | QuotedString(b"'", escChar=b'\\')
operand = model_reference | real | integer | constant | string | variable
plusop = oneOf(b'+ -')
multop = oneOf(b'* / // %')
groupop = Literal(b',')
expr = Forward()
notop = Literal(b'not') + WordEnd()
modifier = Combine(Word(alphas + nums) + b':')
integer.setParseAction(EvalInteger)
real.setParseAction(EvalReal)
string.setParseAction(EvalString)
constant.setParseAction(EvalConstant)
variable.setParseAction(EvalVariable)
model_reference.setParseAction(EvalModelReference)
comparisonop = oneOf(b'< <= > >= != == ~= ^= $=') | Literal(b'not in') + WordEnd() | oneOf(b'in lt lte gt gte matches contains icontains like ilike') + WordEnd()
logicopOR = Literal(b'or') + WordEnd()
logicopAND = Literal(b'and') + WordEnd()
expr << operatorPrecedence(operand, [
 (
  notop, 1, opAssoc.RIGHT, EvalNotOp),
 (
  modifier, 1, opAssoc.RIGHT, EvalModifierOp),
 (
  multop, 2, opAssoc.LEFT, EvalMultOp),
 (
  plusop, 2, opAssoc.LEFT, EvalAddOp),
 (
  comparisonop, 2, opAssoc.LEFT, EvalComparisonOp),
 (
  logicopAND, 2, opAssoc.LEFT, EvalLogicOpAND),
 (
  logicopOR, 2, opAssoc.LEFT, EvalLogicOpOR),
 (
  groupop, 2, opAssoc.LEFT, EvalGroupOp)])

@implements_to_string
class DBExpression(object):
    exp_cache = {}
    _lock = threading.Lock()

    def __init__(self, exp):
        self.exp = exp

    def __repr__(self):
        return b'<DBExpression "%s">' % self.exp

    def __str__(self):
        return self.exp

    def eval(self, archive, context, app=None):
        exp_context = ExpressionContext(self.exp)
        try:
            eval = self.compile_cache(self.exp)
            result = eval(archive, context, app, exp_context)
        except DBEvalError as e:
            raise DBExpressionError(self.exp, text_type(e))

        return result

    def eval2(self, archive, context, app=None):
        exp_context = ExpressionContext(self.exp)
        try:
            eval = self.compile_cache(self.exp)
            result = eval(archive, context, app, exp_context)
        except DBEvalError as e:
            raise DBExpressionError(self.exp, text_type(e))

        return (
         result, exp_context)

    def compile(self):
        return self.compile_cache(self.exp)

    def compile_cache(self, exp):
        with self._lock:
            try:
                return self.exp_cache[exp]
            except KeyError:
                try:
                    compiled_exp = expr.parseString(exp, parseAll=True)
                except ParseException as e:
                    raise DBExpressionError(exp, text_type(e), col=e.col)

                eval = self.exp_cache[exp] = compiled_exp[0].eval
                return eval


if __name__ == b'__main__':
    exp = DBExpression(b"moya.auth#User.username=='will'")
    print(exp.compile())
    exp = DBExpression(b"auth#User.username=='will'")
    print(exp.compile())
    exp = DBExpression(b'comments#Comment.namespace == app.name and comments#Comment.object in comment_keys')
    print(exp.compile())
    exp = DBExpression(b'#CommentObject.count + 1')
    print(exp.compile)