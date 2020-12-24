# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\ParsedExpr.py
# Compiled at: 2006-12-26 13:39:47
__doc__ = '\nThe implementation of parsed XPath expression tokens.\n\nCopyright 2005 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import types, inspect
from xml.dom import Node
from Ft.Lib import boolean, number
from Ft.Lib.Set import Union, Unique
from Ft.Xml import EMPTY_NAMESPACE
from Ft.Xml.Lib.XmlString import SplitQName, XmlStrStrip
from Ft.Xml.XPath import RuntimeException
from Ft.Xml.XPath import ParsedStep, ParsedAxisSpecifier, ParsedNodeTest
from Ft.Xml.XPath import Conversions, _comparisons
from Ft.Xml.XPath import XPathTypes as Types

class ParsedLiteralExpr:
    """
    An object representing a string literal expression
    (XPath 1.0 grammar production 29: Literal)
    """
    __module__ = __name__

    def __init__(self, literal):
        if len(literal) >= 2 and literal[0] in ["'", '"'] and literal[0] == literal[(-1)]:
            literal = literal[1:-1]
        self._literal = literal

    def evaluate(self, context):
        return self._literal

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<Literal at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return '"' + self._literal.encode('unicode_escape') + '"'


class ParsedNLiteralExpr(ParsedLiteralExpr):
    """
    An object representing a numeric literal expression
    (XPath 1.0 grammar production 30: Number)
    """
    __module__ = __name__

    def __init__(self, nliteral):
        self._nliteral = nliteral
        self._literal = float(nliteral)

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<Number at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if number.isnan(self._literal):
            return 'NaN'
        elif number.isinf(self._literal):
            if self._literal < 0:
                return '-Infinity'
            else:
                return 'Infinity'
        else:
            return str(self._nliteral)


class ParsedVariableReferenceExpr:
    """
    An object representing a variable reference expression
    (XPath 1.0 grammar production 36: VariableReference)
    """
    __module__ = __name__

    def __init__(self, name):
        self._name = name
        self._key = SplitQName(name[1:])
        return

    def evaluate(self, context):
        """Returns a string"""
        (prefix, local) = self._key
        if prefix:
            try:
                expanded = (
                 context.processorNss[prefix], local)
            except KeyError:
                raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)

        else:
            expanded = self._key
        try:
            return context.varBindings[expanded]
        except KeyError:
            raise RuntimeException(RuntimeException.UNDEFINED_VARIABLE, expanded[0], expanded[1])

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<Variable at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return self._name


def ParsedFunctionCallExpr(name, args):
    """
    Returns an object representing a function call expression
    (XPath 1.0 grammar production 16: FunctionCall)
    """
    name = XmlStrStrip(name)
    key = SplitQName(name)
    if not args:
        return FunctionCall(name, key, args)
    count = len(args)
    if count == 1:
        return FunctionCall1(name, key, args)
    elif count == 2:
        return FunctionCall2(name, key, args)
    elif count == 3:
        return FunctionCall3(name, key, args)
    else:
        return FunctionCallN(name, key, args)


class FunctionCall:
    """
    An object representing a function call expression
    (XPath 1.0 grammar production 16: FunctionCall)
    """
    __module__ = __name__

    def __init__(self, name, key, args):
        self._name = name
        self._key = key
        self._args = args
        self._func = None
        return

    def pprint(self, indent=''):
        print indent + str(self)
        for arg in self._args:
            arg.pprint(indent + '  ')

    def error(self, *args):
        raise RuntimeException(RuntimeException.UNDEFINED_FUNCTION, self._name)

    def getArgumentError(self):
        if not inspect.isfunction(self._func):
            return None
        argcount = len(self._args)
        (args, vararg, kwarg) = inspect.getargs(self._func.func_code)
        defaults = self._func.func_defaults or ()
        maxargs = len(args) - 1
        minargs = maxargs - len(defaults)
        if argcount > maxargs and not vararg:
            if maxargs == 0:
                return RuntimeException(RuntimeException.ARGCOUNT_NONE, self._name, argcount)
            elif defaults:
                return RuntimeException(RuntimeException.ARGCOUNT_ATMOST, self._name, maxargs, argcount)
            else:
                return RuntimeException(RuntimeException.ARGCOUNT_EXACT, self._name, maxargs, argcount)
        elif argcount < minargs:
            if defaults or vararg:
                return RuntimeException(RuntimeException.ARGCOUNT_ATLEAST, self._name, minargs, argcount)
            else:
                return RuntimeException(RuntimeException.ARGCOUNT_EXACT, self._name, minargs, argcount)
        return None
        return

    def evaluate(self, context):
        """Returns the result of calling the function"""
        func = self._func
        if func is None:
            (prefix, local) = self._key
            if prefix:
                try:
                    expanded = (
                     context.processorNss[prefix], local)
                except:
                    raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)

            else:
                expanded = self._key
            func = context.functions.get(expanded, self.error)
            if not ('nocache' in func.__dict__ and func.nocache):
                self._func = func
        try:
            result = func(context)
        except TypeError:
            exception = self.getArgumentError()
            if not exception:
                raise
            raise exception

        return result
        return

    def __getinitargs__(self):
        return (
         self._name, self._key, self._args)

    def __getstate__(self):
        state = vars(self).copy()
        del state['_func']
        return state

    def __str__(self):
        return '<%s at %x: %s>' % (self.__class__.__name__, id(self), repr(self))

    def __repr__(self):
        result = self._name + '('
        if len(self._args):
            result = result + repr(self._args[0])
            for arg in self._args[1:]:
                result = result + ', ' + repr(arg)

        return result + ')'


