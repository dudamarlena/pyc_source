# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\electricpy\sim.py
# Compiled at: 2019-12-02 21:37:50
# Size of source mod 2**32: 47933 bytes
"""
---------------------
`electricpy.fault.py`
---------------------

Included Functions
------------------
- Digital Filter Simulator:             digifiltersim
- Step Response Filter Simulator:       step_response
- Ramp Response Filter Simulator:       ramp_response
- Parabolic Response Filter Simulator:  parabolic_response
- State-Space System Simulator:         statespace
- Newton Raphson Calculator:            NewtonRaphson
- Power Flow System Generator:          nr_pq
- Multi-Bus Power Flow Calculator:      mbuspowerflow
"""
import numpy as _np
import matplotlib.pyplot as _plt
from numdifftools import Jacobian as jacobian
from scipy.optimize import newton
from warnings import warn as _warn

def digifiltersim(fin, filter, freqs, NN=1000, dt=0.01, title='', legend=True, xlim=False, xmxscale=None, figsize=None):
    r"""
    Digital Filter Simulator
    
    Given an input function and filter parameters (specified in
    the z-domain) this function will plot the input function over
    NN time-steps of an unspecified size (the step-size must be
    specified outside the scope of this function). This function
    will also plot the resultant (output) function over the NN
    time-steps after having been filtered by that filter which
    is specified.
    
    The applied filter should be of the form:
    
    .. math:: \frac{b_0+b_1z^{-1}+b_2z^{-2}}{1-a_1z^{-1}-a_2z^{-2}}
    
    Where each row corresponds to a 1- or 2-pole filter.
    
    Parameters
    ----------
    fin:        function
                The input function, must be callable with specified
                step-size.
    filter:     array_like
                The filter parameter set as shown here:
                
                .. code-block:: python
                   
                   [[ a11, a12, b10, b11, b12],
                   [ a21, a22, b20, b21, b22],
                   [           ...          ],
                   [ an1, an2, bn0, bn1, bn2]]
                
    freqs:      list of float
                The set of frequencies to plot the input and output for.
    NN:         int, optional
                The number of time-steps to be plotted; default=1000
    dt:         float, optional
                The time-step size; default=0.01
    title:      str, optional
                The title presented on each plot; default=""
    xlim:       list, optional
                Limit in x-axis for graph plot. Accepts tuple of: (xmin, xmax).
                default=False.
    xmxscale:   float, optional
                Scaling limit of the x-axis, will set the maximum of the
                x-axis to xmxscale/(dt*freq) where freq is the current
                frequency being plotted.
    legend:     str, optional
                An argument to control whether the legend is shown,
                default=True.
    figsize:    tuple, optional
                The figure dimensions for each subplot, default=None
    """
    if figsize != None:
        _plt.figure(figsize=figsize)
    flen = len(freqs)
    for i in range(flen):
        freq = freqs[i]
        x = _np.zeros(NN)
        y = _np.zeros(NN)

    for k in range(NN):
        x[k] = fin(k * dt, freq)
    else:
        sz = filter.size
        if sz < 5:
            raise ValueError('ERROR: Too few filter arguments provided. Refer to documentation for proper format.')
        else:
            if sz == 5:
                rows = 1
            else:
                rows, cols = filter.shape
        x_tmp = _np.copy(x)
        nsteps = NN - 4
        for row_n in range(rows):
            row = filter[row_n]
            A1 = row[0]
            A2 = row[1]
            B0 = row[2]
            B1 = row[3]
            B2 = row[4]
            T = 3
            for _ in range(nsteps):
                T = T + 1
                y[T] = A1 * y[(T - 1)] + A2 * y[(T - 2)] + B0 * x_tmp[T] + B1 * x_tmp[(T - 1)] + B2 * x_tmp[(T - 2)]
            else:
                x_tmp = _np.copy(y)

        else:
            ytime = _np.copy(x_tmp)
            if flen % 2 == 0:
                _plt.subplot(flen, 2, i + 1)
            else:
                _plt.subplot(flen, 1, i + 1)
            _plt.plot(x, 'k--', label='Input')
            _plt.plot(ytime, 'k', label='Output')
            _plt.title(title)
            _plt.grid(which='both')
            if legend:
                _plt.legend(title=('Frequency = ' + str(freq) + 'Hz'))
            else:
                if xlim != False:
                    _plt.xlim(xlim)
            if xmxscale != None:
                _plt.xlim((0, xmxscale / (freq * dt)))
            _plt.tight_layout()
            _plt.show()


