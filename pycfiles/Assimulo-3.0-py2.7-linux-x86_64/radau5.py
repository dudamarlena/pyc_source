# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/solvers/radau5.py
# Compiled at: 2018-10-13 05:07:25
import numpy as N, scipy as S, scipy.linalg as LIN, scipy.sparse as sp
from assimulo.exception import *
from assimulo.ode import *
from assimulo.explicit_ode import Explicit_ODE
from assimulo.implicit_ode import Implicit_ODE
from assimulo.lib.radau_core import Radau_Common
from assimulo.lib import radau5

class Radau5Error(AssimuloException):
    """
    Defines the Radau5Error and provides the textual error message.
    """
    msg = {-1: 'The input is not consistent.', -2: 'The solver took max internal steps but could not reach the next output time.', 
       -3: 'The step size became too small.', 
       -4: 'The matrix is repeatedly singular.', 
       -5: 'Repeated unexpected step rejections.'}

    def __init__(self, value, t=0.0):
        self.value = value
        self.t = t

    def __str__(self):
        try:
            return repr(self.msg[self.value] + ' At time %f.' % self.t)
        except KeyError:
            return repr('Radau failed with flag %s. At time %f.' % (self.value, self.t))


class Radau5ODE(Radau_Common, Explicit_ODE):
    """
    Radau IIA fifth-order three-stages with step-size control and 
    continuous output. Based on the FORTRAN code RADAU5 by E.Hairer and 
    G.Wanner, which can be found here: 
    http://www.unige.ch/~hairer/software.html
    
    Details about the implementation (FORTRAN) can be found in the book,::
    
        Solving Ordinary Differential Equations II,
        Stiff and Differential-Algebraic Problems
        
        Authors: E. Hairer and G. Wanner
        Springer-Verlag, ISBN: 3-540-60452-9
    
    """

    def __init__(self, problem):
        """
        Initiates the solver.
        
            Parameters::
            
                problem     
                            - The problem to be solved. Should be an instance
                              of the 'Explicit_Problem' class.
        """
        Explicit_ODE.__init__(self, problem)
        self.options['inith'] = 0.01
        self.options['newt'] = 7
        self.options['thet'] = 0.001
        self.options['fnewt'] = 0.0
        self.options['quot1'] = 1.0
        self.options['quot2'] = 1.2
        self.options['fac1'] = 0.2
        self.options['fac2'] = 8.0
        self.options['maxh'] = N.inf
        self.options['safe'] = 0.9
        self.options['atol'] = 1e-06 * N.ones(self.problem_info['dim'])
        self.options['rtol'] = 1e-06
        self.options['usejac'] = True if self.problem_info['jac_fcn'] else False
        self.options['maxsteps'] = 100000
        self.supports['report_continuously'] = True
        self.supports['interpolated_output'] = True
        self.supports['state_events'] = True
        self._leny = len(self.y)
        self._type = '(explicit)'
        self._event_info = None
        self._werr = N.zeros(self._leny)
        return

    def initialize(self):
        self.statistics.reset()

    def set_problem_data(self):
        if self.problem_info['state_events']:

            def event_func(t, y):
                return self.problem.state_events(t, y, self.sw)

            def f(t, y):
                ret = 0
                try:
                    rhs = self.problem.rhs(t, y, self.sw)
                except (N.linalg.LinAlgError, ZeroDivisionError, AssimuloRecoverableError):
                    rhs = y.copy()
                    ret = -1

                return (
                 rhs, [ret])

            self.f = f
            self.event_func = event_func
            self._event_info = [0] * self.problem_info['dimRoot']
            self.g_old = self.event_func(self.t, self.y)
        else:

            def f(t, y):
                ret = 0
                try:
                    rhs = self.problem.rhs(t, y)
                except (N.linalg.LinAlgError, ZeroDivisionError, AssimuloRecoverableError):
                    rhs = y.copy()
                    ret = -1

                return (
                 rhs, [ret])

            self.f = f

    def interpolate(self, time):
        y = N.empty(self._leny)
        for i in range(self._leny):
            y[i] = radau5.contr5(i + 1, time, self.cont)

        return y

    def get_weighted_local_errors(self):
        """
        Returns the vector of weighted estimated local errors at the current step.
        """
        return N.abs(self._werr)

    def _solout(self, nrsol, told, t, y, cont, werr, lrc, irtrn):
        """
        This method is called after every successful step taken by Radau5
        """
        self.cont = cont
        self._werr = werr
        if self.problem_info['state_events']:
            flag, t, y = self.event_locator(told, t, y)
            if flag == ID_PY_EVENT:
                irtrn = -1
        if self._opts['report_continuously']:
            initialize_flag = self.report_solution(t, y, self._opts)
            if initialize_flag:
                irtrn = -1
        else:
            if self._opts['output_list'] is None:
                self._tlist.append(t)
                self._ylist.append(y.copy())
            else:
                output_list = self._opts['output_list']
                output_index = self._opts['output_index']
                try:
                    while output_list[output_index] <= t:
                        self._tlist.append(output_list[output_index])
                        self._ylist.append(self.interpolate(output_list[output_index]))
                        output_index += 1

                except IndexError:
                    pass

            self._opts['output_index'] = output_index
            if self.problem_info['state_events'] and flag == ID_PY_EVENT and len(self._tlist) > 0 and self._tlist[(-1)] != t:
                self._tlist.append(t)
                self._ylist.append(y)
        return irtrn

    def _jacobian(self, t, y):
        """
        Calculates the Jacobian, either by an approximation or by the user
        defined (jac specified in the problem class).
        """
        jac = self.problem.jac(t, y)
        if isinstance(jac, sp.csc_matrix):
            jac = jac.toarray()
        return jac

    def integrate(self, t, y, tf, opts):
        ITOL = 1
        IJAC = 1 if self.usejac else 0
        MLJAC = self.problem_info['dim']
        MUJAC = self.problem_info['dim']
        IMAS = 0
        MLMAS = self.problem_info['dim']
        MUMAS = self.problem_info['dim']
        IOUT = 1
        WORK = N.array([0.0] * (4 * self.problem_info['dim'] ** 2 + 12 * self.problem_info['dim'] + 20))
        IWORK = N.array([0] * (3 * self.problem_info['dim'] + 20))
        WORK[1] = self.safe
        WORK[2] = self.thet
        WORK[3] = self.fnewt
        WORK[4] = self.quot1
        WORK[5] = self.quot2
        WORK[6] = self.maxh
        WORK[7] = self.fac1
        WORK[8] = self.fac2
        IWORK[1] = self.maxsteps
        IWORK[2] = self.newt
        mas_dummy = lambda t: x
        jac_dummy = (lambda t: x) if not self.usejac else self._jacobian
        if opts['initialize']:
            self.set_problem_data()
            self._tlist = []
            self._ylist = []
        self._opts = opts
        t, y, h, iwork, flag = radau5.radau5(self.f, t, y.copy(), tf, self.inith, self.rtol * N.ones(self.problem_info['dim']), self.atol, ITOL, jac_dummy, IJAC, MLJAC, MUJAC, mas_dummy, IMAS, MLMAS, MUMAS, self._solout, IOUT, WORK, IWORK)
        if flag == 1:
            flag = ID_PY_COMPLETE
        elif flag == 2:
            flag = ID_PY_EVENT
        else:
            raise Radau5Error(flag, t)
        self.statistics['nsteps'] += iwork[16]
        self.statistics['nfcns'] += iwork[13]
        self.statistics['njacs'] += iwork[14]
        self.statistics['nfcnjacs'] += (self.usejac or iwork[14]) * self.problem_info['dim'] if 1 else 0
        self.statistics['nerrfails'] += iwork[17]
        self.statistics['nlus'] += iwork[18]
        return (
         flag, self._tlist, self._ylist)

    def state_event_info(self):
        return self._event_info

    def set_event_info(self, event_info):
        self._event_info = event_info

    def print_statistics(self, verbose=NORMAL):
        """
        Prints the run-time statistics for the problem.
        """
        Explicit_ODE.print_statistics(self, verbose)
        self.log_message('\nSolver options:\n', verbose)
        self.log_message(' Solver                  : Radau5 ' + self._type, verbose)
        self.log_message(' Tolerances (absolute)   : ' + str(self._compact_atol()), verbose)
        self.log_message(' Tolerances (relative)   : ' + str(self.options['rtol']), verbose)
        self.log_message('', verbose)


