# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/assimulo/solvers/odepack.py
# Compiled at: 2018-12-15 05:51:02
import numpy as N, scipy.linalg as Sc, scipy.sparse as sp, sys
from assimulo.exception import *
from assimulo.ode import *
import logging
from assimulo.explicit_ode import Explicit_ODE
try:
    from assimulo.lib.odepack import dlsodar, dcfode, dintdy
    from assimulo.lib.odepack import set_lsod_common, get_lsod_common
except ImportError:
    sys.stderr.write('Could not find ODEPACK functions.\n')

class common_like(object):

    def __call__(self):
        return self.__dict__


def g_dummy(t, y):
    return y


def jac_dummy(t, y):
    return N.zeros((len(y), len(y)))


class LSODAR(Explicit_ODE):
    r"""
        LOSDAR is a multistep method for solving explicit ordinary 
        differential equations on the form,
        
        .. math::
    
            \dot{y} = f(t,y), \quad y(t_0) = y_0.
            
        LSODAR automatically switches between using an ADAMS method
        or an BDF method and is also able to monitor events.
        
        LSODAR is part of ODEPACK, http://www.netlib.org/odepack/opkd-sum
    """

    def __init__(self, problem):
        """
        Initiates the solver.
        
            Parameters::
            
                problem     
                            - The problem to be solved. Should be an instance
                              of the 'Implicit_Problem' class.
        """
        Explicit_ODE.__init__(self, problem)
        self.options['atol'] = 1e-06 * N.ones(self.problem_info['dim'])
        self.options['rtol'] = 1e-06
        self.options['usejac'] = False
        self.options['maxsteps'] = 100000
        self.options['rkstarter'] = 1
        self.options['maxordn'] = 12
        self.options['maxords'] = 5
        self.options['maxh'] = 0.0
        self._leny = len(self.y)
        self._nordsieck_array = []
        self._nordsieck_order = 0
        self._nordsieck_time = 0.0
        self._nordsieck_h = 0.0
        self._update_nordsieck = False
        self.supports['state_events'] = True
        self.supports['report_continuously'] = True
        self.supports['interpolated_output'] = True
        self._RWORK = N.array([0.0] * (22 + self.problem_info['dim'] * max(16, self.problem_info['dim'] + 9) + 3 * self.problem_info['dimRoot']))
        self._IWORK = N.array([0] * (20 + self.problem_info['dim']))

    def initialize(self):
        """
        Initializes the overall simulation process
        (called before _simulate) 
        """
        self.statistics.reset()
        self._rkstarter_active = False

    def interpolate(self, t):
        """
        Helper method to interpolate the solution at time t using the Nordsieck history
        array. Wrapper to ODEPACK's subroutine DINTDY.
        """
        if self._update_nordsieck:
            nordsieck_start_index = 21 + 3 * self.problem_info['dimRoot'] - 1
            hu, nqu, nq, nyh, nqnyh = get_lsod_common()
            self._nordsieck_array = self._RWORK[nordsieck_start_index:nordsieck_start_index + (nq + 1) * nyh].reshape((nyh, -1), order='F')
            self._nyh = nyh
            self._update_nordsieck = False
        dky, iflag = dintdy(t, 0, self._nordsieck_array, self._nyh)
        if iflag != 0 and iflag != -2:
            raise ODEPACK_Exception(('DINTDY returned with iflag={} (see ODEPACK documentation).').format(iflag))
        elif iflag == -2:
            dky = self.y.copy()
        return dky

    def autostart(self, t, y, sw0=[]):
        """
        autostart determines the initial stepsize for Runge--Kutta solvers 
        """
        RWORK = self._RWORK.copy()
        IWORK = self._IWORK.copy()
        pr = self.rkstarter + 1
        tol = self.options['atol']
        tolscale = tol[0] ** (1.0 / pr)
        normscale = 1.0
        f = self.problem.rhs
        t0 = t
        tf = RWORK[0]
        T = abs(tf - t0)
        direction = N.sign(tf - t0)
        cent = Sc.norm(y) / normscale / 100.0
        v0 = y + cent * N.random.rand(len(y), 1)
        u0prime = f(t, y, sw0)
        v0prime = f(t, v0, sw0)
        Lip = Sc.norm(u0prime - v0prime) / Sc.norm(y - v0)
        h = direction * min(0.001 * T, max(1e-08 * T, 0.05 / Lip))
        u1 = y + h * u0prime
        t1 = t + h
        u1prime = f(t1, u1, sw0)
        u0comp = u1 - h * u1prime
        du = u0comp - y
        dunorm = Sc.norm(du)
        errnorm = dunorm / normscale
        u0comprime = f(t0, u0comp, sw0)
        L = Sc.norm(u0comprime - u0prime) / dunorm
        M = N.dot(du, u0comprime - u0prime) / dunorm ** 2
        theta1 = tolscale / N.sqrt(errnorm)
        theta2 = tolscale / abs(h * (L + M / 2))
        h = h * (theta1 + theta2) / 2
        h = direction * min(0.003 * T, abs(h))
        return h

    def integrate_start(self, t, y):
        """
        Helper program for the initialization of LSODAR
        """
        if not (self.rkstarter > 1 and self._rkstarter_active):
            ISTATE = 1
            RWORK = 0.0 * self._RWORK
            IWORK = 0.0 * self._IWORK
        else:
            RWORK = self._RWORK.copy()
            IWORK = self._IWORK.copy()
            ISTATE = 2
            dls001 = common_like()
            dlsr01 = common_like()
            hu, nqu, nq, nyh, nqnyh = get_lsod_common()
            H = 0.01
            rkNordsieck = RKStarterNordsieck(self.problem.rhs, H, number_of_steps=self.rkstarter)
            t, nordsieck = rkNordsieck(t, y, self.sw)
            nordsieck = nordsieck.T
            nordsieck_start_index = 21 + 3 * self.problem_info['dimRoot'] - 1
            RWORK[nordsieck_start_index:(nordsieck_start_index + nordsieck.size)] = nordsieck.flatten(order='F')
            dls001.init = 1
            mf = 20
            nq = self.rkstarter
            dls001.meth = meth = mf // 10
            dls001.miter = mf % 10
            elco, tesco = dcfode(meth)
            dls001.maxord = 5
            dls001.nq = self.rkstarter
            dls001.nqu = self.rkstarter
            dls001.meo = meth
            dls001.nqnyh = nq * self.problem_info['dim']
            dls001.conit = 0.5 / (nq + 2)
            dls001.el = elco[:, nq - 1]
            dls001.hu = H
            dls001.jstart = 1
            IWORK[14] = dls001.nq
            IWORK[19] = meth
            dls001.tn = t
            RWORK[12] = t
            RWORK[10] = hu
            RWORK[11] = H
            number_of_fevals = N.array([1, 2, 4, 7, 11])
            IWORK[9:13] = [
             0] * 4
            dls001.nst = 1
            dls001.nfe = number_of_fevals[(self.rkstarter - 1)]
            dls001.nje = 0
            dlsr01.nge = 0
            commonblocks = {}
            commonblocks.update(dls001())
            commonblocks.update(dlsr01())
            set_lsod_common(**commonblocks)
        return (
         ISTATE, RWORK, IWORK)

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
        ITOL = 2
        ITASK = 5
        IOPT = 1
        ISTATE, RWORK, IWORK = self.integrate_start(t, y)
        JT = 1 if self.usejac else 2
        JROOT = N.array([0] * self.problem_info['dimRoot'])
        RWORK[0] = tf
        RWORK[5] = self.options['maxh']
        IWORK[5] = self.maxsteps
        IWORK[7] = self.maxordn
        IWORK[8] = self.maxords
        g_fcn = g_dummy if not self.problem_info['state_events'] else self.problem.state_events
        jac_fcn = jac_dummy if not self.usejac else self._jacobian
        rhs_extra_args = (self.sw,) if self.problem_info['switches'] else ()
        g_extra_args = (self.sw,) if self.problem_info['switches'] else ()
        self._opts = opts
        tlist = []
        ylist = []
        normal_mode = 1 if opts['output_list'] is not None else 0
        atol = self.atol
        rtol = self.rtol * N.ones(self.problem_info['dim'])
        rhs = self.problem.rhs
        if opts['report_continuously'] or opts['output_list'] is None:
            while (ISTATE == 2 or ISTATE == 1) and t < tf:
                y, t, ISTATE, RWORK, IWORK, roots = dlsodar(rhs, y.copy(), t, tf, ITOL, rtol, atol, ITASK, ISTATE, IOPT, RWORK, IWORK, jac_fcn, JT, g_fcn, JROOT, f_extra_args=rhs_extra_args, g_extra_args=g_extra_args)
                self._update_nordsieck = True
                self._IWORK = IWORK
                self._RWORK = RWORK
                self._event_info = roots
                if opts['report_continuously']:
                    flag_initialize = self.report_solution(t, y, opts)
                    if flag_initialize:
                        ISTATE = 3
                else:
                    tlist.append(t)
                    ylist.append(y.copy())
                if ISTATE == 2:
                    flag = ID_PY_COMPLETE
                elif ISTATE == 3:
                    flag = ID_PY_EVENT
                else:
                    raise ODEPACK_Exception('LSODAR failed with flag %d' % ISTATE)

        else:
            ITASK = 4
            output_index = opts['output_index']
            output_list = opts['output_list'][output_index:]
            flag = ID_PY_COMPLETE
            for tout in output_list:
                output_index += 1
                y, t, ISTATE, RWORK, IWORK, roots = dlsodar(rhs, y.copy(), t, tout, ITOL, rtol, atol, ITASK, ISTATE, IOPT, RWORK, IWORK, jac_fcn, JT, g_fcn, JROOT, f_extra_args=rhs_extra_args, g_extra_args=g_extra_args)
                tlist.append(t)
                ylist.append(y.copy())
                self._event_info = roots
                if ISTATE == 2 and t >= tf:
                    flag = ID_PY_COMPLETE
                    break
                elif ISTATE == 3:
                    flag = ID_PY_EVENT
                    break
                elif ISTATE < 0:
                    raise ODEPACK_Exception('LSODAR failed with flag %d' % ISTATE)

            opts['output_index'] = output_index
        self._rkstarter_active = True if ISTATE == 3 and self.rkstarter > 1 else False
        self.statistics['nstatefcns'] += IWORK[9]
        self.statistics['nsteps'] += IWORK[10]
        self.statistics['nfcns'] += IWORK[11]
        self.statistics['njacs'] += IWORK[12]
        self.statistics['nstateevents'] += 1 if flag == ID_PY_EVENT else 0
        if self.rkstarter > 1:
            self._RWORK = RWORK
            self._IWORK = IWORK
        return (flag, tlist, ylist)

    def get_algorithm_data(self):
        """
        Returns the order and step size used in the last successful step.
        """
        hu, nqu, nq, nyh, nqnyh = get_lsod_common()
        return (
         hu, nqu)

    def state_event_info(self):
        """
        Returns the state events indicator as a list where a one (1)
        indicates that the event function have been activated and a (0)
        if not.
        """
        return self._event_info

    def print_statistics(self, verbose=NORMAL):
        """
        Prints the run-time statistics for the problem.
        """
        Explicit_ODE.print_statistics(self, verbose)
        self.log_message('\nSolver options:\n', verbose)
        self.log_message(' Solver                  : LSODAR ', verbose)
        self.log_message((' Absolute tolerances     : {}').format(self.options['atol']), verbose)
        self.log_message((' Relative tolerances     : {}').format(self.options['rtol']), verbose)
        if self.rkstarter == 1:
            self.log_message((' Starter                 : {}').format('classical'), verbose)
        else:
            self.log_message((' Starter                 : Runge-Kutta order {}').format(self.rkstarter), verbose)
        if self.maxordn < 12 or self.maxords < 5:
            self.log_message((' Maximal order Adams     : {}').format(self.maxordn), verbose)
            self.log_message((' Maximal order BDF       : {}').format(self.maxords), verbose)
        if self.maxh > 0.0:
            self.log_message((' Maximal stepsize maxh   : {}').format(self.maxh), verbose)
        self.log_message('', verbose)

    def _set_usejac(self, jac):
        self.options['usejac'] = bool(jac)

    def _get_usejac(self):
        """
        This sets the option to use the user defined jacobian. If a
        user provided jacobian is implemented into the problem the
        default setting is to use that jacobian. If not, an
        approximation is used.
        
            Parameters::
            
                usejac  
                        - True - use user defined jacobian
                          False - use an approximation
                    
                        - Should be a boolean.
                        
                            Example:
                                usejac = False
        """
        return self.options['usejac']

    usejac = property(_get_usejac, _set_usejac)

    def _set_atol(self, atol):
        self.options['atol'] = N.array(atol, dtype=N.float) if len(N.array(atol, dtype=N.float).shape) > 0 else N.array([atol], dtype=N.float)
        if len(self.options['atol']) == 1:
            self.options['atol'] = self.options['atol'] * N.ones(self._leny)
        elif len(self.options['atol']) != self._leny:
            raise ODEPACK_Exception('atol must be of length one or same as the dimension of the problem.')

    def _get_atol(self):
        """
        Defines the absolute tolerance(s) that is to be used by the solver.
        Can be set differently for each variable.
        
            Parameters::
            
                atol    
                        - Default '1.0e-6'.
                
                        - Should be a positive float or a numpy vector
                          of floats.
                        
                            Example:
                                atol = [1.0e-4, 1.0e-6]
        """
        return self.options['atol']

    atol = property(_get_atol, _set_atol)

    def _set_rtol(self, rtol):
        try:
            self.options['rtol'] = float(rtol)
        except (ValueError, TypeError):
            raise ODEPACK_Exception('Relative tolerance must be a (scalar) float.')

        if self.options['rtol'] <= 0.0:
            raise ODEPACK_Exception('Relative tolerance must be a positive (scalar) float.')

    def _get_rtol(self):
        """
        Defines the relative tolerance that is to be used by the solver.
        
            Parameters::
            
                rtol    
                        - Default '1.0e-6'.
                
                        - Should be a positive float.
                        
                            Example:
                                rtol = 1.0e-4
        """
        return self.options['rtol']

    rtol = property(_get_rtol, _set_rtol)

    def _get_maxsteps(self):
        """
        The maximum number of steps allowed to be taken to reach the
        final time.
        
            Parameters::
            
                maxsteps
                            - Default 10000
                            
                            - Should be a positive integer
        """
        return self.options['maxsteps']

    def _set_maxsteps(self, max_steps):
        try:
            max_steps = int(max_steps)
        except (TypeError, ValueError):
            raise ODEPACK_Exception('Maximum number of steps must be a positive integer.')

        self.options['maxsteps'] = max_steps

    maxsteps = property(_get_maxsteps, _set_maxsteps)

    def _get_hmax(self):
        """
        The absolute value of the maximal stepsize for all methods
        
        Parameters::
        
               hmax
                          - Default:  0.  (no maximal step size)
                          
                          - Should be a positive float
        """
        logging.warning("The option 'hmax' is deprecated and will be removed, please use 'maxh' instead.")
        return self.options['maxh']

    def _set_hmax(self, hmax):
        if not (isinstance(hmax, float) and hmax >= 0.0):
            raise ODEPACK_Exception('Maximal step size hmax should be a positive float')
        logging.warning("The option 'hmax' is deprecated and will be removed, please use 'maxh' instead.")
        self.options['maxh'] = hmax

    hmax = property(_get_hmax, _set_hmax)

    def _get_maxh(self):
        """
        The absolute value of the maximal stepsize for all methods
        
        Parameters::
        
               maxh
                          - Default:  0.  (no maximal step size)
                          
                          - Should be a positive float
        """
        return self.options['maxh']

    def _set_maxh(self, maxh):
        if not (isinstance(maxh, float) and maxh >= 0.0):
            raise ODEPACK_Exception('Maximal step size maxh should be a positive float')
        self.options['maxh'] = maxh

    maxh = property(_get_maxh, _set_maxh)

    def _get_maxordn(self):
        """
        The maximum order used by the Adams-Moulton method (nonstiff case)
        
            Parameters::
            
                maxordn
                            - Default 12
                            
                            - Should be a positive integer
        """
        return self.options['maxordn']

    def _set_maxordn(self, maxordn):
        try:
            maxordn = int(maxordn)
        except (TypeError, ValueError):
            raise ODEPACK_Exception('Maximum order must be a positive integer.')

        if maxordn > 12:
            raise ODEPACK_Exception('Maximum order should not exceed 12.')
        self.options['maxordn'] = maxordn

    maxordn = property(_get_maxordn, _set_maxordn)

    def _get_maxords(self):
        """
        The maximum order used by the BDF method (stiff case)
        
            Parameters::
            
                maxords
                            - Default 5
                            
                            - Should be a positive integer
        """
        return self.options['maxords']

    def _set_maxords(self, maxords):
        try:
            maxords = int(maxords)
        except (TypeError, ValueError):
            raise ODEPACK_Exception('Maximum order must be a positive integer.')

        if maxords > 5:
            raise ODEPACK_Exception('Maximum order should not exceed 5.')
        self.options['maxords'] = maxords

    maxords = property(_get_maxords, _set_maxords)

    def _get_rkstarter(self):
        """
        This defines how LSODAR is started. 
        (classically or with a fourth order Runge-Kutta starter)
        
            Parameters::
            
                rkstarter
                            - Default False  starts LSODAR in the classical multistep way
                            
                            - Should be a Boolean
        """
        return self.options['rkstarter']

    def _set_rkstarter(self, rkstarter):
        if rkstarter not in {1, 2, 3, 4, 5}:
            raise ODEPACK_Exception('Must be a positive integer less than 6')
        self.options['rkstarter'] = rkstarter

    rkstarter = property(_get_rkstarter, _set_rkstarter)


