# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\GitHub\AeroSandbox\aerosandbox\tools\fitting.py
# Compiled at: 2020-04-23 18:45:12
# Size of source mod 2**32: 5491 bytes
import numpy as np, casadi as cas
from aerosandbox.tools.miscellaneous import stdout_redirected

def fit(model, x_data, y_data, param_guesses, param_bounds=None, weights=None, verbose=True, scale_problem=True):
    """
    Fits a model to data through least-squares minimization.
    :param model: A callable with syntax f(x, p) where:
            x is a dict of dependent variables. Same format as x_data [dict of 1D ndarrays of length n].
            p is a dict of parameters. Same format as param_guesses [dict of scalars].
        Model should use CasADi functions for differentiability.
    :param x_data: a dict of dependent variables. Same format as model's x. [dict of 1D ndarrays of length n]
    :param y_data: independent variable. [1D ndarray of length n]
    :param param_guesses: a dict of fit parameters. Same format as model's p. Keys are parameter names, values are initial guesses. [dict of scalars]
    :param param_bounds: Optional: a dict of bounds on fit parameters.
        Keys are parameter names, values are a tuple of (min, max).
        May contain only a subset of param_guesses if desired.
        Use None to represent one-sided constraints (i.e. (None, 5)).
        [dict of tuples]
    :param weights: Optional: weights for data points. If not supplied, weights are assumed to be uniform.
        Weights are automatically normalized. [1D ndarray of length n]
    :param verbose: Whether or not to print information about parameters and goodness of fit.
    :param scale_problem: Whether or not to attempt to scale variables, constraints, and objective for more robust solve. [boolean]
    :return: Optimal fit parameters [dict]
    """
    opti = cas.Opti()
    if weights is None:
        weights = cas.GenDM_ones(y_data.shape[0])
    else:
        weights /= cas.sum1(weights)

        def fit_param(initial_guess, lower_bound=None, upper_bound=None):
            """
        Helper function to create a fit variable
        :param initial_guess:
        :param lower_bound:
        :param upper_bound:
        :return:
        """
            if scale_problem:
                if np.abs(initial_guess) > 1e-08:
                    var = initial_guess * opti.variable()
                else:
                    var = opti.variable()
                opti.set_initial(var, initial_guess)
                if lower_bound is not None:
                    lower_bound_abs = np.abs(lower_bound)
                    if scale_problem and lower_bound_abs > 1e-08:
                        opti.subject_to(var / lower_bound_abs > lower_bound / lower_bound_abs)
                    else:
                        opti.subject_to(var > lower_bound)
                if upper_bound is not None:
                    upper_bound_abs = np.abs(upper_bound)
                    if scale_problem and upper_bound_abs > 1e-08:
                        opti.subject_to(var / upper_bound_abs < upper_bound / upper_bound_abs)
            else:
                opti.subject_to(var < upper_bound)
            return var

        if param_bounds is None:
            params = {k:fit_param(param_guesses[k]) for k in param_guesses}
        else:
            params = {k:(fit_param(param_guesses[k]) if k not in param_bounds else fit_param(param_guesses[k], param_bounds[k][0], param_bounds[k][1])) for k in param_guesses}
        if scale_problem:
            y_model_initial = model(x_data, param_guesses)
            residuals_initial = y_model_initial - y_data
            SSE_initial = cas.sum1(weights * residuals_initial ** 2)
            y_model = model(x_data, params)
            residuals = y_model - y_data
            SSE = cas.sum1(weights * residuals ** 2)
            opti.minimize(SSE / SSE_initial)
        else:
            y_model = model(x_data, params)
            residuals = y_model - y_data
            SSE = cas.sum1(weights * residuals ** 2)
            opti.minimize(SSE)
        p_opts = {}
        s_opts = {}
        s_opts['max_iter'] = 3000.0
        opti.solver('ipopt', p_opts, s_opts)
        opti.solver('ipopt')
        if verbose:
            sol = opti.solve()
        else:
            with stdout_redirected():
                sol = opti.solve()
    params_solved = {}
    for k in params:
        try:
            params_solved[k] = sol.value(params[k])
        except:
            params_solved[k] = np.NaN

    if verbose:
        print('\nFit Parameters:')
        if len(params_solved) <= 20:
            [print('\t%s: %f' % (k, v)) for k, v in params_solved.items()]
        else:
            print('\t%i parameters solved for.' % len(params_solved))
        print('\nGoodness of Fit:')
        weighted_RMS_error = sol.value(cas.sqrt(cas.sum1(weights * residuals ** 2)))
        print('\tWeighted RMS error: %f' % weighted_RMS_error)
        y_data_mean = cas.sum1(y_data) / y_data.shape[0]
        SS_tot = cas.sum1(weights * (y_data - y_data_mean) ** 2)
        SS_res = cas.sum1(weights * (y_data - y_model) ** 2)
        R_squared = sol.value(1 - SS_res / SS_tot)
        print('\tR^2: %f' % R_squared)
    return params_solved