class _Radau5ODE(Radau_Common, Explicit_ODE):
    """
    Radau IIA fifth-order three-stages with step-size control and continuous output.
    Based on the FORTRAN code by E.Hairer and G.Wanner, which can be found here: 
    http://www.unige.ch/~hairer/software.html
    
    Details about the implementation (FORTRAN) can be found in the book,::
    
        Solving Ordinary Differential Equations II,
        Stiff and Differential-Algebraic Problems
        
        Authors: E. Hairer and G. Wanner
        Springer-Verlag, ISBN: 3-540-60452-9
    
    This code is aimed at providing a Python implementation of the original code.
    """

    def __init__(self, problem):
        """
        Initiates the solver.
        
            Parameters::
            
                problem     
                            - The problem to be solved. Should be an instance
                              of the 'Explicit_Problem' class.
        """
        Explicit_ODE.__init__(self, problem)
        self.options['inith'] = 0.01
        self.options['newt'] = 7
        self.options['thet'] = 0.001
        self.options['fnewt'] = 0
        self.options['quot1'] = 1.0
        self.options['quot2'] = 1.2
        self.options['fac1'] = 0.2
        self.options['fac2'] = 8.0
        self.options['maxh'] = N.inf
        self.options['safe'] = 0.9
        self.options['atol'] = 1e-06
        self.options['rtol'] = 1e-06
        self.options['usejac'] = True if self.problem_info['jac_fcn'] else False
        self.options['maxsteps'] = 10000
        self._curjac = False
        self._itfail = False
        self._needjac = True
        self._needLU = True
        self._first = True
        self._rejected = True
        self._leny = len(self.y)
        self._oldh = 0.0
        self._olderr = 1.0
        self._eps = N.finfo('double').eps
        self._col_poly = N.zeros(self._leny * 3)
        self._type = '(explicit)'
        self._curiter = 0
        self.f = problem.rhs_internal
        self.Y1 = N.array([0.0] * len(self.y0))
        self.Y2 = N.array([0.0] * len(self.y0))
        self.Y3 = N.array([0.0] * len(self.y0))
        self._f0 = N.array([0.0] * len(self.y0))
        self.supports['one_step_mode'] = True
        self.supports['interpolated_output'] = True
        self._load_parameters()

    def initialize(self):
        self.statistics.reset()

    def step_generator(self, t, y, tf, opts):
        if opts['initialize']:
            self._oldh = self.inith
            self.h = self.inith
            self._fac_con = 1.0
        if self.fnewt == 0:
            self.fnewt = max(10.0 * self._eps / self.rtol, min(0.03, self.rtol ** 0.5))
        self.f(self._f0, t, y)
        self.statistics['nfcns'] += 1
        self._tc = t
        self._yc = y
        for i in range(self.maxsteps):
            if t < tf:
                t, y = self._step(t, y)
                self._tc = t
                self._yc = y
                if self.h > N.abs(tf - t):
                    self.h = N.abs(tf - t)
                if t < tf:
                    yield (
                     ID_PY_OK, t, y)
                else:
                    yield (
                     ID_PY_COMPLETE, t, y)
                    break
                self._first = False
        else:
            raise Explicit_ODE_Exception('Final time not reached within maximum number of steps')

    def step(self, t, y, tf, opts):
        if opts['initialize']:
            self._next_step = self.step_generator(t, y, tf, opts)
        return next(self._next_step)

    def integrate(self, t, y, tf, opts):
        if opts['output_list'] is not None:
            output_list = opts['output_list']
            output_index = opts['output_index']
            next_step = self.step_generator(t, y, tf, opts)
            tlist, ylist = [], []
            res = [
             ID_PY_OK]
            while res[0] != ID_PY_COMPLETE:
                res = next(next_step)
                try:
                    while output_list[output_index] <= res[1]:
                        tlist.append(output_list[output_index])
                        ylist.append(self.interpolate(output_list[output_index]))
                        output_index = output_index + 1

                except IndexError:
                    pass

            return (res[0], tlist, ylist)
        else:
            flags, tlist, ylist = list(zip(*list(self.step_generator(t, y, tf, opts))))
            return (
             flags[(-1)], tlist, ylist)
            return

    def _step(self, t, y):
        """
        This calculates the next step in the integration.
        """
        self._scaling = N.array(abs(y) * self.rtol + self.atol)
        while True:
            self.newton(t, y)
            self._err = self.estimate_error()
            if self._err > 1.0:
                self._rejected = True
                self.statistics['nerrfails'] += 1
                ho = self.h
                self.h = self.adjust_stepsize(self._err)
                self.log_message('Rejecting step at ' + str(t) + 'with old stepsize' + str(ho) + 'and new ' + str(self.h), SCREAM)
                if self._curjac or self._curiter == 1:
                    self._needjac = False
                    self._needLU = True
                else:
                    self._needjac = True
                    self._needLU = True
            else:
                self.log_message('Accepting step at ' + str(t) + 'with stepsize ' + str(self.h), SCREAM)
                self.statistics['nsteps'] += 1
                tn = t + self.h
                yn = y + self._Z[2 * self._leny:3 * self._leny]
                self.f(self._f0, tn, yn)
                self.statistics['nfcns'] += 1
                self._oldoldh = self._oldh
                self._oldh = self.h
                self._oldt = t
                self._newt = tn
                ht = self.adjust_stepsize(self._err, predict=True)
                self.h = min(self.h, ht) if self._rejected else ht
                self._rejected = False
                self._curjac = False
                if self._oldoldh == self.h and self._theta <= self.thet:
                    self._needjac = False
                    self._needLU = False
                elif self._theta <= self.thet:
                    self._needjac = False
                    self._needLU = True
                else:
                    self._needjac = True
                    self._needLU = True
                if self.thet < 0:
                    self._needjac = True
                    self._needLU = True
                self._olderr = max(self._err, 0.01)
                break

        self._col_poly = self._collocation_pol(self._Z, self._col_poly, self._leny)
        return (
         tn, yn)

    def _collocation_pol(self, Z, col_poly, leny):
        col_poly[(2 * leny):(3 * leny)] = Z[:leny] / self.C[(0, 0)]
        col_poly[leny:(2 * leny)] = (Z[:leny] - Z[leny:2 * leny]) / (self.C[(0, 0)] - self.C[(1,
                                                                                              0)])
        col_poly[:leny] = (Z[leny:2 * leny] - Z[2 * leny:3 * leny]) / (self.C[(1, 0)] - 1.0)
        col_poly[(2 * leny):(3 * leny)] = (col_poly[leny:2 * leny] - col_poly[2 * leny:3 * leny]) / self.C[(1,
                                                                                                            0)]
        col_poly[leny:(2 * leny)] = (col_poly[leny:2 * leny] - col_poly[:leny]) / (self.C[(0,
                                                                                           0)] - 1.0)
        col_poly[(2 * leny):(3 * leny)] = col_poly[leny:2 * leny] - col_poly[2 * leny:3 * leny]
        return col_poly

    def _radau_F(self, Z, t, y):
        Z1 = Z[:self._leny]
        Z2 = Z[self._leny:2 * self._leny]
        Z3 = Z[2 * self._leny:3 * self._leny]
        self.f(self.Y1, t + self.C[0] * self.h, y + Z1)
        self.f(self.Y2, t + self.C[1] * self.h, y + Z2)
        self.f(self.Y3, t + self.C[2] * self.h, y + Z3)
        self.statistics['nfcns'] += 3
        return N.hstack((N.hstack((self.Y1, self.Y2)), self.Y3))

    def calc_start_values(self):
        """
        Calculate newton starting values.
        """
        if self._first:
            Z = N.zeros(self._leny * 3)
            W = N.zeros(self._leny * 3)
        else:
            Z = self._Z
            cq = self.C * self.h / self._oldh
            newtval = self._col_poly
            leny = self._leny
            Z[:leny] = cq[(0, 0)] * (newtval[:leny] + (cq[(0, 0)] - self.C[(1, 0)] + 1.0) * (newtval[leny:2 * leny] + (cq[(0,
                                                                                                                           0)] - self.C[(0,
                                                                                                                                         0)] + 1.0) * newtval[2 * leny:3 * leny]))
            Z[leny:(2 * leny)] = cq[(1, 0)] * (newtval[:leny] + (cq[(1, 0)] - self.C[(1,
                                                                                      0)] + 1.0) * (newtval[leny:2 * leny] + (cq[(1,
                                                                                                                                  0)] - self.C[(0,
                                                                                                                                                0)] + 1.0) * newtval[2 * leny:3 * leny]))
            Z[(2 * leny):(3 * leny)] = cq[(2, 0)] * (newtval[:leny] + (cq[(2, 0)] - self.C[(1,
                                                                                            0)] + 1.0) * (newtval[leny:2 * leny] + (cq[(2,
                                                                                                                                        0)] - self.C[(0,
                                                                                                                                                      0)] + 1.0) * newtval[2 * leny:3 * leny]))
            W = N.dot(self.T2, Z)
        return (Z, W)

    def newton(self, t, y):
        """
        The newton iteration. 
        """
        for k in range(20):
            self._curiter = 0
            self._fac_con = max(self._fac_con, self._eps) ** 0.8
            self._theta = abs(self.thet)
            if self._needjac:
                self._jac = self.jacobian(t, y)
            if self._needLU:
                self.statistics['nlus'] += 1
                self._a = self._alpha / self.h
                self._b = self._beta / self.h
                self._g = self._gamma / self.h
                self._B = self._g * self.I - self._jac
                self._P1, self._L1, self._U1 = S.linalg.lu(self._B)
                self._P2, self._L2, self._U2 = S.linalg.lu(self._a * self.I - self._jac)
                self._P3, self._L3, self._U3 = S.linalg.lu(self._b * self.I - self._jac)
                self._needLU = False
                if min(abs(N.diag(self._U1))) < self._eps:
                    raise Explicit_ODE_Exception('Error, gI-J is singular.')
            Z, W = self.calc_start_values()
            for i in range(self.newt):
                self._curiter += 1
                self.statistics['nniters'] += 1
                Z = N.dot(self.T2, self._radau_F(Z.real, t, y))
                Z[:(self._leny)] = Z[:self._leny] - self._g * N.dot(self.I, W[:self._leny])
                Z[(self._leny):(2 * self._leny)] = Z[self._leny:2 * self._leny] - self._a * N.dot(self.I, W[self._leny:2 * self._leny])
                Z[(2 * self._leny):(3 * self._leny)] = Z[2 * self._leny:3 * self._leny] - self._b * N.dot(self.I, W[2 * self._leny:3 * self._leny])
                Z[:(self._leny)] = N.linalg.solve(self._U1, N.linalg.solve(self._L1, N.linalg.solve(self._P1, Z[:self._leny])))
                Z[(self._leny):(2 * self._leny)] = N.linalg.solve(self._U2, N.linalg.solve(self._L2, N.linalg.solve(self._P2, Z[self._leny:2 * self._leny])))
                Z[(2 * self._leny):(3 * self._leny)] = N.linalg.solve(self._U3, N.linalg.solve(self._L3, N.linalg.solve(self._P3, Z[2 * self._leny:3 * self._leny])))
                newnrm = N.linalg.norm(Z.reshape(-1, self._leny) / self._scaling, 'fro') / N.sqrt(3.0 * self._leny)
                if i > 0:
                    thq = newnrm / oldnrm
                    if i == 1:
                        self._theta = thq
                    else:
                        self._theta = N.sqrt(thq * thqold)
                    thqold = thq
                    if self._theta < 0.99:
                        self._fac_con = self._theta / (1.0 - self._theta)
                        dyth = self._fac_con * newnrm * self._theta ** (self.newt - (i + 1) - 1) / self.fnewt
                        if dyth >= 1.0:
                            qnewt = max(0.0001, min(20.0, dyth))
                            self.h = 0.8 * qnewt ** (-1.0 / (4.0 + self.newt - (i + 1) - 1)) * self.h
                            self._itfail = True
                            self._rejected = True
                            break
                    else:
                        self._itfail = True
                        break
                oldnrm = max(newnrm, self._eps)
                W = W + Z
                Z = N.dot(self.T3, W)
                if self._fac_con * newnrm <= self.fnewt:
                    self._itfail = False
                    break
            else:
                self._itfail = True

            if not self._itfail:
                self._Z = Z.real
                break
            else:
                self.log_message('Iteration failed at time %e with step-size %e' % (t, self.h), SCREAM)
                self.statistics['nnfails'] += 1
                self._rejected = True
                if self._theta >= 0.99:
                    self.h = self.h / 2.0
                if self._curjac:
                    self._needjac = False
                    self._needLU = True
                else:
                    self._needjac = True
                    self._needLU = True
        else:
            raise Explicit_ODE_Exception('Newton iteration failed at time %e with step-size %e' % (t, self.h))

    def adjust_stepsize(self, err, predict=False):
        fac = min(self.safe, self.safe * (2.0 * self.newt + 1.0) / (2.0 * self.newt + self._curiter))
        quot = max(1.0 / self.fac2, min(1.0 / self.fac1, err ** 0.25 / fac))
        hnormal = self.h / quot
        if predict:
            if not self._first:
                facgus = self._hacc / self.h * (err ** 2 / self._olderr) ** 0.25 / self.safe
                facgus = max(1.0 / self.fac2, min(1.0 / self.fac1, facgus))
                quot = max(quot, facgus)
                h = self.h / quot
            else:
                h = hnormal
            self._hacc = self.h
        else:
            h = hnormal
        qt = h / self.h
        if qt >= self.quot1 and qt <= self.quot2:
            h = self.h
        if self._first and err >= 1.0:
            h = self.h / 10.0
        if h < self._eps:
            raise Explicit_ODE_Exception('Step-size to small at %e with h = %e' % (self._tc, self.h))
        if h > self.maxh:
            h = self.maxh
        return h

    def estimate_error(self):
        temp = 1.0 / self.h * (self.E[0] * self._Z[:self._leny] + self.E[1] * self._Z[self._leny:2 * self._leny] + self.E[2] * self._Z[2 * self._leny:3 * self._leny])
        scal = self._scaling
        err_v = N.linalg.solve(self._U1, N.linalg.solve(self._L1, N.linalg.solve(self._P1, self._f0 + temp)))
        err = N.linalg.norm(err_v / scal)
        err = max(err / N.sqrt(self._leny), 1e-10)
        if (self._rejected or self._first) and err >= 1.0:
            self.statistics['nfcns'] += 1
            err_new = N.array([0.0] * self._leny)
            self.f(err_new, self._tc, self._yc + err_v)
            err_v = N.linalg.solve(self._U1, N.linalg.solve(self._L1, N.linalg.solve(self._P1, err_new + temp)))
            err = N.linalg.norm(err_v / scal)
            err = max(err / N.sqrt(self._leny), 1e-10)
        return err

    def jacobian(self, t, y):
        """
        Calculates the Jacobian, either by an approximation or by the user
        defined (jac specified in the problem class).
        """
        self._curjac = True
        self._needLU = True
        self._needjac = False
        if self.usejac:
            cjac = self.problem.jac(t, y)
        else:
            delt = N.array([ (self._eps * max(abs(yi), 1e-05)) ** 0.5 for yi in y ]) * N.identity(self._leny)
            Fdelt = N.array([ self.problem.rhs(t, y + e) for e in delt ])
            grad = ((Fdelt - self.problem.rhs(t, y)).T / delt.diagonal()).T
            cjac = N.array(grad).T
            self.statistics['nfcnjacs'] += 1 + self._leny
        self.statistics['njacs'] += 1
        return cjac

    def interpolate(self, t, k=0):
        """
        Calculates the continuous output from Radau5.
        """
        leny = self._leny
        s = (t - self._newt) / self._oldh
        Z = self._col_poly
        yout = self._yc + s * (Z[:leny] + (s - self.C[(1, 0)] + 1.0) * (Z[leny:2 * leny] + (s - self.C[(0,
                                                                                                        0)] + 1.0) * Z[2 * leny:3 * leny]))
        return yout

    def _load_parameters(self):
        A = N.zeros([3, 3])
        A[(0, 0)] = (88.0 - 7.0 * N.sqrt(6.0)) / 360.0
        A[(0, 1)] = (296.0 - 169.0 * N.sqrt(6.0)) / 1800.0
        A[(0, 2)] = (-2.0 + 3.0 * N.sqrt(6.0)) / 225.0
        A[(1, 0)] = (296.0 + 169.0 * N.sqrt(6.0)) / 1800.0
        A[(1, 1)] = (88.0 + 7.0 * N.sqrt(6.0)) / 360.0
        A[(1, 2)] = (-2.0 - 3.0 * N.sqrt(6.0)) / 225.0
        A[(2, 0)] = (16.0 - N.sqrt(6.0)) / 36.0
        A[(2, 1)] = (16.0 + N.sqrt(6.0)) / 36.0
        A[(2, 2)] = 1.0 / 9.0
        C = N.zeros([3, 1])
        C[(0, 0)] = (4.0 - N.sqrt(6.0)) / 10.0
        C[(1, 0)] = (4.0 + N.sqrt(6.0)) / 10.0
        C[(2, 0)] = 1.0
        B = N.zeros([1, 3])
        B[(0, 0)] = (16.0 - N.sqrt(6.0)) / 36.0
        B[(0, 1)] = (16.0 + N.sqrt(6.0)) / 36.0
        B[(0, 2)] = 1.0 / 9.0
        E = N.zeros(3)
        E[0] = -13.0 - 7.0 * N.sqrt(6.0)
        E[1] = -13.0 + 7.0 * N.sqrt(6.0)
        E[2] = -1.0
        E = 1.0 / 3.0 * E
        Ainv = N.linalg.inv(A)
        eig, T = N.linalg.eig(Ainv)
        eig = N.array([eig[2], eig[0], eig[1]])
        J = N.diag(eig)
        self._alpha = eig[1]
        self._beta = eig[2]
        self._gamma = eig[0].real
        temp0 = T[:, 0].copy()
        temp1 = T[:, 1].copy()
        temp2 = T[:, 2].copy()
        T[:, 0] = temp2
        T[:, 1] = temp0
        T[:, 2] = temp1
        Tinv = N.linalg.inv(T)
        I = N.eye(self._leny)
        I3 = N.eye(3)
        T1 = N.kron(J, I)
        T2 = N.kron(Tinv, I)
        T3 = N.kron(T, I)
        self.A = A
        self.B = B
        self.C = C
        self.I = I
        self.E = E
        self.T1 = T1
        self.T2 = T2
        self.T3 = T3
        self.I3 = I3
        self.EIG = eig