def step_response(system, npts=1000, dt=0.01, combine=True, xlim=False, title='Step Response', errtitle='Step Response Error', resplabel='Step Response', funclabel='Step Function', errlabel='Error', filename=None):
    """
    Step Function Response Plotter Function
    
    Given a transfer function, plots the response against step input
    and plots the error for the function.
    
    Parameters
    ----------
    system:     array_like
                The Transfer Function; can be provided as the following:
                * 1 (instance of lti)
                * 2 (num, den)
                * 3 (zeros, poles, gain)
                * 4 (A, B, C, D)
    npts:       int, optional
                Number of steps to calculate over; default is 1000.
    dt:         float, optional
                Difference between each data point, default is 0.01.
    combine:    bool, optional
                If combination of numerator and denominator is needed.
                This value should be set to "True" if the parts should be
                combined to show the complete system with feedback.
                default=True.
    title:      str, optional
                Additional string to be added to plot titles;
                default=""
    xlim:       list, optional
                Limit in x-axis for graph plot. Accepts tuple of: (xmin, xmax).
                default=False.
    filename:   bool, optional
                Control argument to specify whether the plotted
                figures should be saved. default=False
    """
    TT = _np.arange(0, npts * dt, dt)
    system = _sys_condition(system, combine)
    step = _np.zeros(npts)
    errS = _np.zeros(npts)
    for i in range(npts):
        step[i] = 1.0
    else:
        x, y1, x = sig.lsim(system, step, TT)
        for k in range(npts):
            errS[k] = step[k] - y1[k]
        else:
            _plt.figure()
            _plt.subplot(121)
            _plt.title(title)
            _plt.plot(TT, y1, 'k--', label=resplabel)
            _plt.plot(TT, step, 'k', label=funclabel)
            _plt.grid()
            _plt.legend()
            _plt.xlabel('Time (seconds)')
            if xlim != False:
                _plt.xlim(xlim)
            _plt.subplot(122)
            _plt.title(errtitle)
            _plt.plot(TT, errS, 'k', label=errlabel)
            _plt.grid()
            _plt.legend()
            _plt.xlabel('Time (seconds)')
            if xlim != False:
                _plt.xlim(xlim)
            _plt.subplots_adjust(wspace=0.3)
            if filename != None:
                _plt.savefig(filename)
            _plt.show()


def ramp_response(system, npts=1000, dt=0.01, combine=True, xlim=False, title='Ramp Response', errtitle='Ramp Response Error', resplabel='Ramp Response', funclabel='Ramp Function', errlabel='Error', filename=None):
    """
    Ramp Function Response Plotter Function
    
    Given a transfer function, plots the response against step input
    and plots the error for the function.
    
    Parameters
    ----------
    system:     array_like
                The Transfer Function; can be provided as the following:
                * 1 (instance of lti)
                * 2 (num, den)
                * 3 (zeros, poles, gain)
                * 4 (A, B, C, D)
    npts:       int, optional
                Number of steps to calculate over; default is 1000.
    dt:         float, optional
                Difference between each data point, default is 0.01.
    combine:    bool, optional
                If combination of numerator and denominator is needed.
                This value should be set to "True" if the parts should be
                combined to show the complete system with feedback.
                default=True.
    title:      str, optional
                Additional string to be added to plot titles;
                default=""
    xlim:       list, optional
                Limit in x-axis for graph plot. Accepts tuple of: (xmin, xmax).
                default=False.
    filename:   str, optional
                File directory/name with which the plotted figures 
                should be saved. default=None
    """
    TT = _np.arange(0, npts * dt, dt)
    system = _sys_condition(system, combine)
    ramp = _np.zeros(npts)
    errR = _np.zeros(npts)
    for i in range(npts):
        ramp[i] = dt * i
    else:
        x, y2, x = sig.lsim(system, ramp, TT)
        for k in range(npts):
            errR[k] = ramp[k] - y2[k]
        else:
            _plt.figure()
            _plt.subplot(121)
            _plt.title(title)
            _plt.plot(TT, y2, 'k--', label=resplabel)
            _plt.plot(TT, ramp, 'k', label=funclabel)
            _plt.grid()
            _plt.legend()
            _plt.xlabel('Time (seconds)')
            if xlim != False:
                _plt.xlim(xlim)
            _plt.subplot(122)
            _plt.title(errtitle)
            _plt.plot(TT, errR, 'k', label=errlabel)
            _plt.grid()
            _plt.legend()
            _plt.xlabel('Time (seconds)')
            if xlim != False:
                _plt.xlim(xlim)
            _plt.subplots_adjust(wspace=0.3)
            if filename != None:
                _plt.savefig(filename)
            _plt.show()


