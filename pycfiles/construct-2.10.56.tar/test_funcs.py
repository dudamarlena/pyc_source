# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/constrNMPy/test_funcs.py
# Compiled at: 2017-10-18 06:28:42


def beales(x):
    """Beales function.
        
        Beales function given by
        
        .. math:: f(x,y)=(1.5-x+xy)^2+(2.25-x+xy^2)^2+(2.625-x+xy^3)^2
        
        See also https://en.wikipedia.org/wiki/Test_functions_for_optimization .
        
        Args:
                x (numpy.ndarray): 2-D input array.
        
        Returns:
                float: ``f(x,y)``.      
        """
    return (1.5 - x[0] + x[0] * x[1]) ** 2 + (2.25 - x[0] + x[0] * x[1] ** 2) ** 2 + (2.625 - x[0] + x[0] * x[1] ** 3) ** 2


def rosenbrock(x):
    """rosenbrock function.
        
        Rosenbrock function given by
        
        .. math:: f(x,y)=(1-x)^2+100(y-x^2)^2
        
        See also https://en.wikipedia.org/wiki/Test_functions_for_optimization .
        
        Args:
                x (numpy.ndarray): 2-D input array.
        
        Returns:
                float: ``f(x,y)``.      
        """
    return (1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2