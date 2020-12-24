# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\cvodeint\core.py
# Compiled at: 2013-01-14 06:47:43
"""
PySundials CVODE wrapper to automate routine steps of initializing, iterating...

Class :class:`Cvodeint` and its :meth:`~Cvodeint.integrate` method are the 
workhorses of this module. Importing with ``from cgp.cvodeint import *``
includes :class:`Cvodeint`, :exc:`CvodeException`, the :data:`flags` constants
and the :func:`cvodefun` decorator.

Simple example:

.. plot::
   :include-source:
   :width: 300
   
   from cgp.cvodeint import *
   cvodeint = Cvodeint(example_ode.exp_growth, t=[0,2], y=[0.1])
   t, y, flag = cvodeint.integrate()
   plt.plot(t, y, '.-')
   plt.xlabel("t")
   plt.ylabel("y")
   plt.title("$y = 0.1e^t$")

The module :mod:`.example_ode` defines some functions that are used in 
doctests. A replacement for :func:`scipy.integrate.odeint` is in module 
:mod:`.odeint`.

.. data:: flags

   CVODE return flags: dict of messages for each return value, as 
   returned by :func:`pysundials.cvode.CVodeGetReturnFlagName`.
"""
import traceback, ctypes
from pysundials import cvode
import numpy as np, logging
__all__ = (
 'CvodeException', 'Cvodeint', 'flags', 'cvodefun')
log = logging.getLogger('cvodeint')
log.addHandler(logging.StreamHandler())
fmtstr = '%(' + (')s\t%(').join(('asctime levelname name lineno process message').split()) + ')s'
log.handlers[0].setFormatter(logging.Formatter(fmtstr))
cv_ = dict([ (k, v) for k, v in cvode.__dict__.iteritems() if k.startswith('CV_')
           ])
flags = dict([ (v, [ k1 for k1, v1 in cv_.iteritems() if v1 == v ]) for v in np.unique(cv_.values())
             ])
del cv_
nv = cvode.NVector

class CvodeException(StandardError):
    """
    :func:`pysundials.cvode.CVode` returned a flag not in 
    ``[CV_SUCCESS, CV_TSTOP_RETURN, CV_ROOT_RETURN]``
    
    The CvodeException object has a *result* attribute for 
    ``t, Y, flag`` = results so far.
    If the right-hand side function is decorated with 
    :func:`cvodefun` and raised an exception, the traceback is 
    available as ``ode.exc``, where ``ode`` is the wrapped function.
    """

    def __init__(self, flag_or_msg=None, result=None):
        if type(flag_or_msg) == int:
            flag = flag_or_msg
            message = 'CVode returned %s' % ('None' if flag is None else cvode.CVodeGetReturnFlagName(flag))
        elif type(flag_or_msg) == str:
            message = flag_or_msg
        else:
            raise TypeError('Type int (flag) or str expected')
        super(CvodeException, self).__init__(message)
        self.result = result
        return


def assert_assigns_all(fun, y, f_data=None):
    """
    Check that ``fun(t, y, ydot, f_data)`` does assign to all elements of *ydot*.
    
    Normal operation: no output, no exception.
    
    >>> def fun0(t, y, ydot, f_data):
    ...     ydot[0] = 0
    ...     ydot[1] = 0
    >>> assert_assigns_all(fun0, [0, 0]) # no output
    
    Raises exception on failure:
    
    >>> def fun1(t, y, ydot, f_data):
    ...     ydot[1] = 0 # fails to assign a value to ydot[0]
    >>> assert_assigns_all(fun1, [0, 0])
    Traceback (most recent call last):
    ...
    AssertionError: Function fun1 in module ... failed to assign finite value(s) to element(s) [0] of rate vector
    
    The exception instance holds the indices in attribute :attr:`i`.
    
    >>> try:
    ...     assert_assigns_all(fun1, [0, 0])
    ... except AssertionError, exc:
    ...     print exc.i
    [0]
    """
    y = np.array(y, ndmin=1)
    ydot = np.array(y, dtype=float, copy=True)
    ydot.fill(np.nan)
    fun(0, y, ydot, f_data)
    i = np.where(~np.isfinite(ydot))[0]
    if len(i) > 0:
        msg = 'Function ' + fun.__name__
        try:
            msg += ' in module ' + fun.__module__
        except AttributeError:
            pass

        msg += ' failed to assign finite value(s)'
        msg += ' to element(s) %s of rate vector' % i
        try:
            if fun.traceback:
                msg += ':' + fun.traceback
        except AttributeError:
            pass

        err = AssertionError(msg)
        err.i = i
        raise err


def cvodefun(fun):
    """
    Wrap ODE right-hand side function for use with CVODE in Pysundials.
    
    A `CVRhsFn 
    <https://computation.llnl.gov/casc/sundials/documentation/cv_guide/node5.html#SECTION00561000000000000000>`_ 
    (CVODE right-hand side function) is called for its side effect,
    modifying the *ydot* output vector. It should return 0 on success,
    a positive value if a recoverable error occurs,
    and a negative value if it failed unrecoverably.
    
    This decorator allows you to code the CVRhsFn without explicitly assigning
    the return value. It returns a callable object that returns -1 on exception
    and 0 otherwise. In case of exception, the traceback text is stored as a
    "traceback" attribute of the object.
    
    Below, :func:`ode` does not return anything. 
    It raises an exception if y[0] == 0.
    
    >>> @cvodefun
    ... def ode(t, y, ydot, f_data):
    ...     ydot[0] = 1 / y[0]
    >>> ydot = [None]
    >>> ode(0, [1], ydot, None)
    0
    >>> ydot
    [1]
    >>> ode(0, [0], ydot, None)
    -1
    >>> print ode.traceback
    Traceback (most recent call last):
    ...
    ZeroDivisionError: integer division or modulo by zero

    The wrapped function is a proper CVRhsFn with a return value. 
    In case of exception, the return value is set to -1, otherwise the return 
    value is passed through.
    
    >>> @cvodefun
    ... def ode(t, y, ydot, f_data):
    ...     ydot[0] = 1 / y[0]
    ...     return y[0]
    
    >>> ode
    @cvodefun wrapper around <function ode at 0x...>
    >>> ode(0, [2], ydot, None)
    2
    >>> ode(0, [-2], ydot, None)
    -2
    >>> ode(0, [0], ydot, None)
    -1
    >>> print ode.traceback
    Traceback (most recent call last):
    ...
    ZeroDivisionError: integer division or modulo by zero
    
    Pysundials relies on the ODE right-hand side behaving like a function.
    
    >>> ode.__name__
    'ode'
    >>> ode.func_name
    'ode'
    """

    class odefun(object):
        """Wrapper for a CVODE right-hand side function"""

        def __init__(self):
            self.__name__ = fun.__name__
            self.func_name = fun.__name__
            self.traceback = ''

        def __call__(self, *args, **kwargs):
            """Return function value if defined, -1 if exception, 0 otherwise"""
            self.traceback = ''
            try:
                result = fun(*args, **kwargs)
                if result is None:
                    return 0
                return result
            except StandardError:
                self.traceback = traceback.format_exc()
                return -1

            return

        def __repr__(self):
            return '@cvodefun wrapper around %s' % fun

    return odefun()