class RKStarterNordsieck(object):
    """
    A family of Runge-Kutta starters producing a 
    Nordsieck array to (re-)start a Nordsieck based multistep
    method with a given order.
    
    See: Mohammadi (2013): https://lup.lub.lu.se/luur/download?func=downloadFile&recordOId=4196026&fileOId=4196027
    """
    Gamma_0 = [
     N.array([[1.0, 0.0],
      [
       0.0, 1.0]]),
     N.array([[1.0, 0.0, 0.0],
      [
       0.0, 1.0, -1.0],
      [
       0.0, 0.0, 1.0]]),
     N.array([[1.0, 0.0, 0.0, 0.0],
      [
       0.0, 1.0, -5.0 / 3.0, 1.0],
      [
       0.0, 0.0, 3.0, -2.0],
      [
       0.0, 0.0, 0.0, 1.0],
      [
       0.0, 0.0, -4.0 / 3.0, 0.0]]),
     N.array([[1.0, 0.0, 0.0, 0.0, 0.0],
      [
       0.0, 1.0, -5.0 / 6.0, 4.0 / 9.0, -1.0 / 9.0],
      [
       0.0, 0.0, 0.0, 0.0, 0.0],
      [
       0.0, 0.0, 1.0 / 2.0, -4.0 / 9.0, 1.0 / 9.0],
      [
       0.0, 0.0, 7.0 / 3.0, -19.0 / 9.0, 7.0 / 9.0],
      [
       0.0, 0.0, -3.0, 10.0 / 3.0, -4.0 / 3.0],
      [
       0.0, 0.0, 1.0, -11.0 / 9.0, 5.0 / 9.0]])]
    A_s = [
     N.array([1]),
     N.array([[0.0, 0], [1, 0]]),
     N.array([[0.0, 0.0, 0.0, 0.0, 0.0], [1.0 / 2, 0.0, 0.0, 0.0, 0.0],
      [
       0.0, 3.0 / 4, 0.0, 0.0, 0.0], [2.0 / 9, 1.0 / 3, 4.0 / 9, 0.0, 0.0],
      [
       17.0 / 72, 1.0 / 6, 2.0 / 9, -1.0 / 8, 0.0]]),
     N.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       1.0 / 6.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       0.0, 1.0 / 6.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       0.0, 0.0, 1.0 / 3.0, 0.0, 0.0, 0.0, 0.0],
      [
       1.0 / 18.0, 1.0 / 9.0, 1.0 / 9.0, 1.0 / 18.0, 0.0, 0.0, 0.0],
      [
       2.5, -3.0, -3.0, 2.25, 2.25, 0.0, 0.0],
      [
       10.0 / 45.0, -8.0 / 45.0, -8.0 / 45.0, -4.0 / 45.0, 13.0 / 15.0, 1.0 / 45.0, 0.0]]),
     N.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       1.0 / 20, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       3.0 / 160, 9.0 / 160, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       3.0 / 40, -9.0 / 40, 6.0 / 20, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       -11.0 / 216, 5 / 8, -70 / 108, 35.0 / 108, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       1631 / 221184, 175.0 / 2048, 575.0 / 55296, 44275.0 / 442368, 253.0 / 16384, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       37.0 / 1512, 0.0, 250 / 2484, 125.0 / 2376, 0.0, 512 / 7084, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       32.2687682, -39.4956646, -20.7849921, 22.2296308, 45.4543383, 51.9961815, -91.1682621, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       -23.867154567764317, 41 + 31195543 / 31462660, 8 + 6080897 / 76520184, -23 - 7543649 / 15003372, -63 - 91662407 / 130833420, -55 - 27823937 / 32947321, 117 + 23615874 / 27978401, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       -0.5118403967750724, 0.0, 2 + 379808 / 6250467, -2 - 866339 / 6430593, -1 - 151963 / 7810968, -18723895 / 33225736, 8 / 3, 0.0, 303385 / 143008499, 0.0, 0.0, 0.0, 0.0, 0.0],
      [
       -118.50992840087292, 4 + 1586290 / 42052551, 7 + 76050433 / 143964928, 11 + 61385198 / 111742353, 16 + 54354964 / 63299173, 15 + 84679766 / 214253769, 15 + 71618817 / 71932238, 24 + 14108046 / 149713813,
       2 + 12784603 / 81260661, 21 + 38484710 / 59808171, 0.0, 0.0, 0.0, 0.0],
      [
       10.183365237189525, 0.0, -36 - 34947657 / 185923229, 38 + 50251318 / 55929787, 18 + 114017528 / 325586295, 10 + 78529445 / 98887874, -43.5, 0.0, -6714159 / 175827524, 2.25, 0.0, 0.0, 0.0, 0.0],
      [
       -0.1491588850008383, 0.0, 19145766 / 113939551, 8434687 / 36458574, 2012005 / 39716421, 8409989 / 57254530, 10739409 / 94504714, 0.0, -3321 / 86525909, -30352753 / 150092385, 0.0, 70257074 / 109630355,
       0.0, 0.0],
      [
       0.03877310906055409, 0.0, 3021245 / 89251943, 5956469 / 58978530, 851373 / 32201684, 11559106 / 149527791, 11325471 / 112382620, 0.0, -12983 / 235976962, 17692261 / 82454251, 0.0,
       38892959 / 120069679, 11804845.0 / 141497517]])]
    co_ord_s = [[], [], [4], [4, 6], [6, 9, 11]]
    b_s = [
     N.array([1]),
     N.array([1.0 / 2, 1.0 / 2]),
     N.array([1.0 / 6, 0.0, 0.0, 1.0 / 6, 2.0 / 3]),
     N.array([29.0 / 1062.0, 83.0 / 531.0, 83.0 / 531.0, 83.0 / 1062.0, 2.0 / 531.0, 56.0 / 531.0, 251.0 / 531.0]),
     N.array([0.03877310906055409, 0.0, 3021245 / 89251943, 5956469 / 58978530, 851373 / 32201684, 11559106 / 149527791, 11325471 / 112382620, 0.0, -12983 / 235976962, 17692261 / 82454251, 0.0,
      38892959 / 120069679, 11804845.0 / 141497517, 0.0])]
    C_s = [
     N.array([0.0]),
     N.array([0.0]),
     N.array([0.0, 1.0 / 2, 3.0 / 4, 1.0, 1.0 / 2, 1.0]),
     N.array([0.0, 1.0 / 6, 1.0 / 6, 1.0 / 3, 1.0 / 3, 1.0, 1.0, 2.0 / 3, 1.0]),
     N.array([0.0, 1.0 / 20, 3.0 / 40, 3.0 / 20, 1.0 / 4, 7.0 / 28, 1.0 / 4, 2.0 / 4, 1.0, 2.0 / 4, 3.0 / 4, 3.0 / 4, 1.0, 1.0])]
    A_n = [
     N.array([1]),
     N.array([[0.0, 0.0], [0.0, 0.0]]),
     N.array([[0.0, 0.0, 0.0, 0.0], [1.0 / 2, 0.0, 0.0, 0.0], [0.0, 1.0 / 2, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]),
     N.array([[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [2.0 / 5, 0.0, 0.0, 0.0, 0.0, 0.0], [-3.0 / 20, 3.0 / 4, 0.0, 0.0, 0.0, 0.0],
      [
       19.0 / 44, -15.0 / 44, 40.0 / 44, 0.0, 0.0, 0.0], [-31.0 / 64, 185.0 / 192, 5.0 / 64, -11.0 / 192, 0.0, 0.0], [11.0 / 72, 25.0 / 72, 25.0 / 72, 11.0 / 72, 0.0, 0.0]])]
    b_n = [
     N.array([0.0]),
     N.array([1.0 / 2.0, 1.0 / 2.0]),
     N.array([[5.0 / 24, 1.0 / 6, 1.0 / 6, -1 / 24], [1.0 / 6, 1.0 / 3, 1.0 / 3, 1.0 / 6]]),
     N.array([[802.0 / 5625, 68.0 / 225, -67.0 / 225, -143.0 / 5625, 144.0 / 625, 6.0 / 125], [699.0 / 5000, 81.0 / 200, -39.0 / 200, 99.0 / 5000, 144.0 / 625, 0.0], [11.0 / 72, 25.0 / 72, 25.0 / 72, 11.0 / 72, 0.0, 0.0]])]
    C_n = [
     N.array([0.0]),
     N.array([0.0]),
     N.array([0.0, 1.0 / 2, 1.0 / 2, 1.0]),
     N.array([0.0, 2.0 / 5, 3.0 / 5, 1.0, 1.0 / 2, 1.0])]
    A = [
     N.array([0.0]),
     N.array([0.0]),
     N.array([1.0]),
     N.array([[1.0 / 4, 1.0 / 8], [1.0, 1.0]]),
     N.array([[1.0 / 9, 1.0 / 27, 1.0 / 81.0],
      [
       4.0 / 9.0, 8.0 / 27, 16.0 / 81],
      [
       1.0, 1.0, 1.0]]),
     N.array([[1.0 / 16, 1.0 / 64, 1.0 / 256, 1.0 / 1024],
      [
       1.0 / 4, 1.0 / 8, 1.0 / 16, 1.0 / 32],
      [
       9.0 / 16, 27.0 / 64, 81.0 / 256, 243.0 / 1024],
      [
       1.0, 1.0, 1.0, 1.0]])]
    scale = N.array([1, 1, 1 / 2.0, 1.0 / 6.0, 1.0 / 24.0, 1.0 / 120.0]).reshape(-1, 1)

    def __init__(self, rhs, H, method='RKs_f', eval_at=0.0, number_of_steps=4):
        """
        Initiates the Runge-Kutta Starter.
        
            Parameters::
                            
                rhs     
                            - The problem's rhs function
                             
                H
                            - starter step size
                            
                eval_at
                            - Where to evaluate the Nordiseck vector
                              evaluation point is (eval_at)*H
                              Possible choices 
                              eval_at=0.
                              eval_at=1.
             
                number_of_steps
                            - the number of steps :math:`(k)` to start the multistep method with
                              This will determine the initial order of the method, which is
                              :math:`k` for BDF methods and :math:`k+1` for Adams Moulton Methods   .
        """
        self.f = rhs
        self.H = H
        self.method = method
        if not 1 < number_of_steps < 6:
            raise RKStarter_Exception('Step number larget than 4 not yet implemented')
        self.number_of_steps = number_of_steps
        self.eval_at = float(eval_at)
        if not self.eval_at == 0.0:
            raise RKStarter_Exception('Parameter eval_at different from 0 not yet implemented.')

    def RKs_f(self, t0, y0, sw0):
        s = self.number_of_steps
        A_s, C_s, b_s, co_ord_s = (self.A_s, self.C_s, self.b_s, self.co_ord_s)
        A_s = A_s[(s - 1)]
        C_s = C_s[(s - 1)]
        b_s = b_s[(s - 1)]
        co_ord_s = co_ord_s[(s - 1)]
        H = (s - 1) * self.H
        K = N.zeros((N.size(A_s, 0), len(y0)))
        for i in range(N.size(A_s, 0)):
            K[i, :] = self.f(t0 + C_s[i] * H, y0 + H * N.dot(A_s[i, :], K), sw0)

        y = N.zeros((s, len(y0)))
        y[0, :] = y0
        for i in range(1, s):
            if i == s - 1:
                y[i, :] = y0 + H * N.dot(b_s, K)
            else:
                y[i, :] = y0 + H * N.dot(A_s[co_ord_s[(i - 1)], :], K)

        return y

    def RKn_f(self, t0, y0, sw0):
        s = self.number_of_steps
        H = (s - 1) * self.H
        A_n, C_n, b_n = self.A_n, self.C_n, self.b_n
        A_n = A_n[(s - 1)]
        C_n = C_n[(s - 1)]
        b_n = b_n[(s - 1)]
        K = N.zeros((N.size(A_n, 0), len(y0)))
        for i in range(N.size(A_n, 0)):
            K[i, :] = self.f(t0 + C_n[i] * H, y0 + H * N.dot(A_n[i, :], K), sw0)

        y = N.zeros((s, len(y0)))
        y[0, :] = y0
        for i in range(1, s):
            y[i, :] = y0 + H * N.dot(b_n[(i - 1)], K)

        return y

    def rk_like4(self, t0, y0, sw0):
        """
        rk_like computes Runge-Kutta stages
        Note, the currently implementation is **only** correct for
        autonomous systems.
        """
        f = lambda y: self.f(t0, y, sw0)
        h = self.H / 4.0
        k1 = h * f(y0)
        k2 = h * f(y0 + k1)
        k3 = h * f(y0 + 2.0 * k2)
        k4 = h * f(y0 + 3.0 / 4.0 * k1 + 9.0 / 4.0 * k3)
        k5 = h * f(y0 + k1 / 2.0 + k2 + k3 / 2.0 + 2.0 * k4)
        k6 = h * f(y0 + k1 / 12.0 + 2.0 * k2 + k3 / 4.0 + 2.0 / 3.0 * k4 + 2.0 * k5)
        return N.array([y0, k1, k2, k3, k4, k5, k6])

    def rk_like3(self, t0, y0, sw0):
        """
        rk_like computes Runge-Kutta stages
        Note, the currently implementation is **only** correct for
        autonomous systems.

        """
        f = lambda y: self.f(t0, y, sw0)
        h = self.H / 3.0
        k1 = h * f(y0)
        k2 = h * f(y0 + k1)
        k3 = h * f(y0 + k1 + k2)
        k4 = h * f(y0 + 3.0 / 2.0 * k1)
        return N.array([y0, k1, k2, k3, k4])

    def rk_like2(self, t0, y0, sw0):
        """
        rk_like2 computes Runge-Kutta 2nd-stages
        Note, the currently implementation is **only** correct for
        autonomous systems.
        """
        f = lambda y: self.f(t0, y, sw0)
        h = self.H / 2.0
        k1 = h * f(y0)
        k2 = h * f(y0 + k1)
        return N.array([y0, k1, k2])

    def rk_like13(self, t0, y0, sw0):
        """
        rk_like6 computes Runge-Kutta 8th-stages 
        """
        h = self.H
        self.Gamma_2 = self.Gamma_0[3]
        f = lambda y: self.f(t0, y, sw0)
        K = N.zeros((6, len(y0)))
        sol = N.zeros((3, len(y0)))
        b = N.zeros((2, len(y0)))
        nord = N.zeros((4, len(y0)))
        for i in range(5):
            K[i, :] = f(y0 + h * N.dot(self.Gamma_2[i, :], K))

        c = 0
        for i in range(3):
            sol[i, :] = y0 + h * N.dot(self.Gamma_2[i + 3, :], K)
            if i != 0:
                b[c, :] = sol[i, :] - y0 - (c + 1) * h / 2 * K[0, :]
                c += 1

        nord[0, :] = y0
        nord[1, :] = h * K[0, :]
        nord[2:, :] = Sc.solve(self.A[self.number_of_steps], b)
        return nord

    def rk_like14(self, t0, y0, sw0):
        """
        rk_like6 computes Runge-Kutta 8th-stages 
        """
        h = self.H
        Gamma_2 = self.Gamma_0[4]
        f = lambda y: self.f(t0, y, sw0)
        K = N.zeros((8, len(y0)))
        sol = N.zeros((4, len(y0)))
        b = N.zeros((3, len(y0)))
        nord = N.zeros((5, len(y0)))
        for i in range(7):
            K[i, :] = f(y0 + h * N.dot(Gamma_2[i, :], K))

        c = 0
        for i in range(4):
            sol[i, :] = y0 + h * N.dot(Gamma_2[i + 4, :], K)
            if i != 1:
                b[c, :] = sol[i, :] - y0 - (c + 1) * h / 3 * K[0, :]
                c += 1

        nord[0, :] = y0
        nord[1, :] = h * K[0, :]
        nord[2:, :] = Sc.solve(self.A[self.number_of_steps], b)
        return nord

    def rk_like15(self, t0, y0, sw0):
        """
        rk_like6 computes Runge-Kutta 5th-stages ****needs to be modified****
        """
        h = self.H
        Gamma_2 = self.Gamma_0[5]
        f = lambda y: self.f(t0, y, sw0)
        K = N.zeros((14, len(y0)))
        sol = N.zeros((8, len(y0)))
        b = N.zeros((4, len(y0)))
        nord = N.zeros((6, len(y0)))
        for i in range(13):
            K[i, :] = f(y0 + h * N.dot(Gamma_2[i, :], K))

        c = 0
        for i in range(8):
            sol[i, :] = y0 + h * N.dot(Gamma_2[i + 6, :], K)
            if i != 1 and i != 2 and i != 4 and i != 6:
                b[c, :] = sol[i, :] - y0 - (c + 1) * h / 4 * K[0, :]
                c += 1

        nord[0, :] = y0
        nord[1, :] = h * K[0, :]
        nord[2:, :] = Sc.solve(self.A[self.number_of_steps], b)
        return nord

    def nordsieck(self, k):
        """
        Nordsieck array computed at initial point
        """
        nord = self.scale[:self.number_of_steps + 1] * N.dot(self.Gamma_0[(self.number_of_steps - 1)].T, k)
        return nord

    def Nordsieck_RKn(self, t0, y, sw0):
        s = self.number_of_steps
        H = (s - 1) * self.H
        co_nord = [N.array([1.0 / 2, 1.0]), N.array([2.0 / 5, 3.0 / 5, 1.0])]
        l = size(y, 0)
        y0 = y[0, :]
        yf = self.f(t0, y0, sw0)
        if l == 3:
            co = N.array([co_nord[0]])
            nord_n = N.vander(co_nord[0], self.number_of_steps + 1)
            b = y[1:] - y0 - co.T * yf
            nord = Sc.solve(nord_n[0:2, 0:2], b)
        elif l == 4:
            co = N.array([co_nord[1]])
            nord_n = N.vander(co_nord[1], self.number_of_steps + 1)
            b = y[1:] - y0 - H * co.T * yf
            nord = Sc.solve(nord_n[0:3, 0:3], b)
        nord = N.vstack((y0, H * yf, nord[::-1]))
        return nord

    def Nordsieck_RKs(self, t0, y, sw0):
        s = self.number_of_steps
        H = (s - 1) * self.H
        co_nord = [N.array([1]), N.array([1.0 / 2, 1]), N.array([1.0 / 3, 2.0 / 3, 1]),
         N.array([1.0 / 4, 2.0 / 4, 3.0 / 4, 1.0])]
        A = self.A
        y0 = y[0, :]
        yf = self.f(t0, y0, sw0)
        co = co_nord[(s - 2)]
        co = N.array([co])
        b = y[1:] - y0 - H * co.T * yf
        nord = Sc.solve(A[s], b)
        nord = N.vstack((y0, H * yf, nord))
        return nord

    def __call__(self, t0, y0, sw0=[]):
        """
        Evaluates the Runge-Kutta starting values
        
            Parameters::
            
                y0   
                    - starting value
        """
        if self.method == 'RK_G':
            k = self.__getattribute__(('rk_like{}').format(self.number_of_steps))(t0, y0, sw0)
            t = t0 + self.eval_at * self.H
            k = self.nordsieck(k)
        elif self.method == 'RKs_f':
            y = self.RKs_f(t0, y0, sw0)
            t = t0 + self.eval_at * self.H
            k = self.Nordsieck_RKs(t0, y, sw0)
        elif self.method == 'RKn_f':
            y = self.RKn_f(t0, y0, sw0)
            t = t0 + self.eval_at * self.H
            k = self.Nordsieck_RKn(t0, y, sw0)
        return (
         t, k)