def parabolic_response(system, npts=1000, dt=0.01, combine=True, xlim=False, title='Parabolic Response', errtitle='Parabolic Response Error', resplabel='Parabolic Response', funclabel='Parabolic Function', errlabel='Error', filename=None):
    """
    Parabolic Function Response Plotter Function
    
    Given a transfer function, plots the response against step input
    and plots the error for the function.
    
    Parameters
    ----------
    system:     array_like
                The Transfer Function; can be provided as the following:
                * 1 (instance of lti)
                * 2 (num, den)
                * 3 (zeros, poles, gain)
                * 4 (A, B, C, D)
    npts:       int, optional
                Number of steps to calculate over; default is 1000.
    dt:         float, optional
                Difference between each data point, default is 0.01.
    combine:    bool, optional
                If combination of numerator and denominator is needed.
                This value should be set to "True" if the parts should be
                combined to show the complete system with feedback.
                default=True.
    title:      str, optional
                Additional string to be added to plot titles;
                default=""
    xlim:       list, optional
                Limit in x-axis for graph plot. Accepts tuple of: (xmin, xmax).
                default=False.
    filename:   bool, optional
                Control argument to specify whether the plotted
                figures should be saved. default=False
    """
    TT = _np.arange(0, npts * dt, dt)
    system = _sys_condition(system, combine)
    parabola = _np.zeros(npts)
    errP = _np.zeros(npts)
    for i in range(npts):
        parabola[i] = (dt * i) ** 2
    else:
        x, y3, x = sig.lsim(system, parabola, TT)
        for k in range(npts):
            errP[k] = parabola[k] - y3[k]
        else:
            _plt.figure()
            _plt.subplot(121)
            _plt.title(title)
            _plt.plot(TT, y3, 'k--', label=resplabel)
            _plt.plot(TT, parabola, 'k', label=funclabel)
            _plt.grid()
            _plt.legend()
            _plt.xlabel('Time (seconds)')
            if xlim != False:
                _plt.xlim(xlim)
            _plt.subplot(122)
            _plt.title(errtitle)
            _plt.plot(TT, errP, 'k', label=errlabel)
            _plt.grid()
            _plt.legend()
            _plt.xlabel('Time (seconds)')
            if xlim != False:
                _plt.xlim(xlim)
            _plt.subplots_adjust(wspace=0.3)
            if filename != None:
                _plt.savefig(filename)
            _plt.show()


