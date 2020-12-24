# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pysde/StringFunction.py
# Compiled at: 2016-09-09 22:45:16
# Size of source mod 2**32: 7011 bytes
"""Make a string mathematical expression behave as a Python function."""
from math import *

class StringFunction1x:
    __doc__ = '\n    Make a string expression behave as a Python function\n    of one variable.\n    Examples on usage:\n    >>> from StringFunction import StringFunction1x\n    >>> f = StringFunction1x(\'sin(3*x) + log(1+x)\')\n    >>> p = 2.0; v = f(p)  # evaluate function\n    >>> p, v\n    (2.0, 0.8191967904691839)\n    >>> f = StringFunction1x(\'1+t\', independent_variable=\'t\')\n    >>> v = f(1.2)  # evaluate function of t=1.2\n    >>> print("%.2f" % v)\n    2.20\n    >>> f = StringFunction1x(\'sin(t)\')\n    >>> v = f(1.2)  # evaluate function of t=1.2\n    Traceback (most recent call last):\n        v = f(1.2)\n    NameError: name \'t\' is not defined\n    >>> f = StringFunction1x(\'a+b*x\', set_parameters=\'a=1; b=4\')\n    >>> f(2)   # 1 + 4*2\n    9\n    '

    def __init__(self, expression, independent_variable='x', set_parameters=''):
        self._f = expression
        self._var = independent_variable
        self.__name__ = self._f
        self._code = set_parameters

    def set_parameters(self, code):
        self._code = code

    def __call__(self, x):
        exec('%s = %g' % (self._var, x))
        if self._code:
            exec(self._code)
        return eval(self._f)


class StringFunction_alt(StringFunction1x):
    __doc__ = "\n    Extension of class StringFunction1 to an arbitrary\n    number of independent variables.\n    \n    Example on usage:\n    \n    >>> from StringFunction import StringFunction_alt\n    >>> f = StringFunction_alt('1+sin(2*x)')\n    >>> f(1.2)\n    1.675463180551151\n    >>> f = StringFunction_alt('1+sin(2*t)', independent_variables='t')\n    >>> f(1.2)\n    1.675463180551151\n    >>> f = StringFunction_alt('1+A*sin(w*t)', independent_variables='t',                                set_parameters='A=0.1; w=3.14159')\n    >>> f(1.2)\n    0.9412217323869594\n    >>> f.set_parameters('A=1; w=1')\n    >>> f(1.2)\n    1.9320390859672263\n    >>> # function of two variables:\n    >>> f = StringFunction_alt('1+sin(2*x)*cos(y)',                                independent_variables=('x','y'))\n    >>> f(1.2,-1.1)\n    1.3063874788637866\n    >>> f = StringFunction_alt('1+V*sin(w*x)*exp(-b*t)',                                independent_variables=('x','t'))\n    >>> f.set_parameters('V=0.1; w=1; b=0.1')\n    >>> f(1.0,0.1)\n    1.0833098208613807\n    "

    def __init__(self, expression, independent_variables='x', set_parameters=''):
        StringFunction1x.__init__(self, expression, independent_variables, set_parameters)

    def __call__(self, *args):
        vars = str(tuple(self._var)).replace("'", '')
        cmd = '%s = %s' % (vars, args)
        exec(cmd)
        if self._code:
            exec(self._code)
        return eval(self._f)


class StringFunction1:
    __doc__ = '\n    Make a string expression behave as a Python function\n    of one variable.\n    Examples on usage:\n    >>> from StringFunction import StringFunction1x\n    >>> f = StringFunction1(\'sin(3*x) + log(1+x)\')\n    >>> p = 2.0; v = f(p)  # evaluate function\n    >>> p, v\n    (2.0, 0.8191967904691839)\n    >>> f = StringFunction1(\'1+t\', independent_variable=\'t\')\n    >>> v = f(1.2)  # evaluate function of t=1.2\n    >>> print("%.2f" % v)\n    2.20\n    >>> f = StringFunction1(\'sin(t)\')\n    >>> v = f(1.2)  # evaluate function of t=1.2\n    Traceback (most recent call last):\n        v = f(1.2)\n    NameError: name \'t\' is not defined\n    >>> f = StringFunction1(\'a+b*x\', a=1, b=4)\n    >>> f(2)   # 1 + 4*2\n    9\n    >>> f.set_parameters(b=0)\n    >>> f(2)   # 1 + 0*2\n    1\n    '

    def __init__(self, expression, **kwargs):
        self._f = expression
        self._var = kwargs.get('independent_variable', 'x')
        self.__name__ = self._f
        self._prms = kwargs
        try:
            del self._prms['independent_variable']
        except:
            pass

        self._f_compiled = compile(self._f, '<string>', 'eval')

    def set_parameters(self, **kwargs):
        self._prms.update(kwargs)

    def __call__(self, x):
        self._prms[self._var] = x
        return eval(self._f_compiled, globals(), self._prms)


class StringFunction(StringFunction1):
    __doc__ = "\n    Extension of class StringFunction1 to an arbitrary\n    number of independent variables.\n\n    Example on usage:\n\n    >>> from StringFunction import StringFunction\n    >>> f = StringFunction('1+sin(2*x)')\n    >>> f(1.2)\n    1.675463180551151\n    >>> f = StringFunction('1+sin(2*t)', independent_variables='t')\n    >>> f(1.2)\n    1.675463180551151\n    >>> f = StringFunction('1+A*sin(w*t)', independent_variables='t',                            A=0.1, w=3.14159)\n    >>> f(1.2)\n    0.9412217323869594\n    >>> f.set_parameters(A=1, w=1)\n    >>> f(1.2)\n    1.9320390859672263\n    >>> # function of two variables:\n    >>> f = StringFunction('1+sin(2*x)*cos(y)',                            independent_variables=('x','y'))\n    >>> f(1.2,-1.1)\n    1.3063874788637866\n    >>> f = StringFunction('1+V*sin(w*x)*exp(-b*t)',                            independent_variables=('x','t'))\n    >>> f.set_parameters(V=0.1, w=1, b=0.1)\n    >>> f(1.0,0.1)\n    1.0833098208613807\n    >>> # vector field of x and y:\n    >>> f = StringFunction('[a+b*x,y]',                            independent_variables=('x','y'))\n    >>> f.set_parameters(a=1, b=2)\n    >>> f(2,1)  # [1+2*2, 1]\n    [5, 1]\n    \n    "

    def __init__(self, expression, **kwargs):
        StringFunction1.__init__(self, expression, **kwargs)
        self._var = tuple(kwargs.get('independent_variables', 'x'))
        try:
            del self._prms['independent_variables']
        except:
            pass

    def __call__(self, *args):
        for name, value in zip(self._var, args):
            self._prms[name] = value

        try:
            return eval(self._f_compiled, globals(), self._prms)
        except NameError(msg):
            raise NameError('%s; set its value by calling set_parameters' % msg)


def _test():
    import doctest, StringFunction
    return doctest.testmod(StringFunction)


def _try():
    f = StringFunction1('a+b*sin(x)', independent_variable='x', a=1, b=4)
    print(f(2))
    f.set_parameters(a=-1, b=pi)
    print(f(1))


if __name__ == '__main__':
    _test()