class FunctionCall1(FunctionCall):
    __module__ = __name__

    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        func = self._func
        if func is None:
            (prefix, local) = self._key
            if prefix:
                try:
                    expanded = (
                     context.processorNss[prefix], local)
                except:
                    raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)

            else:
                expanded = self._key
            func = context.functions.get(expanded, self.error)
            if not ('nocache' in func.__dict__ and func.nocache):
                self._func = func
        try:
            result = func(context, arg0)
        except TypeError:
            exception = self.getArgumentError()
            if not exception:
                raise
            raise exception

        return result
        return


class FunctionCall2(FunctionCall):
    __module__ = __name__

    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]
        self._arg1 = args[1]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        arg1 = self._arg1.evaluate(context)
        func = self._func
        if func is None:
            (prefix, local) = self._key
            if prefix:
                try:
                    expanded = (
                     context.processorNss[prefix], local)
                except:
                    raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)

            else:
                expanded = self._key
            func = context.functions.get(expanded, self.error)
            if not ('nocache' in func.__dict__ and func.nocache):
                self._func = func
        try:
            result = func(context, arg0, arg1)
        except TypeError:
            exception = self.getArgumentError()
            if not exception:
                raise
            raise exception

        return result
        return


class FunctionCall3(FunctionCall):
    __module__ = __name__

    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)
        self._arg0 = args[0]
        self._arg1 = args[1]
        self._arg2 = args[2]

    def evaluate(self, context):
        arg0 = self._arg0.evaluate(context)
        arg1 = self._arg1.evaluate(context)
        arg2 = self._arg2.evaluate(context)
        func = self._func
        if func is None:
            (prefix, local) = self._key
            if prefix:
                try:
                    expanded = (
                     context.processorNss[prefix], local)
                except:
                    raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)

            else:
                expanded = self._key
            func = context.functions.get(expanded, self.error)
            if not ('nocache' in func.__dict__ and func.nocache):
                self._func = func
        try:
            result = func(context, arg0, arg1, arg2)
        except TypeError:
            exception = self.getArgumentError()
            if not exception:
                raise
            raise exception

        return result
        return


class FunctionCallN(FunctionCall):
    __module__ = __name__

    def __init__(self, name, key, args):
        FunctionCall.__init__(self, name, key, args)

    def evaluate(self, context):
        args = map(lambda arg, c=context: arg.evaluate(c), self._args)
        func = self._func
        if func is None:
            (prefix, local) = self._key
            if prefix:
                try:
                    expanded = (
                     context.processorNss[prefix], local)
                except:
                    raise RuntimeException(RuntimeException.UNDEFINED_PREFIX, prefix)

            else:
                expanded = self._key
            func = context.functions.get(expanded, self.error)
            if not ('nocache' in func.__dict__ and func.nocache):
                self._func = func
        try:
            result = func(context, *args)
        except TypeError:
            exception = self.getArgumentError()
            if not exception:
                raise
            raise exception

        return result
        return