def statespace(A, B, x=None, func=None, C=None, D=None, simpts=9999, NN=10000, dt=0.01, xlim=False, ylim=False, title='', ret=False, plotstate=True, plotforcing=None, plotresult=None, filename=None):
    """
    State-Space Simulation Plotter

    Parameters
    ----------
    A:          array_like
                Matrix A of State-Space Formulation
    B:          array_like
                Matrix B of State-Space Formulation
    x:          array_like, optional
                Initial Condition Matrix, if not provided, will assume
                initial conditions of zero.
    f:          function, optional
                State-Space Forcing Function; callable function that
                will return any/all forcing function Arguments needed as
                array-like object.
                Forcing function(s) can be provided as tuple of function
                handles, system will automatically concatenate their output
                to a matrix that can be handled.
    simpts:     int, optional
                Changes the range of simulation; defualt=9999
    NN:         int, optional
                Number of descrete points; default=10,000
    dt:         float, optional
                Time-step-size; default=0.01
    xlim:       list of float, optional
                Limit in x-axis for graph plot.
    ylim:       list of float, optional
                Limit in y-axis for graph plot.
    title:      str, optional
                Additional String for Plot Title
    ret:        bool, optional
                Control value to specify whether the state space terms should
                be returned.
    plot:       bool, optional
                Control value to enable/disable all plotting capabilities.
    plotforcing:bool, optional
                Control value to enable plotting of the forcing function(s)
    plotresult: bool, optional
                Control value to enable plotting of the final (combined) result.

    Figures:
    --------
    Forcing Functions:        The plot of forcing functions, only provided if plotforcing is true.
    State Variables:        The plot of state variables, always provided if plot is true.
    Combined Output:        The plot of the combined terms in the output, provided if C and D are not False.

    """
    solution = 3

    def tuple_to_matrix(x, yx):
        n = yx(x)
        n = _np.asmatrix(n)
        n = n.T
        return n

    def nparr_to_matrix(x, yx):
        n = yx(x)
        n = _np.asmatrix(n)
        if n.shape[1] != 1:
            n = _np.matrix.reshape(n, (n.size, 1))
        return n

    class c_func_concat:

        def __init__(self, funcs):
            self.nfuncs = len(funcs)
            self.func_reg = {}
            for key in range(self.nfuncs):
                self.func_reg[key] = funcs[key]

        def func_c(self, x):
            rets = _np.array([])
            for i in range(self.nfuncs):
                y = self.func_reg[i](x)
                rets = _np.append(rets, y)
            else:
                rets = _np.asmatrix(rets).T
                return rets

    A = _np.asmatrix(A)
    B = _np.asmatrix(B)
    typetest = (
     _np.matrixlib.defmatrix.matrix, _np.ndarray, tuple, list)
    if simpts >= NN:
        _warn('WARNING: NN must be greater than simpts; NN=' + str(NN) + 'simpts=' + str(simpts), ' Autocorrecting simpts to be NN-1.')
        simpts = NN - 1
    if isinstance(C, typetest) and isinstance(D, typetest):
        solution = 3
    else:
        if isinstance(C, typetest) and not isinstance(D, typetest):
            if D == None:
                _warn('WARNING: D matrix not provided; D now assumed to be 0.')
                D = _np.matrix('0')
                solution = 3
            else:
                C = _np.matrix('0')
                D = _np.matrix('0')
                solution = 2
        else:
            C = _np.asmatrix(C)
            D = _np.asmatrix(D)
            if isinstance(func, function):
                mF = f(1)
            else:
                if isinstance(func, (tuple, list)):
                    if isinstance(func[0], function):
                        c_funcs = c_func_concat(func)
                        mF = 'MultiFunctions'
                    else:
                        mF = 'NA'
                else:
                    mF = 'NA'
        if not isinstance(x, typetest):
            if x == None:
                rA = A.shape[0]
                x = _np.asmatrix(_np.zeros(rA)).T
        x = _np.asmatrix(x)
        rA, cA = A.shape
        rB, cB = B.shape
        rx, cx = x.shape
        rC, cC = C.shape
        rD, cD = D.shape
        rF, cF = (1, 1)
    if isinstance(mF, tuple):
        fn = lambda x: tuple_to_matrix(x, func)
        rF, cF = fn(1).shape
    else:
        if isinstance(mF, _np.ndarray):
            fn = lambda x: nparr_to_matrix(x, func)
            rF, cF = fn(1).shape
        else:
            if isinstance(mF, (int, float, _np.float64)):
                fn = f
            else:
                if isinstance(mF, _np.matrixlib.defmatrix.matrix):
                    fn = f
                    rF, cF = fn(1).shape
                else:
                    if mF == 'MultiFunctions':
                        fn = c_funcs.func_c
                        rF, cF = fn(1).shape
                    else:
                        if mF == 'NA':
                            raise ValueError("Forcing function does not meet requirements.\nFunction doesn't return data type: int, float, numpy.ndarray\n or numpy.matrixlib.defmatrix.matrix. Nor does function \ncontain tuple of function handles. Please review function.")
                        elif cA != rA:
                            raise ValueError("Matrix 'A' is not NxN matrix.")
                        else:
                            if rA != rB:
                                if B.size % rA == 0:
                                    _warn("WARNING: Reshaping 'B' matrix to match 'A' matrix.")
                                    B = _np.matrix.reshape(B, (rA, int(B.size / rA)))
                                else:
                                    raise ValueError("'A' matrix dimensions don't match 'B' matrix dimensions.")
                            else:
                                if rA != rx:
                                    if x.size % rA == 0:
                                        _warn("WARNING: Reshaping 'x' matrix to match 'A' matrix.")
                                        x = _np.matrix.reshape(x, (rA, 1))
                                    else:
                                        raise ValueError("'A' matrix dimensions don't match 'B' matrix dimensions.")
                                else:
                                    if cB != rF or cF != 1:
                                        raise ValueError("'B' matrix dimensions don't match forcing function dimensions.")
    if not solution == 3 or cC != cA or rC != 1:
        raise ValueError("'C' matrix dimensions don't match state-space variable dimensions.")
    else:
        if solution == 3 and not cD != rF:
            if rD != 1:
                if cD == rD and cD == 1 and D[0] == 0:
                    D = _np.asmatrix(_np.zeros(rF))
                    _warn("WARNING: Autogenerating 'D' matrix of zeros to match forcing functions.")
                else:
                    raise ValueError("'D' matrix dimensions don't match forcing function dimensions.")
            if f == None:
                if solution != 0:
                    solution = 0
            T = 0
            TT = _np.arange(0, dt * NN, dt)
            yout = 0
            soltype = [
             '(Zero-Input)', '(Zero-State)', '(Complete Simulation)', '(Complete Sim., Combined Output)']
            xtim = {}
            xtim_len = rA
            for n in range(xtim_len):
                key = n
                xtim_init = _np.zeros(NN)
                xtim[key] = xtim_init

            if mF != tint:
                if mF != tfloat:
                    fn_arr = {}
                    for n in range(rF):
                        key = n
                        fn_init = _np.zeros(NN)
                        fn_arr[key] = fn_init
                        fnc = rF

                else:
                    fn_arr = _np.zeros(NN)
                    fnc = 1
                if solution == 1:
                    for n in range(xtim_len):
                        x[n] = 0

            else:
                for i in range(0, simpts):
                    for n in range(xtim_len):
                        xtim[n][i] = x[n]
                    else:
                        if fnc > 1:
                            for n in range(fnc):
                                fn_arr[n][i] = _np.asarray(fn(T))[n][0]

                        else:
                            fn_arr[i] = fn(T)
                        if solution == 0:
                            x = x + dt * A * x
                        else:
                            x = x + dt * A * x + dt * B * fn(T)
                        if solution == 3:
                            yout = yout + dt * D * fn(T)
                        T = T + dt

                else:
                    if plotforcing:
                        fffig = _plt.figure('Forcing Functions')
                        if fnc > 1:
                            for x in range(fnc):
                                _plt.plot(TT, (fn_arr[x]), label=('f' + str(x + 1)))

                        else:
                            _plt.plot(TT, fn_arr, label='f1')
                        if xlim != False:
                            _plt.xlim(xlim)
                        if ylim != False:
                            _plt.ylim(ylim)
                        _plt.title('Forcing Functions ' + title)
                        _plt.xlabel('Time (seconds)')
                        _plt.legend(title='Forcing Functions')
                        _plt.grid()
                        if filename != None:
                            _plt.savefig('Simulation Forcing Functions.png')
                        if plot:
                            _plt.show()
                        stvfig = _plt.figure('State Variables')
                        for x in range(xtim_len):
                            _plt.plot(TT, (xtim[x]), label=('x' + str(x + 1)))
                        else:
                            if xlim != False:
                                _plt.xlim(xlim)
                            if ylim != False:
                                _plt.ylim(ylim)
                            _plt.title('Simulated Output Terms ' + soltype[solution] + title)
                            _plt.xlabel('Time (seconds)')
                            _plt.legend(title='State Variable')
                            _plt.grid()
                            if filename != None:
                                _plt.savefig('Simulation Terms.png')

                        if plot:
                            _plt.show()
                    elif plotresult:
                        if solution == 3:
                            cofig = _plt.figure('Combined Output')
                            C = _np.asarray(C)
                            for i in range(cC):
                                yout = yout + xtim[i] * C[0][i]
                            else:
                                yout = _np.asarray(yout)
                                _plt.plot(TT, yout[0])
                                if xlim != False:
                                    _plt.xlim(xlim)
                                if ylim != False:
                                    _plt.ylim(ylim)
                                _plt.title('Combined Output ' + title)
                                _plt.xlabel('Time (seconds)')
                                _plt.grid()
                                if filename != None:
                                    _plt.savefig('Simulation Combined Output.png')

                            if plot:
                                _plt.show()

                if ret:
                    return (
                     TT, xtim)


