# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/pysde/StringFunction.py
# Compiled at: 2016-09-09 22:45:16
# Size of source mod 2**32: 7011 bytes
__doc__ = 'Make a string mathematical expression behave as a Python function.'
from math import *

class StringFunction1x:
    """StringFunction1x"""

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
    """StringFunction_alt"""

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
    """StringFunction1"""

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
    """StringFunction"""

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