def new_with_kwargs(cls, args, kwargs):
    """
    A helper function for pickling classes with keyword arguments.
    
    http://stackoverflow.com/questions/5238252/unpickling-new-style-with-kwargs-not-possible
    """
    return cls.__new__(cls, *args, **kwargs)


class Cvodeint(object):
    """
    Wrapper for common uses of :mod:`pysundials.cvode`
    
    :param function f_ode: Function of (t, y, ydot, f_data), 
        which writes rates-of-change to *ydot* and finishes with ``return 0``. 
        The ODE function must accept  four arguments, but is free to ignore 
        some of them.
    :param array_like t: Time, either [start end] or a vector of desired 
        return times. This determines whether 
        :meth:`~cgp.cvodeint.core.Cvodeint.integrate` returns time steps chosen 
        adaptively by CVODE, or just a copy of *t*.
    :param array_like y: Initial state vector, will be coerced to 
        cvode.NVector().
    :param reltol, abstol, nrtfn, g_rtfn, f_data, g_data: Arguments passed 
        to CVODE (`details 
        <https://computation.llnl.gov/casc/sundials/documentation/cv_guide/cv_guide.html>`_)
    :param int chunksize: When returning adaptive time steps, result 
        vectors are allocated in chunks of *chunksize*. 
    :param int maxsteps: If the number of  time-steps exceeds *maxsteps*, 
        an exception is raised.
    :param int mupper, mlower: Upper and lower bandwidth for the 
        `CVBand 
        <https://computation.llnl.gov/casc/sundials/documentation/cv_guide/node5.html#SECTION00566000000000000000>`_
        approximation to the Jacobian. CVDense is used by default if 
        *mupper* and *mlower* are both ``None``.
    
    **Usage example:**
    
    .. plot::
       :include-source:
       :width: 400
       
       >>> from cgp.cvodeint import *
       >>> from pysundials import cvode
       >>> from math import pi, sin
       
       Define the rate of change *dy/dt* as a function of the state *y*.
       The differential equation may use existing Python variables as 
       parameters. By convention, it must take arguments 
       *(t, y, ydot, f_data)*, where *ydot* is a writable parameter for 
       the actual result. See :func:`cvodefun` for details on CVODE's
       requirements for an ODE right-hand side.
       
       >>> r, K, amplitude, period = 1.0, 1.0, 0.25, 1.0
       >>> def ode(t, y, ydot, f_data):
       ...     ydot[0] = r * y[0] * (1 - y[0]/K) + amplitude * sin(2 * pi * t/period)
       
       Call the :meth:`Cvodeint` constructor with ODE function, time, and 
       initial state.
       
       >>> cvodeint = Cvodeint(ode, [0, 4], [0.1])

       Integrate over the time interval specified above.
       The :meth:`integrate` method returns the last *flag* returned by CVODE.
       
       >>> t, y, flag = cvodeint.integrate()
       
       >>> import matplotlib.pyplot as plt
       >>> h = plt.plot(t, y, '.-')
       >>> h = plt.title("Logistic growth + sinusoid")
       >>> text = "Last flag: " + cvode.CVodeGetReturnFlagName(flag)
       >>> h = plt.text(1, 0.8, text)
    
    .. note::
    
        *f_data* is intended for passing parameters to the ODE, but I couldn't
        get it to work. However, you can freely access variables that were in
        scope when the ODE function was defined, as this example shows.
    
    To change parameter values after the function is defined, use a mutable 
    variable for the parameter. In the first integration below, the state is 
    constant because the growth rate is zero.
    
    >>> growth_rate = [0.0]
    >>> def exp_growth(t, y, ydot, f_data):
    ...     ydot[0] = growth_rate[0] * y[0]
    ...     return 0
    >>> cvodeint = Cvodeint(exp_growth, t=[0, 0.5, 1], y=[0.25])
    >>> t, y, flag = cvodeint.integrate()
    >>> y
    array([[ 0.25], [ 0.25], [ 0.25]])
    
    Modify the growth rate and integrate further. Now, there is about 
    0.1 * 0.25 = 0.025 increase in y over 1 time unit.
    
    >>> growth_rate[0] = 0.1
    >>> t, y, flag = cvodeint.integrate(t=[0, 0.1, 1])
    >>> y.round(4)
    array([[ 0.25  ], [ 0.2525], [ 0.2763]])
    
    If the ode function is discontinuous, the solver may need to be
    reinitialized at the point of discontinuity.
    
    .. plot::
       :include-source:
       :width: 400
       
       from cgp.cvodeint import *
       eps = [1, 10]
       t_switch = 5
       t = [0, 10]
       def vdp(t, y, ydot, f_data): # van der Pol equation
           _eps = eps[0] if t <= t_switch else eps[1]
           ydot[0] = y[1]
           ydot[1] = _eps * (1 - y[0] * y[0]) * y[1] - y[0]
           return 0
       cvodeint = Cvodeint(vdp, t, [-2, 0])
       t0, y0, flag0 = cvodeint.integrate(t = [t[0], t_switch])
       t1, y1, flag1 = cvodeint.integrate(t = [t_switch, t[1]])
       plt.plot(t0, y0, t1, y1)    
    
    The :meth:`rootfinding <RootInit>` facilities of CVODE can be used 
    to find zero-crossings of a function of the state vector (example:
    :func:`~cgp.cvodeint.example_ode.g_rtfn_y`). Here we integrate the 
    van der Pol model to a series of specified values for y[0].
           
    .. plot::
       :include-source:
       :width: 400
       
       >>> from ctypes import byref, c_float
       >>> from cgp.cvodeint import *
       >>> thresholds = np.arange(-1.5, 1.5, 0.6)
       >>> cvodeint = Cvodeint(example_ode.vdp, [0, 20], [0, -2], reltol=1e-3)
       >>> res = [cvodeint.integrate(nrtfn=1, g_rtfn=example_ode.g_rtfn_y,
       ...     g_data=byref(c_float(thr))) for thr in thresholds]
       
       >>> import matplotlib.pyplot as plt
       >>> h = [plt.plot(t, y, '.-') for t, y, flag in res]
       >>> h = plt.hlines(thresholds, *plt.xlim(), color="grey")
    """

    def __init__--- This code section failed: ---

 L. 384         0  LOAD_GLOBAL           0  'np'
                3  LOAD_ATTR             1  'array'
                6  LOAD_FAST             2  't'
                9  LOAD_CONST               'dtype'
               12  LOAD_GLOBAL           2  'float'
               15  LOAD_CONST               'ndmin'
               18  LOAD_CONST               1
               21  CALL_FUNCTION_513   513  None
               24  STORE_FAST            2  't'

 L. 385        27  SETUP_EXCEPT         31  'to 61'

 L. 386        30  LOAD_GLOBAL           0  'np'
               33  LOAD_ATTR             1  'array'
               36  LOAD_FAST             3  'y'
               39  LOAD_CONST               'dtype'
               42  LOAD_GLOBAL           2  'float'
               45  LOAD_CONST               'ndmin'
               48  LOAD_CONST               1
               51  CALL_FUNCTION_513   513  None
               54  STORE_FAST            3  'y'
               57  POP_BLOCK        
               58  JUMP_FORWARD         44  'to 105'
             61_0  COME_FROM            27  '27'

 L. 387        61  DUP_TOP          
               62  LOAD_GLOBAL           3  'ValueError'
               65  COMPARE_OP           10  exception-match
               68  POP_JUMP_IF_FALSE   104  'to 104'
               71  POP_TOP          
               72  POP_TOP          
               73  POP_TOP          

 L. 388        74  LOAD_CONST               'State vector y not interpretable as float: {}'
               77  STORE_FAST           14  'msg'

 L. 389        80  LOAD_GLOBAL           3  'ValueError'
               83  LOAD_FAST            14  'msg'
               86  LOAD_ATTR             4  'format'
               89  LOAD_FAST             3  'y'
               92  CALL_FUNCTION_1       1  None
               95  CALL_FUNCTION_1       1  None
               98  RAISE_VARARGS_1       1  None
              101  JUMP_FORWARD          1  'to 105'
              104  END_FINALLY      
            105_0  COME_FROM           104  '104'
            105_1  COME_FROM            58  '58'

 L. 390       105  LOAD_GLOBAL           5  'len'
              108  LOAD_FAST             3  'y'
              111  CALL_FUNCTION_1       1  None
              114  LOAD_CONST               0
              117  COMPARE_OP            4  >
              120  POP_JUMP_IF_TRUE    132  'to 132'
              123  LOAD_ASSERT              AssertionError
              126  LOAD_CONST               'Empty state vector'
              129  RAISE_VARARGS_2       2  None

 L. 392       132  LOAD_GLOBAL           7  'assert_assigns_all'
              135  LOAD_FAST             1  'f_ode'
              138  LOAD_FAST             3  'y'
              141  LOAD_FAST             8  'f_data'
              144  CALL_FUNCTION_3       3  None
              147  POP_TOP          

 L. 397       148  LOAD_FAST             1  'f_ode'
              151  LOAD_FAST             0  'self'
              154  STORE_ATTR            8  'f_ode'

 L. 398       157  LOAD_FAST             1  'f_ode'
              160  LOAD_FAST             2  't'
              163  LOAD_CONST               0
              166  BINARY_SUBSCR    
              167  LOAD_GLOBAL           9  'nv'
              170  LOAD_FAST             3  'y'
              173  CALL_FUNCTION_1       1  None
              176  LOAD_GLOBAL           9  'nv'
              179  LOAD_FAST             3  'y'
              182  CALL_FUNCTION_1       1  None
              185  LOAD_FAST             8  'f_data'
              188  CALL_FUNCTION_4       4  None
              191  STORE_FAST           15  'success_value'

 L. 399       194  SETUP_EXCEPT         25  'to 222'

 L. 400       197  LOAD_FAST             1  'f_ode'
              200  LOAD_CONST               None
              203  LOAD_CONST               None
              206  LOAD_CONST               None
              209  LOAD_CONST               None
              212  CALL_FUNCTION_4       4  None
              215  STORE_FAST           16  'error_value'
              218  POP_BLOCK        
              219  JUMP_FORWARD         56  'to 278'
            222_0  COME_FROM           194  '194'

 L. 401       222  DUP_TOP          
              223  LOAD_GLOBAL          11  'StandardError'
              226  COMPARE_OP           10  exception-match
              229  POP_JUMP_IF_FALSE   277  'to 277'
              232  POP_TOP          
              233  POP_TOP          
              234  POP_TOP          

 L. 402       235  LOAD_CONST               None
              238  STORE_FAST           16  'error_value'

 L. 403       241  SETUP_EXCEPT         13  'to 257'

 L. 404       244  LOAD_CONST               ''
              247  LOAD_FAST             1  'f_ode'
              250  STORE_ATTR           12  'traceback'
              253  POP_BLOCK        
              254  JUMP_ABSOLUTE       278  'to 278'
            257_0  COME_FROM           241  '241'

 L. 405       257  DUP_TOP          
              258  LOAD_GLOBAL          13  'AttributeError'
              261  COMPARE_OP           10  exception-match
              264  POP_JUMP_IF_FALSE   273  'to 273'
              267  POP_TOP          
              268  POP_TOP          
              269  POP_TOP          

 L. 406       270  JUMP_ABSOLUTE       278  'to 278'
              273  END_FINALLY      
            274_0  COME_FROM           273  '273'
              274  JUMP_FORWARD          1  'to 278'
              277  END_FINALLY      
            278_0  COME_FROM           277  '277'
            278_1  COME_FROM           219  '219'

 L. 407       278  LOAD_FAST            15  'success_value'
              281  LOAD_CONST               0
              284  COMPARE_OP            2  ==
              287  POP_JUMP_IF_FALSE   314  'to 314'
              290  LOAD_FAST            16  'error_value'
              293  LOAD_CONST               0
              296  COMPARE_OP            0  <
            299_0  COME_FROM           287  '287'
              299  POP_JUMP_IF_FALSE   314  'to 314'

 L. 408       302  LOAD_FAST             1  'f_ode'
              305  LOAD_FAST             0  'self'
              308  STORE_ATTR           14  'my_f_ode'
              311  JUMP_FORWARD         15  'to 329'

 L. 410       314  LOAD_GLOBAL          15  'cvodefun'
              317  LOAD_FAST             1  'f_ode'
              320  CALL_FUNCTION_1       1  None
              323  LOAD_FAST             0  'self'
              326  STORE_ATTR           14  'my_f_ode'
            329_0  COME_FROM           311  '311'

 L. 416       329  LOAD_GLOBAL           9  'nv'
              332  LOAD_FAST             3  'y'
              335  CALL_FUNCTION_1       1  None
              338  LOAD_FAST             0  'self'
              341  STORE_ATTR           16  'y'

 L. 417       344  LOAD_GLOBAL          17  'cvode'
              347  LOAD_ATTR            18  'realtype'
              350  LOAD_CONST               0.0
              353  CALL_FUNCTION_1       1  None
              356  LOAD_FAST             0  'self'
              359  STORE_ATTR           19  'tret'

 L. 418       362  LOAD_GLOBAL          20  'type'
              365  LOAD_FAST             5  'abstol'
              368  CALL_FUNCTION_1       1  None
              371  LOAD_GLOBAL          17  'cvode'
              374  LOAD_ATTR            18  'realtype'
              377  COMPARE_OP            8  is
              380  POP_JUMP_IF_FALSE   395  'to 395'

 L. 419       383  LOAD_FAST             5  'abstol'
              386  LOAD_FAST             0  'self'
              389  STORE_ATTR           21  'abstol'
              392  JUMP_FORWARD         51  'to 446'

 L. 420       395  LOAD_GLOBAL           0  'np'
              398  LOAD_ATTR            22  'isscalar'
              401  LOAD_FAST             5  'abstol'
              404  CALL_FUNCTION_1       1  None
              407  POP_JUMP_IF_FALSE   431  'to 431'

 L. 421       410  LOAD_GLOBAL          17  'cvode'
              413  LOAD_ATTR            18  'realtype'
              416  LOAD_FAST             5  'abstol'
              419  CALL_FUNCTION_1       1  None
              422  LOAD_FAST             0  'self'
              425  STORE_ATTR           21  'abstol'
              428  JUMP_FORWARD         15  'to 446'

 L. 423       431  LOAD_GLOBAL           9  'nv'
              434  LOAD_FAST             5  'abstol'
              437  CALL_FUNCTION_1       1  None
              440  LOAD_FAST             0  'self'
              443  STORE_ATTR           21  'abstol'
            446_0  COME_FROM           428  '428'
            446_1  COME_FROM           392  '392'

 L. 424       446  LOAD_FAST             2  't'
              449  LOAD_FAST             0  'self'
              452  STORE_ATTR           23  't'

 L. 425       455  LOAD_GLOBAL          17  'cvode'
              458  LOAD_ATTR            18  'realtype'
              461  LOAD_FAST             2  't'
              464  LOAD_CONST               0
              467  BINARY_SUBSCR    
              468  CALL_FUNCTION_1       1  None
              471  LOAD_FAST             0  'self'
              474  STORE_ATTR           24  't0'

 L. 426       477  LOAD_FAST             2  't'
              480  LOAD_CONST               -1
              483  BINARY_SUBSCR    
              484  LOAD_FAST             0  'self'
              487  STORE_ATTR           25  'tstop'

 L. 427       490  LOAD_GLOBAL           5  'len'
              493  LOAD_FAST             3  'y'
              496  CALL_FUNCTION_1       1  None
              499  LOAD_FAST             0  'self'
              502  STORE_ATTR           26  'n'

 L. 428       505  LOAD_FAST             4  'reltol'
              508  LOAD_FAST             0  'self'
              511  STORE_ATTR           27  'reltol'

 L. 429       514  LOAD_GLOBAL          20  'type'
              517  LOAD_FAST             0  'self'
              520  LOAD_ATTR            21  'abstol'
              523  CALL_FUNCTION_1       1  None
              526  LOAD_GLOBAL           9  'nv'
              529  COMPARE_OP            8  is
              532  POP_JUMP_IF_FALSE   544  'to 544'
              535  LOAD_GLOBAL          17  'cvode'
              538  LOAD_ATTR            28  'CV_SV'
              541  JUMP_FORWARD          6  'to 550'
              544  LOAD_GLOBAL          17  'cvode'
              547  LOAD_ATTR            29  'CV_SS'
            550_0  COME_FROM           541  '541'
              550  LOAD_FAST             0  'self'
              553  STORE_ATTR           30  'itol'

 L. 430       556  LOAD_FAST             8  'f_data'
              559  LOAD_FAST             0  'self'
              562  STORE_ATTR           31  'f_data'

 L. 431       565  LOAD_FAST             9  'g_data'
              568  LOAD_FAST             0  'self'
              571  STORE_ATTR           32  'g_data'

 L. 432       574  LOAD_FAST            10  'chunksize'
              577  LOAD_FAST             0  'self'
              580  STORE_ATTR           33  'chunksize'

 L. 433       583  LOAD_FAST            11  'maxsteps'
              586  LOAD_FAST             0  'self'
              589  STORE_ATTR           34  'maxsteps'

 L. 434       592  LOAD_CONST               None
              595  LOAD_FAST             0  'self'
              598  STORE_ATTR           35  'last_flag'

 L. 436       601  LOAD_GLOBAL          17  'cvode'
              604  LOAD_ATTR            36  'CVodeCreate'
              607  LOAD_GLOBAL          17  'cvode'
              610  LOAD_ATTR            37  'CV_BDF'
              613  LOAD_GLOBAL          17  'cvode'
              616  LOAD_ATTR            38  'CV_NEWTON'
              619  CALL_FUNCTION_2       2  None
              622  LOAD_FAST             0  'self'
              625  STORE_ATTR           39  'cvode_mem'

 L. 437       628  LOAD_GLOBAL          17  'cvode'
              631  LOAD_ATTR            40  'CVodeMalloc'
              634  LOAD_FAST             0  'self'
              637  LOAD_ATTR            39  'cvode_mem'
              640  LOAD_FAST             0  'self'
              643  LOAD_ATTR            14  'my_f_ode'
              646  LOAD_FAST             0  'self'
              649  LOAD_ATTR            24  't0'
              652  LOAD_FAST             0  'self'
              655  LOAD_ATTR            16  'y'

 L. 438       658  LOAD_FAST             0  'self'
              661  LOAD_ATTR            30  'itol'
              664  LOAD_FAST             0  'self'
              667  LOAD_ATTR            27  'reltol'
              670  LOAD_FAST             0  'self'
              673  LOAD_ATTR            21  'abstol'
              676  CALL_FUNCTION_7       7  None
              679  POP_TOP          

 L. 439       680  LOAD_FAST             8  'f_data'
              683  LOAD_CONST               None
              686  COMPARE_OP            9  is-not
              689  POP_JUMP_IF_FALSE   729  'to 729'

 L. 440       692  LOAD_GLOBAL          17  'cvode'
              695  LOAD_ATTR            41  'CVodeSetFdata'
              698  LOAD_FAST             0  'self'
              701  LOAD_ATTR            39  'cvode_mem'

 L. 441       704  LOAD_GLOBAL           0  'np'
              707  LOAD_ATTR            42  'ctypeslib'
              710  LOAD_ATTR            43  'as_ctypes'
              713  LOAD_FAST             0  'self'
              716  LOAD_ATTR            31  'f_data'
              719  CALL_FUNCTION_1       1  None
              722  CALL_FUNCTION_2       2  None
              725  POP_TOP          
              726  JUMP_FORWARD          0  'to 729'
            729_0  COME_FROM           726  '726'

 L. 442       729  LOAD_GLOBAL          17  'cvode'
              732  LOAD_ATTR            44  'CVodeSetStopTime'
              735  LOAD_FAST             0  'self'
              738  LOAD_ATTR            39  'cvode_mem'
              741  LOAD_FAST             0  'self'
              744  LOAD_ATTR            25  'tstop'
              747  CALL_FUNCTION_2       2  None
              750  POP_TOP          

 L. 444       751  LOAD_FAST            12  'mupper'
              754  LOAD_CONST               None
              757  COMPARE_OP            8  is
              760  POP_JUMP_IF_FALSE   788  'to 788'

 L. 445       763  LOAD_GLOBAL          17  'cvode'
              766  LOAD_ATTR            45  'CVDense'
              769  LOAD_FAST             0  'self'
              772  LOAD_ATTR            39  'cvode_mem'
              775  LOAD_FAST             0  'self'
              778  LOAD_ATTR            26  'n'
              781  CALL_FUNCTION_2       2  None
              784  POP_TOP          
              785  JUMP_FORWARD         28  'to 816'

 L. 447       788  LOAD_GLOBAL          17  'cvode'
              791  LOAD_ATTR            46  'CVBand'
              794  LOAD_FAST             0  'self'
              797  LOAD_ATTR            39  'cvode_mem'
              800  LOAD_FAST             0  'self'
              803  LOAD_ATTR            26  'n'
              806  LOAD_FAST            12  'mupper'
              809  LOAD_FAST            13  'mlower'
              812  CALL_FUNCTION_4       4  None
              815  POP_TOP          
            816_0  COME_FROM           785  '785'

 L. 448       816  LOAD_FAST             0  'self'
              819  LOAD_ATTR            47  'RootInit'
              822  LOAD_FAST             6  'nrtfn'
              825  LOAD_FAST             7  'g_rtfn'
              828  LOAD_FAST             9  'g_data'
              831  CALL_FUNCTION_3       3  None
              834  POP_TOP          
              835  LOAD_CONST               None
              838  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 835

    def __new__(cls, *args, **kwargs):
        """Used for pickling."""
        instance = super(Cvodeint, cls).__new__(cls)
        instance._init_args = (args, kwargs)
        instance.__init__(*args, **kwargs)
        return instance

    def __reduce__(self):
        """Used for pickling."""
        args, kwargs = self._init_args
        return (new_with_kwargs, (self.__class__, args, kwargs), None)

    def ydoti(self, index):
        """
        Get rate-of-change of y[index] as a function of (t, y, gout, g_data).
        
        :param int index: Index of a state variable.
        
        For use with CVode's `rootfinding
        <https://computation.llnl.gov/casc/sundials/documentation/cv_guide/node3.html#SECTION00340000000000000000>`_
        functions.
        
        >>> from cgp.cvodeint.example_ode import vdp
        >>> c = Cvodeint(vdp, t=[0, 1], y=[1, 1])
        >>> gout = cvode.NVector([0.0])
        >>> f = c.ydoti(0)
        >>> f(0, c.y, gout, None)  # returns 0 per CVODE convention
        0
        >>> gout  # The actual result is written to the output parameter gout
        [1.0]
        """
        ydot = np.empty_like(self.y)

        def result(t, y, gout, g_data):
            """Function for CVODE rootfinding."""
            self.f_ode(t, y, ydot, None)
            gout[0] = ydot[index]
            return 0

        return result

    def integrate(self, t=None, y=None, nrtfn=None, g_rtfn=None, g_data=None, assert_flag=None, ignore_flags=False):
        """
        Integrate over time interval, init'ing solver or rootfinding as needed.
        
        :param array_like t: new output time(s)
        :param array_like y: new initial state (default: resume from current 
            solver state
        :param int nrtfn: length of gout (required if *g_rtfn* is not ``None``)
        :param function g_rtfn: new rootfinding function of 
            *(t, y, gout, g_data)*,
            passed to :func:`~pysundials.cvode.CVodeRootInit`
        :param g_data: new data for rootfinding function
        :param int assert_flag: raise exception if the last flag returned by 
            CVode differs from *assert_flag* (see `flags`)
        :param bool ignore_flags: overrides assert_flag and does not check 
            CVode flag
        :return tuple: 
            * **tout**: time vector 
              (equal to input time *t* if that has len > 2), 
            * **Y**: array of state vectors at time ``t[i]``
            * **flag**: flag returned by :func:`~pysundials.cvode.CVode`, 
              one of ``[cvode.CV_SUCCESS, cvode.CV_ROOT_RETURN, 
              cvode.CV_TSTOP_RETURN]``
        
        * With no input arguments, integration continues from the current time 
          and state until the end time passed to :meth:`Cvodeint`.
        * If t is None, init solver and use the t passed to Cvodeint().
        * If t is scalar, integrate to that time, return adaptive time steps.
        * If len(t) == 1, return output only for that time.
        * If len(t) == 2, integrate from t[0] to t[1], return adaptive time 
          steps.
        * If len(t) > 2, integrate from t[0] and return fixed time steps = t.
        * If y is None, resume from current solver state.
        
        >>> from cgp.cvodeint.core import Cvodeint
        >>> from cgp.cvodeint.example_ode import exp_growth, exp_growth_sol
        >>> t, y = [0, 2], [0.1]
        >>> cvodeint = Cvodeint(exp_growth, t, y)
        
        With no parameters, :meth:`integrate` uses the current state, t0 and tstop:
        
        >>> t, Y, flag = cvodeint.integrate()
        
        Repeating the call will reset time:
        
        >>> t1, Y1, flag1 = cvodeint.integrate(); t1[0], t1[-1]
        (0.0, 2.0)
        
        Using a scalar or single-element t integrates from current time to t:
        
        >>> t2, Y2, flag2 = cvodeint.integrate(t=3); t2[0], t2[-1]
        (2.0, 3.0)
        
        Verify the solution:
        
        >>> Ysol = exp_growth_sol(t, Y[0])
        >>> err = (Y.squeeze() - Ysol)[1:]
        >>> "%.5e %.5e" % (err.min(), err.max())
        '2.75108e-09 1.25356e-06'
        
        ..  plot::
            :width: 300
            
            import matplotlib.pyplot as plt
            from cgp.cvodeint.core import Cvodeint
            from cgp.cvodeint.example_ode import exp_growth, exp_growth_sol
            cvodeint = Cvodeint(exp_growth, t=[0, 2], y=[0.1])
            t, Y, flag = cvodeint.integrate()
            Ysol = exp_growth_sol(t, Y[0])
            plt.plot(t, Y, '.-', t, Ysol, 'o')
            plt.title("Exponential growth")
            plt.xlabel("Time")
            plt.ylabel("y(t)")
        
        In case of error, the solution so far will be returned:
        
        ..  plot::
            :include-source:
            :width: 400
            
            from cgp.cvodeint import *
            import matplotlib.pyplot as plt
            import math
            def ode(t, y, ydot, f_data):
                ydot[0] = math.log(y[1])
                ydot[1] = 1 / y[0] - t # will eventually turn negative
            cvodeint = Cvodeint(ode, [0, 4], [1, 1])
            try:
                cvodeint.integrate()    # Logs error and prints traceback,   
            except CvodeException, exc: # both ignored by doctest.
                t, y, flag = exc.result
                plt.plot(t, y, '.-')
                plt.text(1, 1, "Flag: %s" % flags[flag])
        
        Another example:
        
        >>> from example_ode import logistic_growth, logistic_growth_sol
        >>> cvodeint = Cvodeint(logistic_growth, [0, 2], [0.1])
        >>> t, Y, flag = cvodeint.integrate()
        >>> Ysol = logistic_growth_sol(t, Y[0])
        >>> err = (Y.squeeze() - Ysol)[1:]
        >>> "%.5e %.5e" % (err.min(), err.max())
        '-1.40383e-07 3.40267e-08'        
        
        With len(t) == 2, re-initialize at t[0] and set tstop = t[-1]:
        
        >>> t, y, flag = cvodeint.integrate(t=[2, 3])
        >>> print np.array2string(t, precision=3)
        [ 2.     2.001  2.001  2.002  ... 2.966  2.995  3.   ]
        >>> print np.array2string(y, precision=3)
        [[ 0.451] [ 0.451] [ 0.451] ... [ 0.683] [ 0.69 ] [ 0.691]]
        
        With t omitted, re-initialize at existing t0 with current state:
        
        >>> t, y, flag = cvodeint.integrate(y=[0.2])
        >>> print np.array2string(t, precision=3)
        [ 2.     2.     2.001 ... 2.924  2.973  3.   ]
        >>> print np.array2string(y, precision=3)
        [[ 0.2 ] [ 0.2  ] [ 0.2  ] ... [ 0.387] [ 0.398] [ 0.405]]

        With both t and y given:
        
        >>> t, y, flag = cvodeint.integrate(t=[0, 1, 2], y=[0.3])
        >>> print np.array2string(y, precision=3)
        [[ 0.3  ] [ 0.538] [ 0.76 ]]
        
        Example with discontinuous right-hand-side:
        
        >>> eps = [1, 10]
        >>> t_switch = 5
        >>> tspan = [0, 10]
        >>> def vdp(t, y, ydot, f_data): # van der Pol equation
        ...     _eps = eps[0] if t <= t_switch else eps[1]
        ...     ydot[0] = y[1]
        ...     ydot[1] = _eps * (1 - y[0] * y[0]) * y[1] - y[0]
        ...     return 0
        >>> cvodeint = Cvodeint(vdp, t, [-2, 0])
        
        Integrate until RHS discontinuity:
        
        >>> t, y, flag = cvodeint.integrate(t = [tspan[0], t_switch])
        >>> t[-1], y[-1]
        (5.0, array([ 0.83707776, -1.30708838]))

        Calling :meth:`Cvodeint.integrate` again will do the necessary 
        re-initialization:
        
        >>> t, y, flag = cvodeint.integrate(t = [t_switch, tspan[1]])
        >>> t[0], t[-1], y[-1]
        (5.0, 10.0, array([-1.69...,  0.090...]))
        """
        self._ReInit_if_required(t, y)
        self.RootInit(nrtfn, g_rtfn, g_data)
        if len(self.t) > 2:
            result = self._integrate_fixed_steps()
        else:
            result = self._integrate_adaptive_steps()
        flag = result[(-1)]
        self.last_flag = flag
        if type(assert_flag) is int:
            assert_flag = (
             assert_flag,)
        if ignore_flags or assert_flag is None or flag in assert_flag:
            return result
        raise CvodeException(flag, result)
        return

    def _ReInit_if_required(self, t=None, y=None):
        """
        Interpret/set time, state; call SetStopTime(), ReInit() if needed.
        
        If *t* is None, ``self.t`` is used to re-initialize at `
        ``tret==t0==self.t[0], tstop = self.t[-1]``.
        If *y* is ``None``, the current *y* is used at time ``tret``.
        If *t* is a scalar, *t0* is initialized to the current ``tret.value``.
        """
        if t is None and self.last_flag == cvode.CV_ROOT_RETURN and self.tret < self.tstop:
            t = self.tstop
        if t is not None:
            t = np.array(t, ndmin=1)
            if len(t) == 1:
                self.t = [
                 self.tret.value, t[0]]
                if y is None:
                    Dky = nv(self.y)
                    cvode.CVodeGetDky(self.cvode_mem, self.tret, 0, self.y)
                    if any(np.isnan(self.y)):
                        self.y[:] = Dky
                else:
                    try:
                        self.y[:] = y
                    except TypeError:
                        self.y[:] = y.item()

            else:
                self.t = t
        if y is not None:
            try:
                self.y[:] = y
            except TypeError:
                self.y[:] = y.item()

        self.t0.value = self.t[0]
        self.tret.value = self.t[0]
        self.tstop = self.t[(-1)]
        if y is not None or t is None or len(self.t) >= 2:
            cvode.CVodeSetStopTime(self.cvode_mem, self.tstop)
            cvode.CVodeReInit(self.cvode_mem, self.my_f_ode, self.t0, self.y, self.itol, self.reltol, self.abstol)
        return

    def _integrate_adaptive_steps(self):
        """
        Repeatedly call CVode() with task CV_ONE_STEP_TSTOP and tout=tstop.
        
        Output: t, Y, flag. See Cvodeint.integrate().
        
        ..  plot::
            :include-source:
            :width: 400
            
            import matplotlib.pyplot as plt
            from cgp.cvodeint import *
            cvodeint = Cvodeint(example_ode.logistic_growth, 
                                t=[0, 2], y=[0.1], reltol=1e-3)
            t, y, flag = cvodeint.integrate()
            plt.plot(t, y, '.-')
        """
        Y = np.empty(shape=(self.chunksize, self.n))
        t = np.empty(shape=(self.chunksize,))
        d1 = self.chunksize
        Y[0] = np.array(self.y, copy=True)
        t[0] = self.t0.value
        i = 1
        maxsteps = self.maxsteps
        tstop = self.tstop
        cvode_mem = self.cvode_mem
        byref = ctypes.byref
        CVode = cvode.CVode
        y = self.y
        CV_SUCCESS = cvode.CV_SUCCESS
        CV_ROOT_RETURN = cvode.CV_ROOT_RETURN
        CV_TSTOP_RETURN = cvode.CV_TSTOP_RETURN
        CV_ONE_STEP_TSTOP = cvode.CV_ONE_STE_TSTOP
        flag = None
        while self.tret < tstop:
            if i >= maxsteps:
                Y.resize((i, self.n), refcheck=False)
                t.resize(i, refcheck=False)
                raise CvodeException('Maximum number of steps exceeded', (
                 t, Y, flag))
            flag = CVode(cvode_mem, tstop, y, byref(self.tret), CV_ONE_STEP_TSTOP)
            if flag in (CV_SUCCESS, CV_TSTOP_RETURN, CV_ROOT_RETURN):
                Y[i], t[i] = y, self.tret.value
                if flag == CV_ROOT_RETURN:
                    i += 1
                    break
            else:
                log.debug('Exception: %s: %s' % (i, flags[flag]))
                Y.resize((i, self.n), refcheck=False)
                t.resize(i, refcheck=False)
                raise CvodeException(flag, (t, Y, flag))
            i += 1
            if i >= d1:
                d1 = len(t) + self.chunksize
                log.warning('Enlarging arrays from %s to %s' % (i, d1))
                Y.resize((d1, self.n), refcheck=False)
                t.resize(d1, refcheck=False)
        else:
            flag = CV_TSTOP_RETURN

        Y.resize((i, self.n), refcheck=False)
        t.resize(i, refcheck=False)
        return (t, Y, flag)

    def _integrate_fixed_steps(self):
        """
        Repeatedly call CVode() with task CV_ONE_STEP_TSTOP and tout=t[i]
        
        Output: t, Y, flag. See :meth:`integrate`.
        The *maxsteps* setting is ignored when using fixed time steps.
        
        >>> from example_ode import logistic_growth
        >>> cvodeint = Cvodeint(logistic_growth, t=[0, 0.5, 2], y=[0.1])
        >>> cvodeint.integrate()
        (array([ 0. , 0.5, 2. ]), array([[ 0.1 ], [ 0.154...], [ 0.45...]]), 0)
        
        ..  plot::
            :width: 400
            
            from example_ode import logistic_growth
            cvodeint = Cvodeint(logistic_growth, t=np.linspace(0, 2, 5), y=[0.1])
            t, y, flag = cvodeint.integrate()
            plt.plot(t, y, '.-')
        """
        imax = len(self.t)
        Y = np.empty(shape=(imax, self.n))
        t = np.empty(shape=(imax,))
        Y[0] = np.array(self.y).copy()
        t[0] = self.t0.value
        cvode_mem = self.cvode_mem
        y = self.y
        i = 0
        for i in range(1, imax):
            flag = cvode.CVode(cvode_mem, self.t[i], y, ctypes.byref(self.tret), cvode.CV_NORMAL)
            Y[i], t[i] = y, self.tret.value
            if flag == cvode.CV_SUCCESS:
                continue
            else:
                break

        Y.resize((i + 1, self.n), refcheck=False)
        t.resize(i + 1, refcheck=False)
        result = (t, Y, flag)
        if flag in (cvode.CV_ROOT_RETURN, cvode.CV_SUCCESS):
            return result
        raise CvodeException(flag, result)

    def RootInit(self, nrtfn, g_rtfn=None, g_data=None):
        """
        Initialize rootfinding, disable rootfinding, or keep current settings.
        
        * If nrtfn == 0, disable rootfinding.
        * If nrtfn > 0, set rootfinding for g_rtfn.
        * If nrtfn is None, do nothing.
        
        Details `here 
        <https://computation.llnl.gov/casc/sundials/documentation/cv_guide/node6.html#SECTION00670000000000000000>`__.
        
        >>> from pysundials import cvode
        >>> from example_ode import exp_growth, g_rtfn_y
        >>> g_data = ctypes.c_float(2.5)
        >>> cvodeint = Cvodeint(exp_growth, t=[0, 3], y=[1],
        ...     nrtfn=1, g_rtfn=g_rtfn_y, g_data=ctypes.byref(g_data))
        >>> t, y, flag = cvodeint.integrate()
        >>> y[-1]
        array([ 2.5])
        >>> cvode.CVodeGetReturnFlagName(flag)
        'CV_ROOT_RETURN'

        Warn if nrtfn is not given but g_rtfn or g_data is given:
        
        >>> cvodeint = Cvodeint(exp_growth, t=[0, 3], y=[1],
        ...     g_rtfn=g_rtfn_y, g_data=ctypes.byref(g_data))
        Traceback (most recent call last):
        ...
        CvodeException: If g_rtfn or g_data is given, nrtfn is required.
        """
        if nrtfn is not None:
            cvode.CVodeRootInit(self.cvode_mem, int(nrtfn), g_rtfn, g_data)
        elif g_rtfn is not None or g_data is not None:
            raise CvodeException('If g_rtfn or g_data is given, nrtfn is required.')
        return

    def __repr__(self):
        """
        String representation of Cvodeint object
        
        Unfortunately not as detailed under Cython as in pure Python.
        """
        import inspect
        try:
            args, _, _, defaults = inspect.getargspec(self.__init__)
        except TypeError:
            msg = '%s %s\ngetargspec(__init__) is not available'
            msg += ' when running under Cython'
            return msg % (self.__class__, self.f_ode)

        if defaults is None:
            defaults = ()
        del args[0]
        defaults = [
         None] * (len(args) - len(defaults)) + list(defaults)
        arglist = []
        for arg, default in zip(args, defaults):
            try:
                val = getattr(self, arg)
                if inspect.isfunction(val):
                    arglist.append((arg, val.func_name))
                elif val != default:
                    arglist.append((arg, repr(val)))
            except ValueError:
                try:
                    if any(val != default):
                        arglist.append((arg, repr(val)))
                except ValueError:
                    if np.any(val != default):
                        arglist.append((arg, repr(val)))

            except AttributeError:
                continue

        argstr = (', ').join([ '%s=%s' % x for x in arglist ])
        return '%s(%s)' % (self.__class__.__name__, argstr)

    def __eq__(self, other):
        """
        Compare a CVODE wrapper object to another.
        
        >>> from example_ode import vdp, exp_growth 
        >>> a, b = [Cvodeint(vdp, [0, 20], [0, -2]) for i in range(2)]
        >>> a == b
        True
        >>> a.y[0] = 1
        >>> a == b
        False
        >>> c = Cvodeint(exp_growth, t=[0,2], y=[0.1])
        >>> a == c
        False
        """
        return repr(self) == repr(other)

    def diff(self, other):
        """
        Return a detailed comparison of a CVODE wrapper object to another.
        
        Returns 0 if the objects are equal, otherwise a string.
        
        >>> from example_ode import vdp, exp_growth
        >>> from pprint import pprint 
        >>> a, b = [Cvodeint(vdp, [0, 20], [0, -2]) for i in range(2)]
        >>> print a.diff(b)
        <BLANKLINE>
        >>> a.y[0] = 1
        >>> print a.diff(b)
        - Cvodeint(f_ode=vdp, t=array([ 0., 20.]), y=[1.0, -2.0],
        ?                                           ^
        + Cvodeint(f_ode=vdp, t=array([ 0., 20.]), y=[0.0, -2.0],
        ?                                           ^
        >>> c = Cvodeint(exp_growth, t=[0,2], y=[0.25])
        >>> print a.diff(c)
        - Cvodeint(f_ode=vdp, t=array([  0.,  20.]), y=[1.0, -2.0],
        ?                ^^             -      -        ^ ---- ^^
        + Cvodeint(f_ode=exp_growth, t=array([ 0.,  2.]), y=[0.25],
        ?                ^^ +++++++                          ^  ^
        """
        import textwrap, difflib
        s, o = [ textwrap.wrap(repr(x)) for x in (self, other) ]
        return ('\n').join([ li.strip() for li in difflib.ndiff(s, o) if not li.startswith(' ')
                           ])


if __name__ == '__main__':
    import doctest
    failure_count, test_count = doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    print '\n        NOTE: This doctest will (by design) result in an error message and a \n        traceback, which will be ignored by doctest (apparently, is is printed \n        outside of standard error and output). \n        Warnings about "enlarging arrays" are also intended.\n        '
    if failure_count == 0:
        print 'All doctests passed.'