def NewtonRaphson(F, J, X0, eps=0.0001, mxiter=100, lsq_eps=0.25):
    """
    Newton Raphson Calculator
    
    Solve nonlinear system F=0 by Newton's method.
    J is the Jacobian of F. Both F and J must be functions of x.
    At input, x holds the start value. The iteration continues
    until ||F|| < eps.
    
    Parameters
    ----------
    F:          array_like
                The Non-Linear System; a function handle/instance.
                The input function must accept only one (1) argument as an
                array or int/float representing the variables required.
    J:          array_like
                The Jacobian of F; a function handle/instance.
                The input Jacobian of F must accept only one (1) argument as
                an array or int/float representing the variables required.
    X0:         array_like
                The Initial Value (or initial guess); a representative array.
    eps:        float, optional
                Epsilon - The error value, default=0.0001
    mxiter:     int, optional
                Maximum Iterations - The highest number of iterations allowed,
                default=100
    lsq_eps:    float, optional
                Least Squares Method (Failover) Epsilon - the error value.
                default=0.25
    
    Returns
    -------
    X0:                 array_like
                        The computed result
    iteration_counter:  int
                        The number of iterations completed before returning
                        either due to solution being found, or max iterations
                        being surpassed.
    
    Examples
    --------
    >>> import numpy as np
    >>> from electricpy import sim # Import Simulation Submodule
    >>> def F(x):
        matr = np.array([[x[1]*10*np.sin(x[0])+2],
            [x[1]*(-10)*np.cos(x[0])+x[1]**2*10+1]])
        return(matr)
    >>> def J(x):
        matr = np.array([[10*x[1]*np.cos(x[0]), 10*np.sin(x[0])],
            [10*x[1]*np.sin(x[0]), -10*np.cos(x[0])+20*x[1]]])
        return(matr)
    # Now compute Newton-Raphson
    >>> X0 = [0, 1]
    >>> results, iter = sim.NewtonRaphson(F,J,X0)
    >>> print(results)
    [-0.236,0.8554]
    >>> print(iter) # Iteration Counter
    4
    
    See Also
    --------
    nr_pq:              Newton-Raphson System Generator
    mbuspowerflow:      Multi-Bus Power Flow Calculator
    
    """
    if isinstance(F(X0), (int, float, _np.float64)):
        if not isinstance(J(X0), (int, float, _np.float64)):
            raise ValueError("ERROR: The Jacobian isn't size-1.")
    else:
        return newton(F, X0, J)
        f0sz = len(F(X0))
        j0sz = len(J(X0))
        if f0sz != j0sz:
            raise ValueError('ERROR: The arguments return arrays or lists of different sizes: f0=' + str(f0sz) + '; j0=' + str(j0sz))

        def inv(m):
            a, b = m.shape
            if a != b:
                raise ValueError('Only square matrices are invertible.')
            i = _np.eye(a, a)
            return _np.linalg.lstsq(m, i, rcond=None)[0]

        F_value = F(X0)
        F_norm = _np.linalg.norm(F_value, ord=2)
        iteration_counter = 0
        teps = eps
        while abs(F_norm) > teps:
            if iteration_counter < mxiter:
                try:
                    delta = _np.linalg.solve(J(X0), -F_value)
                    teps = eps
                except _np.linalg.LinAlgError:
                    try:
                        tst = userhasbeenwarned
                    except NameError:
                        userhasbeenwarned = True
                        _warn('WARNING: Singular matrix, attempting LSQ method.')
                    else:
                        delta = -inv(J(X0)).dot(F_value)
                        teps = lsq_eps
                else:
                    X0 = X0 + delta
                    F_value = F(X0)
                    F_norm = _np.linalg.norm(F_value, ord=2)
                    iteration_counter += 1

    if abs(F_norm) > teps:
        iteration_counter = -1
        _warn('WARNING: Maximum number of iterations exceeded.')
        _warn('Most recent delta:' + str(delta))
        _warn('Most recent F-Norm:' + str(F_norm))
    return (
     X0, iteration_counter)


