# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/safeeval.py
# Compiled at: 2019-08-19 15:09:29
"""
safeeval.py: Safe eval replacement with whitelist support
"""
from __future__ import print_function
from builtins import range
from builtins import object
__all__ = [
 'SafeEvaluator']
__docformat__ = 'restructuredtext'

class SafeEvaluator(object):
    """This class provides a safe eval replacement.

    The method eval() will only evaluate the expressions considered safe (whitelisted).
    By default it has a whitelist of mathematical expressions that can be turn off using defaultSafe=False at init

    The user can add more safe functions passing a safedict to the addSafe() or init methods.

    Functions can be removed by name using removeSafe()

    Note: In order to use variables defined outside, the user must explicitly declare them safe.
    """

    def __init__(self, safedict=None, defaultSafe=True):
        self._default_numpy = ('abs', 'array', 'arange', 'arccos', 'arcsin', 'arctan',
                               'arctan2', 'average', 'ceil', 'cos', 'cosh', 'degrees',
                               'dot', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp',
                               'hypot', 'ldexp', 'linspace', 'log', 'log10', 'logspace',
                               'modf', 'ones', 'pi', 'radians', 'shape', 'sin', 'sinh',
                               'sqrt', 'sum', 'tan', 'tanh', 'zeros')
        self._default_numpy_random = ('randn', 'rand', 'randint')
        if safedict is None:
            safedict = {}
        self.safe_dict = safedict
        if defaultSafe:
            import numpy
            from taurus.core.units import Quantity, UR
            self.safe_dict['pow'] = pow
            self.safe_dict['len'] = len
            self.safe_dict['int'] = int
            self.safe_dict['float'] = float
            self.safe_dict['bool'] = bool
            self.safe_dict['str'] = str
            self.safe_dict['bytes'] = bytes
            self.safe_dict['list'] = list
            self.safe_dict['range'] = range
            self.safe_dict['True'] = True
            self.safe_dict['False'] = False
            self.safe_dict['None'] = None
            for n in self._default_numpy:
                self.safe_dict[n] = getattr(numpy, n)

            for n in self._default_numpy_random:
                self.safe_dict[n] = getattr(numpy.random, n)

            self.safe_dict['Quantity'] = Quantity
            self.safe_dict['Q'] = Quantity
            self.safe_dict['UR'] = UR
        self._originalSafeDict = self.safe_dict.copy()
        return

    def eval(self, expr):
        """safe eval"""
        return eval(expr, {'__builtins__': None}, self.safe_dict)

    def addSafe(self, safedict, permanent=False):
        """The values in safedict will be evaluable (whitelisted)
        The safedict is as follows: {"eval_name":object, ...}. The evaluator will interpret eval_name as object.
        """
        self.safe_dict.update(safedict)
        if permanent:
            self._originalSafeDict.update(safedict)

    def removeSafe(self, name, permanent=False):
        """Removes an object from the whitelist"""
        self.safe_dict.pop(name)
        if permanent:
            try:
                self._originalSafeDict.pop(name)
            except KeyError:
                pass

    def resetSafe(self):
        """restores the safe dict with wich the evaluator was instantiated"""
        self.safe_dict = self._originalSafeDict.copy()

    def getSafe(self):
        """returns the currently whitelisted expressions"""
        return self.safe_dict


if __name__ == '__main__':
    x = list(range(6))
    sev = SafeEvaluator()
    print('trying to evaluate a variable that has not been registered')
    try:
        print(sev.safeEval('x+2'))
    except:
        print('failed!!')

    sev.addSafe({'x': x})
    f0 = 'x'
    f1 = 'sqrt(x)'
    f2 = 'pow(2,8)'
    f3 = 'ceil(array(x)/2.)'
    f4 = 'x[3]*2'
    f5 = 'open("/etc/passwd")'
    for f in [f0, f1, f2, f3, f4, f5]:
        print('Evaluating "%s":' % f)
        try:
            print(sev.eval(f))
        except:
            print('ERROR: %s cannot be evaluated' % f)

    import numpy
    vector = numpy.arange(6)
    sev2 = SafeEvaluator({'x': x, 'y': vector}, defaultSafe=False)
    print('x*y=', sev2.eval('x*y'))
    y = 0
    print('x*y=', sev2.eval('x*y'))