class ParsedUnionExpr:
    """
    An object representing a union expression
    (XPath 1.0 grammar production 18: UnionExpr)
    """
    __module__ = __name__

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        """Returns a node-set"""
        left = self._left.evaluate(context)
        if not isinstance(left, Types.NodesetType):
            raise TypeError('%s must be a node-set, not a %s' % (repr(self._left),
             Types.g_xpathPrimitiveTypes.get(type(left), type(left).__name__)))
        right = self._right.evaluate(context)
        if not isinstance(right, Types.NodesetType):
            raise TypeError('%s must be a node-set, not a %s' % (repr(self._right),
             Types.g_xpathPrimitiveTypes.get(type(right), type(right).__name__)))
        set = Union(left, right)
        return set

    def __str__(self):
        return '<UnionExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._left) + ' | ' + repr(self._right)


class ParsedPathExpr:
    """
    An object representing a path expression
    (XPath 1.0 grammar production 19: PathExpr)
    """
    __module__ = __name__

    def __init__(self, descendant, left, right):
        self._descendant = descendant
        self._left = left
        self._right = right
        return

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def _descendants(self, context, nodeset):
        for child in context.node.childNodes:
            context.node = child
            results = self._right.select(context)
            if not isinstance(results, Types.NodesetType):
                raise TypeError('%r must be a node-set, not a %s' % (self._right,
                 Types.g_xpathPrimitiveTypes.get(type(results), type(results).__name__)))
            if results:
                nodeset.extend(results)
            if child.nodeType == Node.ELEMENT_NODE:
                nodeset = self._descendants(context, nodeset)

        return nodeset

    def evaluate(self, context):
        """Returns a node-set"""
        left = self._left.evaluate(context)
        if not isinstance(left, Types.NodesetType):
            raise TypeError('%r must be a node-set, not a %s' % (self._left,
             Types.g_xpathPrimitiveTypes.get(type(left), type(left).__name__)))
        state = context.copy()
        results = []
        for node in left:
            context.node = node
            nodeset = self._right.select(context)
            if not isinstance(nodeset, Types.NodesetType):
                raise TypeError('%r must be a node-set, not a %s' % (self._right,
                 Types.g_xpathPrimitiveTypes.get(type(nodeset), type(nodeset).__name__)))
            elif self._descendant:
                nodeset = self._descendants(context, nodeset)
            results.extend(nodeset)

        results = Unique(results)
        context.set(state)
        return results

    def __str__(self):
        return '<PathExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        op = self._descendant and '//' or '/'
        return repr(self._left) + op + repr(self._right)


class ParsedFilterExpr:
    """
    An object representing a filter expression
    (XPath 1.0 grammar production 20: FilterExpr)
    """
    __module__ = __name__

    def __init__(self, filter_, predicates):
        self._filter = filter_
        self._predicates = predicates
        return

    def evaluate(self, context):
        """Returns a node-set"""
        nodeset = self._filter.evaluate(context)
        if not isinstance(nodeset, Types.NodesetType):
            raise TypeError('%s must be a node-set, not a %s' % (repr(self._filter),
             Types.g_xpathPrimitiveTypes.get(type(nodeset), type(nodeset).__name__)))
        if nodeset:
            nodeset.sort()
            nodeset = self._predicates.filter(nodeset, context, reverse=0)
        return nodeset

    def pprint(self, indent=''):
        print indent + str(self)
        self._filter.pprint(indent + '  ')
        self._predicates.pprint(indent + '  ')

    def shiftContext(self, context, index, set, len, func):
        return func(context)

    def __str__(self):
        return '<FilterExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._filter) + repr(self._predicates)


class ParsedOrExpr:
    """
    An object representing an or expression
    (XPath 1.0 grammar production 21: OrExpr)
    """
    __module__ = __name__

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        """Returns a boolean"""
        rt = Conversions.BooleanValue(self._left.evaluate(context))
        if not rt:
            rt = Conversions.BooleanValue(self._right.evaluate(context))
        return rt

    def __str__(self):
        return '<OrExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._left) + ' or ' + repr(self._right)


class ParsedAndExpr:
    """
    An object representing an and expression
    (XPath 1.0 grammar production 22: AndExpr)
    """
    __module__ = __name__

    def __init__(self, left, right):
        self._left = left
        self._right = right

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def evaluate(self, context):
        """Returns a boolean"""
        rt = Conversions.BooleanValue(self._left.evaluate(context))
        if rt:
            rt = Conversions.BooleanValue(self._right.evaluate(context))
        return rt

    def __str__(self):
        return '<AndExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return repr(self._left) + ' and ' + repr(self._right)