def nr_pq(Ybus, V_set, P_set, Q_set, extend=True, argshape=False, verbose=False):
    """
    Newton Raphson Real/Reactive Power Function Generator
    
    Given specified parameters, will generate the necessary real and reactive
    power functions necessary to compute the system's power flow.
    
    Parameters
    ----------
    Ybus:       array_like
                Postitive Sequence Y-Bus Matrix for Network.
    V_set:      list of list of float
                List of known and unknown voltages.
                Known voltages should be provided as
                a list of floating values in the form of:
                [mag, ang], unknown voltages should
                be provided as None.
    P_set:      list of float
                List of known and unknown real powers.
                Known powers should be provided as
                a floating point value, unknown powers
                should be provided as None. Generated power
                should be noted as positive, consumed power
                should be noted as negative.
    Q_set:      list of float
                List of known and unknown reactive powers.
                Known powers should be provided as
                a floating point value, unknown powers
                should be provided as None. Generated power
                should be noted as positive, consumed power
                should be noted as negative.
    extend:     bool, optional
                Control argument to format returned value as
                singular function handle or lists of function
                handles. default=True; singular function
    argshape:   bool, optional
                Control argument to force return of the voltage
                argument array as a tuple of: (Θ-len, V-len).
                default=False
    verbose:    bool, optional
                Control argument to print verbose information
                about function generation, useful for debugging.
                default=False
    
    Returns
    -------
    retset:     array_like
                An array of function handles corresponding to
                the appropriate voltage magnitude and angle
                calculation functions based on the real and
                reactive power values. Function(s) will accept
                an argument of the form:
                [Θ1, Θ2,..., Θn, V1, V2,..., Vm]
                where n is the number of busses with unknown
                voltage angle, and m is the number of busses
                with unknown voltage magnitude.
    
    Examples
    --------
    >>> import numpy as np
    >>> from electricpy import sim # Import Simulation Submodule
    >>> ybustest = [[-10j,10j],
        [10j,-10j]]
    >>> Vlist = [[1,0],[None,None]] # We don't know the voltage or angle at bus 2
    >>> Plist = [None,-2.0] # 2pu watts consumed
    >>> Qlist = [None,-1.0] # 1pu vars consumed
    >>> F = nr_pq(ybustest,Vlist,Plist,Qlist)
    >>> X0 = [0,1] # Define Initial Conditions
    >>> J = sim.jacobian(F) # Find Jacobian
    >>> # Now use Newton-Raphson to Solve
    >>> results, iter = sim.NewtonRaphson(F,J,X0)
    >>> print(results)
    [-0.236,0.8554]
    >>> print(iter) # Iteration Counter
    4
    
    See Also
    --------
    NewtonRaphson:      Newton-Raphson System Solver
    mbuspowerflow:      Multi-Bus Power Flow Calculator
    
    """
    global P_funcs
    global P_list
    global P_strgs
    global Q_funcs
    global Q_list
    global Q_strgs
    global V_list
    global YBUS
    Ybus = _np.asarray(Ybus)
    row, col = Ybus.shape
    N = row
    if row != col:
        raise ValueError('Invalid Y-Bus Shape')
    if N != len(V_set):
        raise ValueError('Invalid V_set Shape')
    if N != len(P_set):
        raise ValueError('Invalid P_set Shape')
    if N != len(Q_set):
        raise ValueError('Invalid Q_set Shape')
    for i in range(N):
        if all((P_set[i], Q_set[i], V_set[i][0])):
            raise ValueError('Over-Constrained System')
    else:

        class c_func_concat:

            def __init__(self, funcs):
                self.nfuncs = len(funcs)
                self.func_reg = {}
                for key in range(self.nfuncs):
                    self.func_reg[key] = funcs[key]

            def func_c(self, x):
                rets = _np.array([])
                for i in range(self.nfuncs):
                    y = self.func_reg[i](x)
                    rets = _np.append(rets, y)
                else:
                    return rets

        P_funcs = []
        Q_funcs = []
        P_strgs = []
        Q_strgs = []
        Vi_list = []
        lists = [
         P_strgs, Q_strgs]
        i = 0
        ii = 0
        V_list = V_set
        YBUS = Ybus
        P_list = P_set
        Q_list = Q_set
        Pstr = '{0}*{2}*(YBUS{4}.real*_np.cos({1}-{3})+YBUS{4}.imag*_np.sin({1}-{3}))'
        Qstr = '{0}*{2}*(YBUS{4}.real*_np.sin({1}-{3})-YBUS{4}.imag*_np.cos({1}-{3})){5}'
        ang_len = 0
        mag_len = 0
        magoff = 1
        angoff = 1
        for _k in range(N):
            Padd = False
            Qadd = False

    for _j in range(N):
        if P_list[_k] == None:
            pass
        else:
            if _k != _j:
                if not Padd:
                    ang_len += 1
                    Padd = True
            if _k != _j and Q_list[_k] != None:
                Qadd or mag_len += 1
                Qadd = True
    else:
        Vxdim = ang_len + mag_len
        if verbose:
            print("Angle EQ's (P):", ang_len, "\tMagnitude EQ's (Q):", mag_len)
            print('Vx Dimension:', Vxdim)
        for _k in range(N):
            newentry = True

    for _j in range(N):
        for LST in lists:
            LST.append(None)

        if P_list[_k] == None:
            pass
        else:
            Yind = '[{}][{}]'.format(_k, _j)
            if verbose:
                print('K:', _k, '\tJ:', _j)
            if _k != _j:
                if V_list[_k][0] == None:
                    Vkm = 'Vx[{}]'.format(_k + ang_len - magoff * _k)
                    Vka = 'Vx[{}]'.format(_k - angoff)
                else:
                    Vkm = 'V_list[{}][0]'.format(_k)
                    if V_list[_k][1] == None:
                        Vka = 'Vx[{}]'.format(_k - angoff)
                    else:
                        Vka = 'V_list[{}][1]'.format(_k)
                if V_list[_j][0] == None:
                    Vjm = 'Vx[{}]'.format(_j + ang_len - magoff * _j)
                    Vja = 'Vx[{}]'.format(_j - angoff)
                else:
                    Vjm = 'V_list[{}][0]'.format(_j)
                    if V_list[_j][1] == None:
                        Vja = 'Vx[{}]'.format(_j - angoff)
                    else:
                        Vja = 'V_list[{}][1]'.format(_j)
                P_strgs[i] = Pstr.format(Vkm, Vka, Vjm, Vja, Yind)
                if verbose:
                    print('New P-String:', P_strgs[i])
                if Q_list[_k] != None:
                    if newentry:
                        newentry = False
                        Qgen = '-Vx[{0}]**2*YBUS[{0}][{0}].imag'.format(_k)
                    else:
                        Qgen = ''
                    Q_strgs[i] = Qstr.format(Vkm, Vka, Vjm, Vja, Yind, Qgen)
                    if verbose:
                        print('New Q-String:', Q_strgs[i])
            i += 1
    else:
        tempPstr = 'P_funcs.append(lambda Vx: -P_list[{0}]'.format(_k)
        tempQstr = 'Q_funcs.append(lambda Vx: -Q_list[{0}]'.format(_k)
        for _i in range(ii, i):
            P = P_strgs[_i]
            Q = Q_strgs[_i]
            if P != None:
                tempPstr += '+' + P
            if Q != None:
                tempQstr += '+' + Q
            tempPstr += ')'
            tempQstr += ')'
            if any(P_strgs[ii:i]):
                if verbose:
                    print('Full P-Func Str:', tempPstr)
                exec(tempPstr)
            if any(Q_strgs[ii:i]):
                if verbose:
                    print('Full Q-Func Str:', tempQstr)
                exec(tempQstr)
            ii = i
        else:
            retset = (
             P_funcs, Q_funcs)
            if extend:
                funcset = P_funcs.copy()
                funcset.extend(Q_funcs)
                funcgroup = c_func_concat(funcset)
                retset = funcgroup.func_c
            if argshape:
                retset = (
                 retset, (ang_len, mag_len))
            return retset


