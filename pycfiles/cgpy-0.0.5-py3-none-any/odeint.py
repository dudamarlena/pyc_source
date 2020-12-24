# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\cgp\cvodeint\odeint.py
# Compiled at: 2011-11-08 05:11:38
__doc__ = '\nSimple replacement for :func:`scipy.integrate.odeint` based on Sundials.\n\nSee :func:`odeint`.\n'
from .core import Cvodeint

def odeint(func, y0_in, t_in, args=()):
    """
    Simple replacement for scipy.integrate.odeint() based on Sundials.
    
    Example from http://www.scipy.org/SciPyPackages/Integrate
    
    >>> from scipy import *
    >>> from pylab import *
    >>> deriv = lambda y,t : array([y[1],-y[0]])
    >>> # Integration parameters
    >>> start=0
    >>> end=10
    >>> numsteps=10000
    >>> time=linspace(start,end,numsteps)
    >>> from scipy import integrate
    >>> y0=array([0.0005,0.2])
    >>> y=integrate.odeint(deriv,y0,time)
    >>> plot(time,y[:,0])                                  # doctest: +SKIP
    >>> show()                                             # doctest: +SKIP
    >>> y2=odeint(deriv,y0,time)                           # should equal y
    >>> print "%.5e" % abs((y - y2).max())                 # should be small
    6.82502e-07
    """

    def ode(t, y, ydot, f_data):
        """Right-hand side."""
        ydot[:] = func(y, t, args) if args else func(y, t)
        return 0

    cvodeint = Cvodeint(ode, t_in, y0_in)
    result = cvodeint.integrate()
    return result[1]


if __name__ == '__main__':
    import doctest
    doctest.testmod()