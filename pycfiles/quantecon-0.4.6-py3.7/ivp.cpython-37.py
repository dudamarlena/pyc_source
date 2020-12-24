# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quantecon/ivp.py
# Compiled at: 2019-11-04 18:33:25
# Size of source mod 2**32: 8993 bytes
r"""
Base class for solving initial value problems (IVPs) of the form:

.. math::

    \frac{dy}{dt} = f(t,y),\ y(t_0) = y_0

using finite difference methods. The `quantecon.ivp` class uses various
integrators from the `scipy.integrate.ode` module to perform the
integration (i.e., solve the ODE) and parametric B-spline interpolation
from `scipy.interpolate` to approximate the value of the solution
between grid points. The `quantecon.ivp` module also provides a method
for computing the residual of the solution which can be used for
assessing the overall accuracy of the approximated solution.

"""
import numpy as np
from scipy import integrate, interpolate

class IVP(integrate.ode):
    __doc__ = '\n    Creates an instance of the IVP class.\n\n    Parameters\n    ----------\n    f : callable ``f(t, y, *f_args)``\n        Right hand side of the system of equations defining the ODE.\n        The independent variable, ``t``, is a ``scalar``; ``y`` is\n        an ``ndarray`` of dependent variables with ``y.shape ==\n        (n,)``. The function `f` should return a ``scalar``,\n        ``ndarray`` or ``list`` (but not a ``tuple``).\n    jac : callable ``jac(t, y, *jac_args)``, optional(default=None)\n        Jacobian of the right hand side of the system of equations\n        defining the ODE.\n\n        .. :math:\n\n            \\mathcal{J}_{i,j} = \\bigg[\\frac{\\partial f_i}{\\partial y_j}\\bigg]\n\n    '

    def __init__(self, f, jac=None):
        super(IVP, self).__init__(f, jac)

    def _integrate_fixed_trajectory(self, h, T, step, relax):
        """Generates a solution trajectory of fixed length."""
        solution = np.hstack((self.t, self.y))
        while self.successful():
            self.integrate(self.t + h, step, relax)
            current_step = np.hstack((self.t, self.y))
            solution = np.vstack((solution, current_step))
            if h > 0 and self.t >= T:
                break
            elif h < 0 and self.t <= T:
                break
            continue

        return solution

    def _integrate_variable_trajectory(self, h, g, tol, step, relax):
        """Generates a solution trajectory of variable length."""
        solution = np.hstack((self.t, self.y))
        while self.successful():
            self.integrate(self.t + h, step, relax)
            current_step = np.hstack((self.t, self.y))
            solution = np.vstack((solution, current_step))
            if g(self.t, self.y, *self.f_params) < tol:
                break
            continue

        return solution

    def _initialize_integrator(self, t0, y0, integrator, **kwargs):
        """Initializes the integrator prior to integration."""
        self.set_initial_value(y0, t0)
        (self.set_integrator)(integrator, **kwargs)

    def compute_residual(self, traj, ti, k=3, ext=2):
        r"""
        The residual is the difference between the derivative of the B-spline
        approximation of the solution trajectory and the right-hand side of the
        original ODE evaluated along the approximated solution trajectory.

        Parameters
        ----------
        traj : array_like (float)
            Solution trajectory providing the data points for constructing the
            B-spline representation.
        ti : array_like (float)
            Array of values for the independent variable at which to
            interpolate the value of the B-spline.
        k : int, optional(default=3)
            Degree of the desired B-spline. Degree must satisfy
            :math:`1 \le k \le 5`.
        ext : int, optional(default=2)
            Controls the value of returned elements for outside the
            original knot sequence provided by traj. For extrapolation, set
            `ext=0`; `ext=1` returns zero; `ext=2` raises a `ValueError`.

        Returns
        -------
        residual : array (float)
            Difference between the derivative of the B-spline approximation
            of the solution trajectory and the right-hand side of the ODE
            evaluated along the approximated solution trajectory.

        """
        soln = self.interpolate(traj, ti, k, 0, ext)
        deriv = self.interpolate(traj, ti, k, 1, ext)
        T = ti.size
        rhs_ode = np.vstack([(self.f)(ti[i], soln[i, 1:], *self.f_params) for i in range(T)])
        rhs_ode = np.hstack((ti[:, np.newaxis], rhs_ode))
        residual = deriv - rhs_ode
        return residual

    def solve(self, t0, y0, h=1.0, T=None, g=None, tol=None, integrator='dopri5', step=False, relax=False, **kwargs):
        """
        Solve the IVP by integrating the ODE given some initial condition.

        Parameters
        ----------
        t0 : float
            Initial condition for the independent variable.
        y0 : array_like (float, shape=(n,))
            Initial condition for the dependent variables.
        h : float, optional(default=1.0)
            Step-size for computing the solution. Can be positive or negative
            depending on the desired direction of integration.
        T : int, optional(default=None)
            Terminal value for the independent variable. One of either `T`
            or `g` must be specified.
        g : callable ``g(t, y, f_args)``, optional(default=None)
            Provides a stopping condition for the integration. If specified
            user must also specify a stopping tolerance, `tol`.
        tol : float, optional (default=None)
            Stopping tolerance for the integration. Only required if `g` is
            also specifed.
        integrator : str, optional(default='dopri5')
            Must be one of 'vode', 'lsoda', 'dopri5', or 'dop853'
        step : bool, optional(default=False)
            Allows access to internal steps for those solvers that use adaptive
            step size routines. Currently only 'vode', 'zvode', and 'lsoda'
            support `step=True`.
        relax : bool, optional(default=False)
            Currently only 'vode', 'zvode', and 'lsoda' support `relax=True`.
        **kwargs : dict, optional(default=None)
            Dictionary of integrator specific keyword arguments. See the
            Notes section of the docstring for `scipy.integrate.ode` for a
            complete description of solver specific keyword arguments.

        Returns
        -------
        solution: ndarray (float)
            Simulated solution trajectory.

        """
        (self._initialize_integrator)(t0, y0, integrator, **kwargs)
        if g is not None and tol is not None:
            soln = self._integrate_variable_trajectory(h, g, tol, step, relax)
        else:
            if T is not None:
                soln = self._integrate_fixed_trajectory(h, T, step, relax)
            else:
                mesg = "Either both 'g' and 'tol', or 'T' must be specified."
                raise ValueError(mesg)
        return soln

    def interpolate(self, traj, ti, k=3, der=0, ext=2):
        r"""
        Parametric B-spline interpolation in N-dimensions.

        Parameters
        ----------
        traj : array_like (float)
            Solution trajectory providing the data points for constructing the
            B-spline representation.
        ti : array_like (float)
            Array of values for the independent variable at which to
            interpolate the value of the B-spline.
        k : int, optional(default=3)
            Degree of the desired B-spline. Degree must satisfy
            :math:`1 \le k \le 5`.
        der : int, optional(default=0)
            The order of derivative of the spline to compute (must be less
            than or equal to `k`).
        ext : int, optional(default=2) Controls the value of returned elements
            for outside the original knot sequence provided by traj. For
            extrapolation, set `ext=0`; `ext=1` returns zero; `ext=2` raises a
            `ValueError`.

        Returns
        -------
        interp_traj: ndarray (float)
            The interpolated trajectory.

        """
        u = traj[:, 0]
        n = traj.shape[1]
        x = [traj[:, i] for i in range(1, n)]
        tck, t = interpolate.splprep(x, u=u, k=k, s=0)
        out = interpolate.splev(ti, tck, der, ext)
        interp_traj = np.hstack((ti[:, np.newaxis], np.array(out).T))
        return interp_traj