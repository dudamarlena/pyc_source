# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\Xslt\Exslt\Math_.py
# Compiled at: 2006-12-26 13:39:48
__doc__ = '\nEXSLT 2.0 - Math (http://www.exslt.org/math/index.html)\n\nCopyright 2006 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
import math
from Ft.Lib import number
from Ft.Lib.Random import Random as _Random
from Ft.Xml.XPath import Conversions
from Ft.Xml.Xslt import XsltRuntimeException, Error
EXSL_MATH_NS = 'http://exslt.org/math'
CONSTANTS = {'PI': math.pi, 'E': math.e, 'SQRRT2': math.sqrt(2), 'LN2': math.log(2), 'LN10': math.log(10), 'LOG2E': 1 / math.log(2), 'SQRT1_2': math.sqrt(0.5)}

def _max(numbers):
    if not numbers or filter(number.isnan, numbers):
        return number.nan
    numbers.sort()
    return numbers[(-1)]


def _min(numbers):
    if not numbers or filter(number.isnan, numbers):
        return number.nan
    numbers.sort()
    return numbers[0]


def Abs(context, num):
    """
    The math:abs function returns the absolute value of a number.
    """
    return abs(Conversions.NumberValue(num))


def ACos(context, num):
    """
    The math:acos function returns the arccosine value of a number.
    """
    try:
        return math.acos(Conversions.NumberValue(num))
    except ValueError:
        return number.nan


def ASin(context, num):
    """
    The math:asin function returns the arcsine value of a number.
    """
    try:
        return math.asin(Conversions.NumberValue(num))
    except ValueError:
        return number.nan


def ATan(context, num):
    """
    The math:atan function returns the arctangent value of a number.
    """
    try:
        return math.atan(Conversions.NumberValue(num))
    except ValueError:
        return number.nan


def ATan2(context, y, x):
    """
    The math:atan2 function returns the angle ( in radians ) from the X axis
    to a point (y,x).
    """
    x = Conversions.NumberValue(x)
    y = Conversions.NumberValue(y)
    try:
        return math.atan2(y, x)
    except ValueError:
        return number.nan


def Constant(context, name, precision):
    """
    The math:constant function returns the specified constant to a set precision.
    """
    name = Conversions.StringValue(name)
    if not CONSTANTS.has_key(name):
        return number.nan
    precision = Conversions.NumberValue(precision)
    return float('%0.*f' % (int(precision), CONSTANTS[name]))


def Cos(context, num):
    """
    The math:cos function returns cosine of the passed argument.
    """
    return math.cos(Conversions.NumberValue(num))


def Exp(context, num):
    """
    The math:exp function returns e (the base of natural logarithms) raised to
    a power.
    """
    return math.exp(Conversions.NumberValue(num))


def Highest(context, nodeset):
    """
    The math:highest function returns the nodes in the node set whose value is
    the maximum value for the node set. The maximum value for the node set is
    the same as the value as calculated by math:max. A node has this maximum
    value if the result of converting its string value to a number as if by the
    number function is equal to the maximum value, where the equality
    comparison is defined as a numerical comparison using the = operator.
    """
    if type(nodeset) != type([]):
        raise XsltRuntimeException(Error.WRONG_ARGUMENT_TYPE, context.currentInstruction)
    numbers = map(Conversions.NumberValue, nodeset)
    max = _max(numbers[:])
    if number.isnan(max):
        return []
    result = []
    for i in xrange(len(nodeset)):
        if numbers[i] == max:
            result.append(nodeset[i])

    return result


def Log(context, num):
    """
    The math:log function returns the natural logarithm of a number.
    """
    return math.log(Conversions.NumberValue(num))


def Lowest(context, nodeset):
    """
    The math:lowest function returns the nodes in the node set whose value is
    the minimum value for the node set. The minimum value for the node set is
    the same as the value as calculated by math:min. A node has this minimum
    value if the result of converting its string value to a number as if by the
    number function is equal to the minimum value, where the equality
    comparison is defined as a numerical comparison using the = operator.
    """
    if type(nodeset) != type([]):
        raise XsltRuntimeException(Error.WRONG_ARGUMENT_TYPE, context.currentInstruction)
    numbers = map(Conversions.NumberValue, nodeset)
    min = _min(numbers[:])
    if number.isnan(min):
        return []
    result = []
    for i in xrange(len(nodeset)):
        if numbers[i] == min:
            result.append(nodeset[i])

    return result


def Max(context, nodeset):
    """
    The math:max function returns the maximum value of the nodes passed as
    the argument.
    """
    if type(nodeset) != type([]):
        raise XsltRuntimeException(Error.WRONG_ARGUMENT_TYPE, context.currentInstruction)
    numbers = map(Conversions.NumberValue, nodeset)
    return _max(numbers)


def Min(context, nodeset):
    """
    The math:min function returns the minimum value of the nodes passed as
    the argument.
    """
    if type(nodeset) != type([]):
        raise XsltRuntimeException(Error.WRONG_ARGUMENT_TYPE, context.currentInstruction)
    numbers = map(Conversions.NumberValue, nodeset)
    return _min(numbers)


def Power(context, base, exponent):
    """
    The math:power function returns the value of a base expression taken to
    a specified power.
    """
    return Conversions.NumberValue(base) ** Conversions.NumberValue(exponent)


def Random(context):
    """
    The math:random function returns a random number from 0 to 1.
    """
    return _Random()


def Sin(context, num):
    """
    The math:sin function returns the sine of the number.
    """
    return math.sin(Conversions.NumberValue(num))


def Sqrt(context, num):
    """
    The math:sqrt function returns the square root of a number.
    """
    n = Conversions.NumberValue(num)
    if number.isnan(n):
        return number.nan
    if n < 0.0:
        return 0.0
    try:
        return math.sqrt(Conversions.NumberValue(num))
    except ValueError:
        return 0.0


def Tan(context, num):
    """
    The math:tan function returns the tangent of the number passed as
    an argument.
    """
    return math.tan(Conversions.NumberValue(num))


ExtNamespaces = {EXSL_MATH_NS: 'math'}
ExtFunctions = {(EXSL_MATH_NS, 'abs'): Abs, (EXSL_MATH_NS, 'acos'): ACos, (EXSL_MATH_NS, 'asin'): ASin, (EXSL_MATH_NS, 'atan'): ATan, (EXSL_MATH_NS, 'atan2'): ATan2, (EXSL_MATH_NS, 'constant'): Constant, (EXSL_MATH_NS, 'cos'): Cos, (EXSL_MATH_NS, 'exp'): Exp, (EXSL_MATH_NS, 'highest'): Highest, (EXSL_MATH_NS, 'log'): Log, (EXSL_MATH_NS, 'lowest'): Lowest, (EXSL_MATH_NS, 'max'): Max, (EXSL_MATH_NS, 'min'): Min, (EXSL_MATH_NS, 'power'): Power, (EXSL_MATH_NS, 'random'): Random, (EXSL_MATH_NS, 'sin'): Sin, (EXSL_MATH_NS, 'sqrt'): Sqrt, (EXSL_MATH_NS, 'tan'): Tan}
ExtElements = {}