def mbuspowerflow(Ybus, Vknown, Pknown, Qknown, X0='flatstart', eps=0.0001, mxiter=100, returnct=False, degrees=True, split=False, slackbus=0, lsq_eps=0.25):
    """
    Multi-Bus Power Flow Calculator
    
    Function wrapper to simplify the evaluation of a power flow calculation.
    Determines the function array (F) and the Jacobian array (J) and uses the
    Newton-Raphson method to iteratively evaluate the system to converge to a
    solution.
    
    Parameters
    ----------
    Ybus:       array_like
                Postitive Sequence Y-Bus Matrix for Network.
    Vknown:     list of list of float
                List of known and unknown voltages.
                Known voltages should be provided as
                a list of floating values in the form of:
                [mag, ang], unknown voltages should
                be provided as None.
    Pknown:     list of float
                List of known and unknown real powers.
                Known powers should be provided as
                a floating point value, unknown powers
                should be provided as None. Generated power
                should be noted as positive, consumed power
                should be noted as negative.
    Qknown:     list of float
                List of known and unknown reactive powers.
                Known powers should be provided as
                a floating point value, unknown powers
                should be provided as None. Generated power
                should be noted as positive, consumed power
                should be noted as negative.
    X0:         {'flatstart', list of float}, optional
                Initial conditions/Initial guess. May be set
                to 'flatstart' to force function to generate
                flat voltages and angles of 1∠0°. Must be
                specified in the form:
                [Θ1, Θ2,..., Θn, V1, V2,..., Vm]
                where n is the number of busses with unknown
                voltage angle, and m is the number of busses
                with unknown voltage magnitude.
    eps:        float, optional
                Epsilon - The error value, default=0.0001
    mxiter:     int, optional
                Maximum Iterations - The highest number of
                iterations allowed, default=100
    returnct:   bool, optional
                Control argument to force function to return
                the iteration counter from the Newton-Raphson
                solution. default=False
    degrees:    bool, optional
                Control argument to force returned angles to
                degrees. default=True
    split:      bool, optional
                Control argument to force returned array to
                split into lists of magnitudes and angles.
                default=False
    slackbus:   int, optional
                Control argument to specify the bus index for
                the slack bus. If the slack bus is not positioned
                at bus index 1 (default), this control can be
                used to reformat the data sets to a format
                necessary for proper generation and Newton
                Raphson computation. Must be zero-based.
                default=0
    lsq_eps:    float, optional
                Least Squares Method (Failover) Epsilon - the error value.
                default=0.25
    
    
    .. image:: /_static/mbuspowerflow_example.png
    
    Examples
    --------
    >>> # Perform Power-Flow Analysis for Figure
    >>> import numpy as np
    >>> from electricpy import sim # Import Simulation Submodule
    >>> ybustest = [[-10j,10j],
        [10j,-10j]]
    >>> Vlist = [[1,0],[None,None]] # We don't know the voltage or angle at bus 2
    >>> Plist = [None,-2.0] # 2pu watts consumed
    >>> Qlist = [None,-1.0] # 1pu vars consumed
    >>> nr_res = sim.mbuspowerflow(ybustest,Vlist,Plist,Qlist,degrees=True,split=True,returnct=True)
    >>> print(nr_res)
    ([array([-13.52185223]), array([ 0.85537271])], 4)
    
    See Also
    --------
    NewtonRaphson:          Newton-Raphson System Solver
    nr_pq:                  Newton-Raphson System Generator
    electricpy.powerflow:   Simple (2-bus) Power Flow Calculator
    """
    if slackbus != 0:
        Ybus = _np.asarray(Ybus)
        row, col = Ybus.shape
        Ybus = _np.roll(Ybus, col - slackbus, (0, 1))
        Vknown = _np.roll(Vknown, len(Vknown) - slackbus, 0).tolist()
        Pknown = _np.roll(Pknown, len(Pknown) - slackbus, 0).tolist()
        Qknown = _np.roll(Qknown, len(Qknown) - slackbus, 0).tolist()
    else:
        F, shp = nr_pq(Ybus, Vknown, Pknown, Qknown, True, True, False)
        if X0 == 'flatstart':
            ang_len, mag_len = shp
            X0 = _np.append(_np.zeros(ang_len), _np.ones(mag_len))
        J = jacobian(F)
        nr_result, iter_count = NewtonRaphson(F, J, X0, eps, mxiter, lsq_eps)
        if degrees:
            for i in range(ang_len):
                nr_result[i] = _np.degrees(nr_result[i])

    if split:
        nr_result = [
         nr_result[:ang_len], nr_result[-mag_len:]]
    if returnct:
        return (
         nr_result, iter_count)
    return nr_result