class Radau5DAE(Radau_Common, Implicit_ODE):
    """
    Radau IIA fifth-order three-stages with step-size control and 
    continuous output. Based on the FORTRAN code RADAU5 by E.Hairer and 
    G.Wanner, which can be found here: 
    http://www.unige.ch/~hairer/software.html
    
    Details about the implementation (FORTRAN) can be found in the book,::
    
        Solving Ordinary Differential Equations II,
        Stiff and Differential-Algebraic Problems
        
        Authors: E. Hairer and G. Wanner
        Springer-Verlag, ISBN: 3-540-60452-9
    
    """

    def __init__(self, problem):
        """
        Initiates the solver.
        
            Parameters::
            
                problem     
                            - The problem to be solved. Should be an instance
                              of the 'Explicit_Problem' class.
        """
        Implicit_ODE.__init__(self, problem)
        self.options['inith'] = 0.01
        self.options['newt'] = 7
        self.options['thet'] = 0.001
        self.options['fnewt'] = 0.0
        self.options['quot1'] = 1.0
        self.options['quot2'] = 1.2
        self.options['fac1'] = 0.2
        self.options['fac2'] = 8.0
        self.options['maxh'] = N.inf
        self.options['safe'] = 0.9
        self.options['atol'] = 1e-06 * N.ones(self.problem_info['dim'])
        self.options['rtol'] = 1e-06
        self.options['usejac'] = True if self.problem_info['jac_fcn'] else False
        self.options['maxsteps'] = 100000
        self.supports['report_continuously'] = True
        self.supports['interpolated_output'] = True
        self.supports['state_events'] = True
        self._leny = len(self.y)
        self._type = '(implicit)'
        self._event_info = None
        return

    def initialize(self):
        self.statistics.reset()

    def set_problem_data(self):
        if self.problem_info['state_events']:
            if self.problem_info['type'] == 1:

                def event_func(t, y, yd):
                    return self.problem.state_events(t, y, yd, self.sw)

            else:

                def event_func(t, y, yd):
                    return self.problem.state_events(t, y, self.sw)

            def f(t, y):
                leny = self._leny
                ret = 0
                res = self.problem.res(t, y[:leny], y[leny:2 * leny], self.sw)
                return (N.append(y[leny:2 * leny], res), [ret])

            self._f = f
            self.event_func = event_func
            self._event_info = [0] * self.problem_info['dimRoot']
            self.g_old = self.event_func(self.t, self.y, self.yd)
        else:

            def f(t, y):
                leny = self._leny
                ret = 0
                res = self.problem.res(t, y[:leny], y[leny:2 * leny])
                return (N.append(y[leny:2 * leny], res), [ret])

            self._f = f

    def interpolate(self, time, k=0):
        y = N.empty(self._leny * 2)
        for i in range(self._leny * 2):
            y[i] = radau5.contr5(i + 1, time, self.cont)

        if k == 0:
            return y[:self._leny]
        if k == 1:
            return y[self._leny:2 * self._leny]

    def _solout(self, nrsol, told, t, y, cont, lrc, irtrn):
        """
        This method is called after every successful step taken by Radau5
        """
        self.cont = cont
        yd = y[self._leny:2 * self._leny].copy()
        y = y[:self._leny].copy()
        if self.problem_info['state_events']:
            flag, t, y, yd = self.event_locator(told, t, y, yd)
            if flag == ID_PY_EVENT:
                irtrn = -1
        if self._opts['report_continuously']:
            initialize_flag = self.report_solution(t, y, yd, self._opts)
            if initialize_flag:
                irtrn = -1
        else:
            if self._opts['output_list'] is None:
                self._tlist.append(t)
                self._ylist.append(y)
                self._ydlist.append(yd)
            else:
                output_list = self._opts['output_list']
                output_index = self._opts['output_index']
                try:
                    while output_list[output_index] <= t:
                        self._tlist.append(output_list[output_index])
                        self._ylist.append(self.interpolate(output_list[output_index]))
                        self._ydlist.append(self.interpolate(output_list[output_index], 1))
                        output_index += 1

                except IndexError:
                    pass

            self._opts['output_index'] = output_index
            if self.problem_info['state_events'] and flag == ID_PY_EVENT and len(self._tlist) > 0 and self._tlist[(-1)] != t:
                self._tlist.append(t)
                self._ylist.append(y)
                self._ydlist.append(yd)
        return irtrn

    def _mas_f(self, am):
        return self._mass_matrix

    def integrate(self, t, y, yd, tf, opts):
        if self.usejac:
            self.usejac = False
            self.log_message('Jacobians are not currently supported, disabling.', NORMAL)
        ITOL = 1
        IJAC = 1 if self.usejac else 0
        MLJAC = self.problem_info['dim'] * 2
        MUJAC = 0
        IMAS = 1
        MLMAS = 0
        MUMAS = 0
        IOUT = 1
        WORK = N.array([0.0] * (5 * ((self.problem_info['dim'] * 2) ** 2 + 12) + 20))
        IWORK = N.array([0] * (3 * (self.problem_info['dim'] * 2) + 20))
        WORK[1] = self.safe
        WORK[2] = self.thet
        WORK[3] = self.fnewt
        WORK[4] = self.quot1
        WORK[5] = self.quot2
        WORK[6] = self.maxh
        WORK[7] = self.fac1
        WORK[8] = self.fac2
        IWORK[1] = self.maxsteps
        IWORK[2] = self.newt
        IWORK[4] = self._leny
        IWORK[5] = self._leny
        IWORK[8] = self._leny
        IWORK[9] = self._leny
        mas_dummy = lambda t: x
        jac_dummy = (lambda t: x) if not self.usejac else self.problem.jac
        if opts['initialize']:
            self.set_problem_data()
            self._tlist = []
            self._ylist = []
            self._ydlist = []
        self._opts = opts
        y = N.append(y, yd)
        self._mass_matrix = N.array([[0] * self._leny])
        atol = N.append(self.atol, self.atol)
        t, y, h, iwork, flag = radau5.radau5(self._f, t, y.copy(), tf, self.inith, self.rtol * N.ones(self.problem_info['dim'] * 2), atol, ITOL, jac_dummy, IJAC, MLJAC, MUJAC, self._mas_f, IMAS, MLMAS, MUMAS, self._solout, IOUT, WORK, IWORK)
        if flag == 1:
            flag = ID_PY_COMPLETE
        elif flag == 2:
            flag = ID_PY_EVENT
        else:
            raise Radau5Error(flag, t)
        self.statistics['nsteps'] += iwork[16]
        self.statistics['nfcns'] += iwork[13]
        self.statistics['njacs'] += iwork[14]
        self.statistics['nfcnjacs'] += (self.usejac or iwork[14]) * self.problem_info['dim'] if 1 else 0
        self.statistics['nerrfails'] += iwork[17]
        self.statistics['nlus'] += iwork[18]
        return (
         flag, self._tlist, self._ylist, self._ydlist)

    def state_event_info(self):
        return self._event_info

    def set_event_info(self, event_info):
        self._event_info = event_info

    def print_statistics(self, verbose=NORMAL):
        """
        Prints the run-time statistics for the problem.
        """
        Implicit_ODE.print_statistics(self, verbose)
        self.log_message('\nSolver options:\n', verbose)
        self.log_message(' Solver                  : Radau5 ' + self._type, verbose)
        self.log_message(' Tolerances (absolute)   : ' + str(self._compact_atol()), verbose)
        self.log_message(' Tolerances (relative)   : ' + str(self.options['rtol']), verbose)
        self.log_message('', verbose)