def _nodeset_compare(compare, a, b, relational=False):
    """
    Applies a comparison function to node-sets a and b
    in order to evaluate equality (=, !=) and relational (<, <=, >=, >)
    expressions in which both objects to be compared are node-sets.

    Returns an XPath boolean indicating the result of the comparison.
    """
    if isinstance(a, Types.NodesetType) and isinstance(b, Types.NodesetType):
        if not (a and b):
            return boolean.false
        if relational:
            coerce = Conversions.NumberValue
        else:
            coerce = Conversions.StringValue
        a = map(coerce, a)
        b = map(coerce, b)
        for left in a:
            for right in b:
                if compare(left, right):
                    return boolean.true

        return boolean.false
    if isinstance(a, Types.NodesetType):
        if isinstance(b, Types.BooleanType):
            a = Conversions.BooleanValue(a)
            return compare(a, b) and boolean.true or boolean.false
        elif relational:
            b = Conversions.NumberValue(b)
            coerce = Conversions.NumberValue
        elif isinstance(b, Types.NumberType):
            coerce = Conversions.NumberValue
        else:
            b = Conversions.StringValue(b)
            coerce = Conversions.StringValue
        for node in a:
            if compare(coerce(node), b):
                return boolean.true

    elif isinstance(a, Types.BooleanType):
        b = Conversions.BooleanValue(b)
        return compare(a, b) and boolean.true or boolean.false
    elif relational:
        a = Conversions.NumberValue(a)
        coerce = Conversions.NumberValue
    elif isinstance(a, Types.NumberType):
        coerce = Conversions.NumberValue
    else:
        a = Conversions.StringValue(a)
        coerce = Conversions.StringValue
    for node in b:
        if compare(a, coerce(node)):
            return boolean.true

    return boolean.false


class ParsedEqualityExpr:
    """
    An object representing an equality expression
    (XPath 1.0 grammar production 23: EqualityExpr)
    """
    __module__ = __name__

    def __init__(self, op, left, right):
        self._op = op
        self._left = left
        self._right = right
        if op == '=':
            self._cmp = _comparisons.eq
        else:
            self._cmp = _comparisons.ne

    def __getstate__(self):
        return (
         self._op, self._left, self._right)

    def __setstate__(self, state):
        self.__init__(*state)

    def evaluate(self, context):
        """Returns a boolean"""
        left = self._left.evaluate(context)
        right = self._right.evaluate(context)
        if isinstance(left, Types.NodesetType) or isinstance(right, Types.NodesetType):
            return _nodeset_compare(self._cmp, left, right)
        if isinstance(left, Types.BooleanType):
            right = Conversions.BooleanValue(right)
        elif isinstance(right, Types.BooleanType):
            left = Conversions.BooleanValue(left)
        elif isinstance(left, Types.NumberType):
            right = Conversions.NumberValue(right)
        elif isinstance(right, Types.NumberType):
            left = Conversions.NumberValue(left)
        else:
            left = Conversions.StringValue(left)
            right = Conversions.StringValue(right)
        return self._cmp(left, right) and boolean.true or boolean.false

    def pprint(self, indent=''):
        print indent + str(self)
        self._left.pprint(indent + '  ')
        self._right.pprint(indent + '  ')

    def __str__(self):
        return '<EqualityExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if self._op == '=':
            op = ' = '
        else:
            op = ' != '
        return repr(self._left) + op + repr(self._right)


class ParsedRelationalExpr:
    """
    An object representing a relational expression
    (XPath 1.0 grammar production 24: RelationalExpr)
    """
    __module__ = __name__

    def __init__(self, opcode, left, right):
        self._op = opcode
        self._left = left
        self._right = right
        if opcode == 0:
            self._cmp = _comparisons.lt
        elif opcode == 1:
            self._cmp = _comparisons.le
        elif opcode == 2:
            self._cmp = _comparisons.gt
        elif opcode == 3:
            self._cmp = _comparisons.ge
        return

    def __getstate__(self):
        return (
         self._op, self._left, self._right)

    def __setstate__(self, state):
        self.__init__(*state)

    def evaluate(self, context):
        """Returns a boolean"""
        left = self._left.evaluate(context)
        right = self._right.evaluate(context)
        if isinstance(left, Types.NodesetType) or isinstance(right, Types.NodesetType):
            return _nodeset_compare(self._cmp, left, right, relational=True)
        left = Conversions.NumberValue(left)
        right = Conversions.NumberValue(right)
        return self._cmp(left, right) and boolean.true or boolean.false

    def pprint(self, indent=''):
        print indent + str(self)
        if type(self._left) == types.InstanceType:
            self._left.pprint(indent + '  ')
        else:
            print indent + '  ' + '<Primitive: %s>' % str(self._left)
        if type(self._right) == types.InstanceType:
            self._right.pprint(indent + '  ')
        else:
            print indent + '  ' + '<Primitive: %s>' % str(self._right)

    def __str__(self):
        return '<RelationalExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if self._op == 0:
            op = ' < '
        elif self._op == 1:
            op = ' <= '
        elif self._op == 2:
            op = ' > '
        elif self._op == 3:
            op = ' >= '
        return repr(self._left) + op + repr(self._right)


class ParsedAdditiveExpr:
    """
    An object representing an additive expression
    (XPath 1.0 grammar production 25: AdditiveExpr)
    """
    __module__ = __name__

    def __init__(self, sign, left, right):
        self._sign = sign
        self._leftLit = 0
        self._rightLit = 0
        if isinstance(left, ParsedLiteralExpr):
            self._leftLit = 1
            self._left = Conversions.NumberValue(left.evaluate(None))
        else:
            self._left = left
        if isinstance(right, ParsedLiteralExpr):
            self._rightLit = 1
            self._right = Conversions.NumberValue(right.evaluate(None))
        else:
            self._right = right
        return
        return

    def evaluate(self, context):
        """Returns a number"""
        if self._leftLit:
            lrt = self._left
        else:
            lrt = self._left.evaluate(context)
            lrt = Conversions.NumberValue(lrt)
        if self._rightLit:
            rrt = self._right
        else:
            rrt = self._right.evaluate(context)
            rrt = Conversions.NumberValue(rrt)
        return lrt + rrt * self._sign

    def pprint(self, indent=''):
        print indent + str(self)
        if type(self._left) == types.InstanceType:
            self._left.pprint(indent + '  ')
        else:
            print indent + '  ' + '<Primitive: %s>' % str(self._left)
        if type(self._right) == types.InstanceType:
            self._right.pprint(indent + '  ')
        else:
            print indent + '  ' + '<Primitive: %s>' % str(self._right)

    def __str__(self):
        return '<AdditiveExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if self._sign > 0:
            op = ' + '
        else:
            op = ' - '
        return repr(self._left) + op + repr(self._right)


class ParsedMultiplicativeExpr:
    """
    An object representing an multiplicative expression
    (XPath 1.0 grammar production 26: MultiplicativeExpr)
    """
    __module__ = __name__

    def __init__(self, opcode, left, right):
        self._op = opcode
        self._left = left
        self._right = right

    def evaluate(self, context):
        """Returns a number"""
        lrt = self._left.evaluate(context)
        lrt = Conversions.NumberValue(lrt)
        rrt = self._right.evaluate(context)
        rrt = Conversions.NumberValue(rrt)
        res = 0
        if self._op == 0:
            res = lrt * rrt
        elif self._op == 1:
            try:
                res = lrt / rrt
            except ZeroDivisionError:
                if lrt < 0:
                    res = -number.inf
                elif lrt == 0:
                    res = number.nan
                else:
                    res = number.inf

        elif self._op == 2:
            try:
                res = lrt % rrt
            except ZeroDivisionError:
                res = number.nan

        return res

    def pprint(self, indent=''):
        print indent + str(self)
        if type(self._left) == types.InstanceType:
            self._left.pprint(indent + '  ')
        else:
            print indent + '  ' + '<Primitive: %s>' % str(self._left)
        if type(self._right) == types.InstanceType:
            self._right.pprint(indent + '  ')
        else:
            print indent + '  ' + '<Primitive: %s>' % str(self._right)

    def __str__(self):
        return '<MultiplicativeExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        if self._op == 0:
            op = ' * '
        elif self._op == 1:
            op = ' div '
        elif self._op == 2:
            op = ' mod '
        return repr(self._left) + op + repr(self._right)


class ParsedUnaryExpr:
    """
    An object representing a unary expression
    (XPath 1.0 grammar production 27: UnaryExpr)
    """
    __module__ = __name__

    def __init__(self, exp):
        self._exp = exp

    def evaluate(self, context):
        """Returns a number"""
        exp = self._exp.evaluate(context)
        exp = Conversions.NumberValue(exp)
        return exp * -1.0

    def pprint(self, indent=''):
        print indent + str(self)

    def __str__(self):
        return '<UnaryExpr at %x: %s>' % (id(self), repr(self))

    def __repr__(self):
        return '-' + repr(self._exp)