class _Radau5DAE(Radau_Common, Implicit_ODE):
    """
    Radau IIA fifth-order three-stages with step-size control and continuous output.
    Based on the FORTRAN code by E.Hairer and G.Wanner, which can be found here: 
    http://www.unige.ch/~hairer/software.html
    
    Details about the implementation (FORTRAN) can be found in the book,::
    
        Solving Ordinary Differential Equations II,
        Stiff and Differential-Algebraic Problems
        
        Authors: E. Hairer and G. Wanner
        Springer-Verlag, ISBN: 3-540-60452-9
    
    This code is aimed at providing a Python implementation of the original code.
    """

    def __init__(self, problem):
        """
        Initiates the solver.
        
            Parameters::
            
                problem     
                            - The problem to be solved. Should be an instance
                              of the 'Implicit_Problem' class.
        """
        Implicit_ODE.__init__(self, problem)
        self._leny = len(self.y)
        self._2leny = 2 * self._leny
        self.options['inith'] = 0.01
        self.options['newt'] = 7
        self.options['thet'] = 0.001
        self.options['fnewt'] = 0
        self.options['quot1'] = 1.0
        self.options['quot2'] = 1.2
        self.options['fac1'] = 0.2
        self.options['fac2'] = 8.0
        self.options['maxh'] = N.inf
        self.options['safe'] = 0.9
        self.options['atol'] = N.array([1e-06] * self._leny)
        self.options['rtol'] = 1e-06
        self.options['index'] = N.array([1] * self._leny + [2] * self._leny)
        self.options['usejac'] = True if self.problem_info['jac_fcn'] else False
        self.options['maxsteps'] = 10000
        self._curjac = False
        self._itfail = False
        self._needjac = True
        self._needLU = True
        self._first = True
        self._rejected = True
        self._oldh = 0.0
        self._olderr = 1.0
        self._eps = N.finfo('double').eps
        self._col_poly = N.zeros(self._2leny * 3)
        self._type = '(implicit)'
        self._curiter = 0
        self.f = problem.res_internal
        self.RES = N.array([0.0] * len(self.y0))
        self.Y1 = N.array([0.0] * len(self.y0))
        self.Y2 = N.array([0.0] * len(self.y0))
        self.Y3 = N.array([0.0] * len(self.y0))
        self._f0 = N.array([0.0] * len(self.y0))
        self.supports['one_step_mode'] = True
        self.supports['interpolated_output'] = True
        self._load_parameters()

    def _set_index(self, index):
        """
        Sets the index of the variables in the problem which in turn
        determine the error estimations.
        
            Parameters::
            
                    index - A list of integers, indicating the index
                            (1,2,3) of the variable.
                            
                            Example:
                                Radau5.index = [2,1]
                            
        """
        if len(index) == self._2leny:
            ind = N.array(index)
        elif len(index) == self._leny:
            ind = N.array(index + (N.array(index) + 1).tolist())
        else:
            raise Implicit_ODE_Exception('Wrong number of variables in the index vector.')
        self.options['index'] = ind

    def _get_index(self):
        """
        Sets the index of the variables in the problem which in turn
        determine the error estimations.
        
            Parameters::
            
                    index - A list of integers, indicating the index
                            (1,2,3) of the variable.
                            
                            Example:
                                Radau5.index = [2,1]
                            
        """
        return self.options['index']

    index = property(_get_index, _set_index)

    def initialize(self):
        self.statistics.reset()

    def step_generator(self, t, y, yd, tf, opts):
        if opts['initialize']:
            self._oldh = self.inith
            self.h = self.inith
            self._fac_con = 1.0
        if self.fnewt == 0:
            self.fnewt = max(10.0 * self._eps / self.rtol, min(0.03, self.rtol ** 0.5))
        self._f0 = self._ode_f(t, N.append(y, yd))
        self.statistics['nfcns'] += 1
        self._tc = t
        self._yc = y
        self._ydc = yd
        for i in range(self.maxsteps):
            if t < tf:
                t, y, yd = self._step(t, y, yd)
                self._tc = t
                self._yc = y
                self._ydc = yd
                if self.h > N.abs(tf - t):
                    self.h = N.abs(tf - t)
                if t < tf:
                    yield (
                     ID_PY_OK, t, y, yd)
                else:
                    yield (
                     ID_PY_COMPLETE, t, y, yd)
                    break
                self._first = False
        else:
            raise Implicit_ODE_Exception('Final time not reached within maximum number of steps')

    def step(self, t, y, yd, tf, opts):
        if opts['initialize']:
            self._next_step = self.step_generator(t, y, yd, tf, opts)
        return next(self._next_step)

    def integrate(self, t, y, yd, tf, opts):
        if opts['output_list'] is not None:
            output_list = opts['output_list']
            output_index = opts['output_index']
            next_step = self.step_generator(t, y, yd, tf, opts)
            tlist, ylist, ydlist = [], [], []
            res = [
             ID_PY_OK]
            while res[0] != ID_PY_COMPLETE:
                res = next(next_step)
                try:
                    while output_list[output_index] <= res[1]:
                        tlist.append(output_list[output_index])
                        ylist.append(self.interpolate(output_list[output_index]))
                        ydlist.append(self.interpolate(output_list[output_index], k=1))
                        output_index = output_index + 1

                except IndexError:
                    pass

            return (res[0], tlist, ylist, ydlist)
        else:
            flags, tlist, ylist, ydlist = list(zip(*list(self.step_generator(t, y, yd, tf, opts))))
            return (
             flags[(-1)], tlist, ylist, ydlist)
            return

    def _ode_f(self, t, y):
        self.f(self.RES, t, y[:self._leny], y[self._leny:])
        return N.hstack((y[self._leny:], self.RES))

    def _radau_F(self, Z, t, y, yd):
        Z1 = Z[:self._2leny]
        Z2 = Z[self._2leny:2 * self._2leny]
        Z3 = Z[2 * self._2leny:3 * self._2leny]
        q = N.append(y, yd)
        sol1 = self._ode_f(t + self.C[0] * self.h, q + Z1)
        sol2 = self._ode_f(t + self.C[1] * self.h, q + Z2)
        sol3 = self._ode_f(t + self.C[2] * self.h, q + Z3)
        self.statistics['nfcns'] += 3
        return N.hstack((N.hstack((sol1, sol2)), sol3))

    def _step(self, t, y, yd):
        """
        This calculates the next step in the integration.
        """
        self._scaling = N.array(abs(N.append(y, yd)) * self.rtol + self.atol.tolist() * 2)
        while True:
            self.newton(t, y, yd)
            self._err = self.estimate_error()
            if self._err > 1.0:
                self._rejected = True
                self.statistics['nerrfails'] += 1
                ho = self.h
                self.h = self.adjust_stepsize(self._err)
                self.log_message('Rejecting step at ' + str(t) + 'with old stepsize' + str(ho) + 'and new ' + str(self.h) + '. Error: ' + str(self._err), SCREAM)
                if self._curjac or self._curiter == 1:
                    self._needjac = False
                    self._needLU = True
                else:
                    self._needjac = True
                    self._needLU = True
            else:
                self.log_message('Accepting step at ' + str(t) + ' with stepsize ' + str(self.h) + '. Error: ' + str(self._err), SCREAM)
                self.statistics['nsteps'] += 1
                tn = t + self.h
                yn = y + self._Z[2 * self._2leny:3 * self._2leny][:self._leny]
                ydn = yd + self._Z[2 * self._2leny:3 * self._2leny][self._leny:]
                self._f0 = self._ode_f(t, N.append(yn, ydn))
                self.statistics['nfcns'] += 1
                self._oldoldh = self._oldh
                self._oldh = self.h
                self._oldt = t
                self._newt = tn
                ht = self.adjust_stepsize(self._err, predict=True)
                self.h = min(self.h, ht) if self._rejected else ht
                self._rejected = False
                self._curjac = False
                if self._oldoldh == self.h and (self._theta <= self.thet or self._curiter == 1):
                    self._needjac = False
                    self._needLU = False
                elif self._theta <= self.thet or self._curiter == 1:
                    self._needjac = False
                    self._needLU = True
                else:
                    self._needjac = True
                    self._needLU = True
                if self.thet < 0:
                    self._needjac = True
                    self._needLU = True
                self._olderr = max(self._err, 0.01)
                break

        self._col_poly = self._collocation_pol(self._Z, self._col_poly, self._2leny)
        return (
         tn, yn, ydn)

    def newton(self, t, y, yd):
        """
        The newton iteration. 
        """
        for k in range(20):
            self._curiter = 0
            self._fac_con = max(self._fac_con, self._eps) ** 0.8
            self._theta = abs(self.thet)
            if self._needjac:
                self._jac = self.jacobian(t, y, yd)
            if self._needLU:
                self.statistics['nlus'] += 1
                self._a = self._alpha / self.h
                self._b = self._beta / self.h
                self._g = self._gamma / self.h
                self._B = self._g * self.M - self._jac
                self._P1, self._L1, self._U1 = S.linalg.lu(self._B)
                self._P2, self._L2, self._U2 = S.linalg.lu(self._a * self.M - self._jac)
                self._P3, self._L3, self._U3 = S.linalg.lu(self._b * self.M - self._jac)
                self._needLU = False
                if min(abs(N.diag(self._U1))) < self._eps:
                    raise Implicit_ODE_Exception('Error, gM-J is singular at ', self._tc)
            Z, W = self.calc_start_values()
            for i in range(self.newt):
                self._curiter += 1
                self.statistics['nniters'] += 1
                Z = N.dot(self.T2, self._radau_F(Z.real, t, y, yd))
                Z[:(self._2leny)] = Z[:self._2leny] - self._g * N.dot(self.M, W[:self._2leny])
                Z[(self._2leny):(2 * self._2leny)] = Z[self._2leny:2 * self._2leny] - self._a * N.dot(self.M, W[self._2leny:2 * self._2leny])
                Z[(2 * self._2leny):(3 * self._2leny)] = Z[2 * self._2leny:3 * self._2leny] - self._b * N.dot(self.M, W[2 * self._2leny:3 * self._2leny])
                Z[:(self._2leny)] = N.linalg.solve(self._U1, N.linalg.solve(self._L1, N.linalg.solve(self._P1, Z[:self._2leny])))
                Z[(self._2leny):(2 * self._2leny)] = N.linalg.solve(self._U2, N.linalg.solve(self._L2, N.linalg.solve(self._P2, Z[self._2leny:2 * self._2leny])))
                Z[(2 * self._2leny):(3 * self._2leny)] = N.linalg.solve(self._U3, N.linalg.solve(self._L3, N.linalg.solve(self._P3, Z[2 * self._2leny:3 * self._2leny])))
                self._scaling = self._scaling / self.h ** (self.index - 1)
                newnrm = N.linalg.norm(Z.reshape(-1, self._2leny) / self._scaling, 'fro') / N.sqrt(3.0 * self._2leny)
                if i > 0:
                    thq = newnrm / oldnrm
                    if i == 1:
                        self._theta = thq
                    else:
                        self._theta = N.sqrt(thq * thqold)
                    thqold = thq
                    if self._theta < 0.99:
                        self._fac_con = self._theta / (1.0 - self._theta)
                        dyth = self._fac_con * newnrm * self._theta ** (self.newt - (i + 1) - 1) / self.fnewt
                        if dyth >= 1.0:
                            qnewt = max(0.0001, min(20.0, dyth))
                            self._hhfac = 0.8 * qnewt ** (-1.0 / (4.0 + self.newt - (i + 1) - 1))
                            self.h = self._hhfac * self.h
                            self._itfail = True
                            self._rejected = True
                            break
                    else:
                        self._itfail = True
                        break
                oldnrm = max(newnrm, self._eps)
                W = W + Z
                Z = N.dot(self.T3, W)
                if self._fac_con * newnrm <= self.fnewt:
                    self._itfail = False
                    break
            else:
                self._itfail = True

            if not self._itfail:
                self._Z = Z.real
                break
            else:
                self.log_message('Iteration failed at time %e with step-size %e' % (t, self.h), SCREAM)
                self.statistics['nnfails'] += 1
                self._rejected = True
                if self._theta >= 0.99:
                    self._hhfac = 0.5
                    self.h = self.h * self._hhfac
                if self._curjac:
                    self._needjac = False
                    self._needLU = True
                else:
                    self._needjac = True
                    self._needLU = True
        else:
            raise Implicit_ODE_Exception('Newton iteration failed at time %e with step-size %e' % (t, self.h))

    def estimate_error(self):
        temp = 1.0 / self.h * (self.E[0] * self._Z[:self._2leny] + self.E[1] * self._Z[self._2leny:2 * self._2leny] + self.E[2] * self._Z[2 * self._2leny:3 * self._2leny])
        temp = N.dot(self.M, temp)
        self._scaling = self._scaling / self.h ** (self.index - 1)
        scal = self._scaling
        err_v = N.linalg.solve(self._U1, N.linalg.solve(self._L1, N.linalg.solve(self._P1, self._f0 + temp)))
        err = N.linalg.norm(err_v / scal)
        err = max(err / N.sqrt(self._2leny), 1e-10)
        if (self._rejected or self._first) and err >= 1.0:
            self.statistics['nfcns'] += 1
            err_v = self._ode_f(self._tc, N.append(self._yc, self._ydc) + err_v)
            err_v = N.linalg.solve(self._U1, N.linalg.solve(self._L1, N.linalg.solve(self._P1, err_v + temp)))
            err = N.linalg.norm(err_v / scal)
            err = max(err / N.sqrt(self._2leny), 1e-10)
        return err

    def interpolate(self, t, k=0):
        """
        Calculates the continuous output from Radau5.
        """
        leny = self._2leny
        s = (t - self._newt) / self._oldh
        Z = self._col_poly
        diff = s * (Z[:leny] + (s - self.C[(1, 0)] + 1.0) * (Z[leny:2 * leny] + (s - self.C[(0,
                                                                                             0)] + 1.0) * Z[2 * leny:3 * leny]))
        yout = self._yc + diff[:self._leny]
        ydout = self._ydc + diff[self._leny:]
        if k == 0:
            return yout
        if k == 1:
            return ydout
        raise Implicit_ODE_Exception('Unknown value of k. Should be either 0 or 1')

    def jacobian(self, t, y, yd):
        """
        Calculates the Jacobian, either by an approximation or by the user
        defined (jac specified in the problem class).
        """
        self._curjac = True
        self._needLU = True
        self._needjac = False
        q = N.append(y, yd)
        if self.usejac:
            cjac = self.problem.jac(t, y, yd)
        else:
            delt = N.array([ (self._eps * max(abs(yi), 1e-05)) ** 0.5 for yi in q ]) * N.identity(self._2leny)
            Fdelt = N.array([ self._ode_f(t, q + e) for e in delt ])
            grad = ((Fdelt - self._ode_f(t, q)).T / delt.diagonal()).T
            cjac = N.array(grad).T
            self.statistics['nfcnjacs'] += 1 + self._2leny
        self.statistics['njacs'] += 1
        return cjac

    def adjust_stepsize(self, err, predict=False):
        fac = min(self.safe, self.safe * (2.0 * self.newt + 1.0) / (2.0 * self.newt + self._curiter))
        quot = max(1.0 / self.fac2, min(1.0 / self.fac1, err ** 0.25 / fac))
        hnormal = self.h / quot
        if predict:
            if not self._first:
                facgus = self._hacc / self.h * (err ** 2 / self._olderr) ** 0.25 / self.safe
                facgus = max(1.0 / self.fac2, min(1.0 / self.fac1, facgus))
                quot = max(quot, facgus)
                h = self.h / quot
            else:
                h = hnormal
            self._hacc = self.h
        else:
            h = hnormal
        qt = h / self.h
        if qt >= self.quot1 and qt <= self.quot2:
            h = self.h
        if h > self.maxh:
            h = self.maxh
        if self._first and err >= 1.0:
            self._hhfac = 0.1
            h = self.h * self._hhfac
        else:
            self._hhfac = h / self.h
        if h < self._eps:
            raise Implicit_ODE_Exception('Step-size to small at %e with h = %e' % (self._tc, self.h))
        return h

    def _collocation_pol(self, Z, col_poly, leny):
        col_poly[(2 * leny):(3 * leny)] = Z[:leny] / self.C[(0, 0)]
        col_poly[leny:(2 * leny)] = (Z[:leny] - Z[leny:2 * leny]) / (self.C[(0, 0)] - self.C[(1,
                                                                                              0)])
        col_poly[:leny] = (Z[leny:2 * leny] - Z[2 * leny:3 * leny]) / (self.C[(1, 0)] - 1.0)
        col_poly[(2 * leny):(3 * leny)] = (col_poly[leny:2 * leny] - col_poly[2 * leny:3 * leny]) / self.C[(1,
                                                                                                            0)]
        col_poly[leny:(2 * leny)] = (col_poly[leny:2 * leny] - col_poly[:leny]) / (self.C[(0,
                                                                                           0)] - 1.0)
        col_poly[(2 * leny):(3 * leny)] = col_poly[leny:2 * leny] - col_poly[2 * leny:3 * leny]
        return col_poly

    def calc_start_values(self):
        """
        Calculate newton starting values.
        """
        if self._first:
            Z = N.zeros(self._2leny * 3)
            W = N.zeros(self._2leny * 3)
        else:
            Z = self._Z
            cq = self.C * self.h / self._oldh
            newtval = self._col_poly
            leny = self._2leny
            Z[:leny] = cq[(0, 0)] * (newtval[:leny] + (cq[(0, 0)] - self.C[(1, 0)] + 1.0) * (newtval[leny:2 * leny] + (cq[(0,
                                                                                                                           0)] - self.C[(0,
                                                                                                                                         0)] + 1.0) * newtval[2 * leny:3 * leny]))
            Z[leny:(2 * leny)] = cq[(1, 0)] * (newtval[:leny] + (cq[(1, 0)] - self.C[(1,
                                                                                      0)] + 1.0) * (newtval[leny:2 * leny] + (cq[(1,
                                                                                                                                  0)] - self.C[(0,
                                                                                                                                                0)] + 1.0) * newtval[2 * leny:3 * leny]))
            Z[(2 * leny):(3 * leny)] = cq[(2, 0)] * (newtval[:leny] + (cq[(2, 0)] - self.C[(1,
                                                                                            0)] + 1.0) * (newtval[leny:2 * leny] + (cq[(2,
                                                                                                                                        0)] - self.C[(0,
                                                                                                                                                      0)] + 1.0) * newtval[2 * leny:3 * leny]))
            W = N.dot(self.T2, Z)
        return (Z, W)

    def _load_parameters(self):
        A = N.zeros([3, 3])
        A[(0, 0)] = (88.0 - 7.0 * N.sqrt(6.0)) / 360.0
        A[(0, 1)] = (296.0 - 169.0 * N.sqrt(6.0)) / 1800.0
        A[(0, 2)] = (-2.0 + 3.0 * N.sqrt(6.0)) / 225.0
        A[(1, 0)] = (296.0 + 169.0 * N.sqrt(6.0)) / 1800.0
        A[(1, 1)] = (88.0 + 7.0 * N.sqrt(6.0)) / 360.0
        A[(1, 2)] = (-2.0 - 3.0 * N.sqrt(6.0)) / 225.0
        A[(2, 0)] = (16.0 - N.sqrt(6.0)) / 36.0
        A[(2, 1)] = (16.0 + N.sqrt(6.0)) / 36.0
        A[(2, 2)] = 1.0 / 9.0
        C = N.zeros([3, 1])
        C[(0, 0)] = (4.0 - N.sqrt(6.0)) / 10.0
        C[(1, 0)] = (4.0 + N.sqrt(6.0)) / 10.0
        C[(2, 0)] = 1.0
        B = N.zeros([1, 3])
        B[(0, 0)] = (16.0 - N.sqrt(6.0)) / 36.0
        B[(0, 1)] = (16.0 + N.sqrt(6.0)) / 36.0
        B[(0, 2)] = 1.0 / 9.0
        E = N.zeros(3)
        E[0] = -13.0 - 7.0 * N.sqrt(6.0)
        E[1] = -13.0 + 7.0 * N.sqrt(6.0)
        E[2] = -1.0
        E = 1.0 / 3.0 * E
        M = N.array([[1.0, 0.0], [0.0, 0.0]])
        Ainv = N.linalg.inv(A)
        eig, T = N.linalg.eig(Ainv)
        eig = N.array([eig[2], eig[0], eig[1]])
        J = N.diag(eig)
        self._alpha = eig[1]
        self._beta = eig[2]
        self._gamma = eig[0].real
        temp0 = T[:, 0].copy()
        temp1 = T[:, 1].copy()
        temp2 = T[:, 2].copy()
        T[:, 0] = temp2
        T[:, 1] = temp0
        T[:, 2] = temp1
        Tinv = N.linalg.inv(T)
        I = N.eye(self._2leny)
        M = N.kron(M, N.eye(self._leny))
        I3 = N.eye(3)
        T1 = N.kron(J, M)
        T2 = N.kron(Tinv, I)
        T3 = N.kron(T, I)
        self.A = A
        self.B = B
        self.C = C
        self.I = I
        self.E = E
        self.M = M
        self.T1 = T1
        self.T2 = T2
        self.T3 = T3
        self.I3 = I3
        self.EIG = eig