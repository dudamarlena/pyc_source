# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\tikon\Clima\PyKrige\uk.py
# Compiled at: 2017-01-05 16:18:42
# Size of source mod 2**32: 52768 bytes
__doc__ = 'Code by Benjamin S. Murphy\nbscott.murphy@gmail.com\n\nDependencies:\n    numpy\n    scipy\n    matplotlib\n\nClasses:\n    UniversalKriging: Provides greater control over 2D kriging by\n        utilizing drift terms.\n\nReferences:\n    P.K. Kitanidis, Introduction to Geostatistcs: Applications in Hydrogeology,\n    (Cambridge University Press, 1997) 272 p.\n\nCopyright (c) 2015 Benjamin S. Murphy\n'
import Clima.PyKrige.core as core, matplotlib.pyplot as plt, numpy as np, scipy.linalg
from scipy.spatial.distance import cdist
import tikon.Clima.PyKrige.variogram_models as variogram_models

class UniversalKriging:
    """UniversalKriging"""
    UNBIAS = True
    eps = 1e-10
    variogram_dict = {'linear':variogram_models.linear_variogram_model,  'power':variogram_models.power_variogram_model, 
     'gaussian':variogram_models.gaussian_variogram_model, 
     'spherical':variogram_models.spherical_variogram_model, 
     'exponential':variogram_models.exponential_variogram_model}

    def __init__(self, x, y, z, variogram_model='linear', variogram_parameters=None, variogram_function=None, nlags=6, weight=False, anisotropy_scaling=1.0, anisotropy_angle=0.0, drift_terms=None, point_drift=None, external_drift=None, external_drift_x=None, external_drift_y=None, specified_drift=None, functional_drift=None, verbose=False, enable_plotting=False):
        if drift_terms is None:
            drift_terms = []
        else:
            if specified_drift is None:
                specified_drift = []
            else:
                if functional_drift is None:
                    functional_drift = []
                else:
                    self.X_ORIG = np.atleast_1d(np.squeeze(np.array(x, copy=True)))
                    self.Y_ORIG = np.atleast_1d(np.squeeze(np.array(y, copy=True)))
                    self.Z = np.atleast_1d(np.squeeze(np.array(z, copy=True)))
                    self.verbose = verbose
                    self.enable_plotting = enable_plotting
                    if self.enable_plotting:
                        if self.verbose:
                            print('Plotting Enabled\n')
                    self.XCENTER = (np.amax(self.X_ORIG) + np.amin(self.X_ORIG)) / 2.0
                    self.YCENTER = (np.amax(self.Y_ORIG) + np.amin(self.Y_ORIG)) / 2.0
                    self.anisotropy_scaling = anisotropy_scaling
                    self.anisotropy_angle = anisotropy_angle
                    if self.verbose:
                        print('Adjusting data for anisotropy...')
                    self.X_ADJUSTED, self.Y_ADJUSTED = core.adjust_for_anisotropy(np.copy(self.X_ORIG), np.copy(self.Y_ORIG), self.XCENTER, self.YCENTER, self.anisotropy_scaling, self.anisotropy_angle)
                    self.variogram_model = variogram_model
                    if self.variogram_model not in self.variogram_dict.keys():
                        if self.variogram_model != 'custom':
                            raise ValueError("Specified variogram model '%s' is not supported." % variogram_model)
                    if self.variogram_model == 'custom':
                        if variogram_function is None or not callable(variogram_function):
                            raise ValueError('Must specify callable function for custom variogram model.')
                        else:
                            self.variogram_function = variogram_function
                    else:
                        self.variogram_function = self.variogram_dict[self.variogram_model]
                    if self.verbose:
                        print('Initializing variogram model...')
                    self.lags, self.semivariance, self.variogram_model_parameters = core.initialize_variogram_model(self.X_ADJUSTED, self.Y_ADJUSTED, self.Z, self.variogram_model, variogram_parameters, self.variogram_function, nlags, weight)
                    if self.verbose:
                        if self.variogram_model == 'linear':
                            print("Using '%s' Variogram Model" % 'linear')
                            print('Slope:', self.variogram_model_parameters[0])
                            print('Nugget:', self.variogram_model_parameters[1], '\n')
                        else:
                            if self.variogram_model == 'power':
                                print("Using '%s' Variogram Model" % 'power')
                                print('Scale:', self.variogram_model_parameters[0])
                                print('Exponent:', self.variogram_model_parameters[1])
                                print('Nugget:', self.variogram_model_parameters[2], '\n')
                            else:
                                if self.variogram_model == 'custom':
                                    print('Using Custom Variogram Model')
                                else:
                                    print("Using '%s' Variogram Model" % self.variogram_model)
                                    print('Sill:', self.variogram_model_parameters[0])
                                    print('Range:', self.variogram_model_parameters[1])
                                    print('Nugget:', self.variogram_model_parameters[2])
                                if self.enable_plotting:
                                    self.display_variogram_model()
                                if self.verbose:
                                    print('Calculating statistics on variogram model fit...')
                                self.delta, self.sigma, self.epsilon = core.find_statistics(self.X_ADJUSTED, self.Y_ADJUSTED, self.Z, self.variogram_function, self.variogram_model_parameters)
                                self.Q1 = core.calcQ1(self.epsilon)
                                self.Q2 = core.calcQ2(self.epsilon)
                                self.cR = core.calc_cR(self.Q2, self.sigma)
                                if self.verbose:
                                    print('Q1 =', self.Q1)
                                    print('Q2 =', self.Q2)
                                    print('cR =', self.cR, '\n')
                                if self.verbose:
                                    print('Initializing drift terms...')
                                if 'regional_linear' in drift_terms:
                                    self.regional_linear_drift = True
                                    if self.verbose:
                                        print('Implementing regional linear drift.')
                                else:
                                    self.regional_linear_drift = False
                            if 'external_Z' in drift_terms:
                                if external_drift is None:
                                    raise ValueError('Must specify external Z drift terms.')
                                if external_drift_x is None or external_drift_y is None:
                                    raise ValueError('Must specify coordinates of external Z drift terms.')
                                self.external_Z_drift = True
                                if external_drift.shape[0] != external_drift_y.shape[0] or external_drift.shape[1] != external_drift_x.shape[0]:
                                    if external_drift.shape[0] == external_drift_x.shape[0] and external_drift.shape[1] == external_drift_y.shape[0]:
                                        self.external_Z_drift = np.array(external_drift.T)
                                else:
                                    raise ValueError('External drift dimensions do not match provided x- and y-coordinate dimensions.')
                            else:
                                self.external_Z_array = np.array(external_drift)
                        self.external_Z_array_x = np.array(external_drift_x).flatten()
                        self.external_Z_array_y = np.array(external_drift_y).flatten()
                        self.z_scalars = self._calculate_data_point_zscalars(self.X_ORIG, self.Y_ORIG)
                        if self.verbose:
                            print('Implementing external Z drift.')
                    else:
                        self.external_Z_drift = False
                    if 'point_log' in drift_terms:
                        if point_drift is None:
                            raise ValueError('Must specify location(s) and strength(s) of point drift terms.')
                        self.point_log_drift = True
                        point_log = np.atleast_2d(np.squeeze(np.array(point_drift, copy=True)))
                        self.point_log_array = np.zeros(point_log.shape)
                        self.point_log_array[:, 2] = point_log[:, 2]
                        x_adj, y_adj = core.adjust_for_anisotropy(point_log[:, 0], point_log[:, 1], self.XCENTER, self.YCENTER, self.anisotropy_scaling, self.anisotropy_angle)
                        self.point_log_array[:, 0] = x_adj
                        self.point_log_array[:, 1] = y_adj
                        if self.verbose:
                            print('Implementing external point-logarithmic drift; number of points =', self.point_log_array.shape[0], '\n')
                    else:
                        self.point_log_drift = False
                if 'specified' in drift_terms:
                    if type(specified_drift) is not list:
                        raise TypeError('Arrays for specified drift terms must be encapsulated in a list.')
                    if len(specified_drift) == 0:
                        raise ValueError("Must provide at least one drift-value array when using the 'specified' drift capability.")
                    self.specified_drift = True
                    self.specified_drift_data_arrays = []
                    for term in specified_drift:
                        specified = np.squeeze(np.array(term, copy=True))
                        if specified.size != self.X_ORIG.size:
                            raise ValueError("Must specify the drift values for each data point when using the 'specified' drift capability.")
                        self.specified_drift_data_arrays.append(specified)

                else:
                    self.specified_drift = False
            if 'functional' in drift_terms:
                if type(functional_drift) is not list:
                    raise TypeError('Callables for functional drift terms must be encapsulated in a list.')
                if len(functional_drift) == 0:
                    raise ValueError("Must provide at least one callable object when using the 'functional' drift capability.")
                self.functional_drift = True
                self.functional_drift_terms = functional_drift
            else:
                self.functional_drift = False

    def _calculate_data_point_zscalars(self, x, y, type_='array'):
        """Determines the Z-scalar values at the specified coordinates
        for use when setting up the kriging matrix. Uses bilinear
        interpolation.
        Currently, the Z scalar values are extracted from the input Z grid
        exactly at the specified coordinates. This means that if the Z grid
        resolution is finer than the resolution of the desired kriged grid,
        there is no averaging of the scalar values to return an average
        Z value for that cell in the kriged grid. Rather, the exact Z value
        right at the coordinate is used."""
        if type_ == 'scalar':
            nx = 1
            ny = 1
            z_scalars = None
        else:
            if x.ndim == 1:
                nx = x.shape[0]
                ny = 1
            else:
                ny = x.shape[0]
                nx = x.shape[1]
            z_scalars = np.zeros(x.shape)
        for m in range(ny):
            for n in range(nx):
                if type_ == 'scalar':
                    xn = x
                    yn = y
                else:
                    if x.ndim == 1:
                        xn = x[n]
                        yn = y[n]
                    else:
                        xn = x[(m, n)]
                        yn = y[(m, n)]
                    if xn > np.amax(self.external_Z_array_x) or xn < np.amin(self.external_Z_array_x) or yn > np.amax(self.external_Z_array_y) or yn < np.amin(self.external_Z_array_y):
                        raise ValueError('External drift array does not cover specified kriging domain.')
                    external_x2_index = np.amin(np.where(self.external_Z_array_x >= xn)[0])
                    external_x1_index = np.amax(np.where(self.external_Z_array_x <= xn)[0])
                    external_y2_index = np.amin(np.where(self.external_Z_array_y >= yn)[0])
                    external_y1_index = np.amax(np.where(self.external_Z_array_y <= yn)[0])
                    if external_y1_index == external_y2_index:
                        if external_x1_index == external_x2_index:
                            z = self.external_Z_array[(external_y1_index, external_x1_index)]
                        else:
                            z = (self.external_Z_array[(external_y1_index, external_x1_index)] * (self.external_Z_array_x[external_x2_index] - xn) + self.external_Z_array[(external_y2_index, external_x2_index)] * (xn - self.external_Z_array_x[external_x1_index])) / (self.external_Z_array_x[external_x2_index] - self.external_Z_array_x[external_x1_index])
                    else:
                        if external_x1_index == external_x2_index:
                            if external_y1_index == external_y2_index:
                                z = self.external_Z_array[(external_y1_index, external_x1_index)]
                            else:
                                z = (self.external_Z_array[(external_y1_index, external_x1_index)] * (self.external_Z_array_y[external_y2_index] - yn) + self.external_Z_array[(external_y2_index, external_x2_index)] * (yn - self.external_Z_array_y[external_y1_index])) / (self.external_Z_array_y[external_y2_index] - self.external_Z_array_y[external_y1_index])
                        else:
                            z = (self.external_Z_array[(external_y1_index, external_x1_index)] * (self.external_Z_array_x[external_x2_index] - xn) * (self.external_Z_array_y[external_y2_index] - yn) + self.external_Z_array[(external_y1_index, external_x2_index)] * (xn - self.external_Z_array_x[external_x1_index]) * (self.external_Z_array_y[external_y2_index] - yn) + self.external_Z_array[(external_y2_index, external_x1_index)] * (self.external_Z_array_x[external_x2_index] - xn) * (yn - self.external_Z_array_y[external_y1_index]) + self.external_Z_array[(external_y2_index, external_x2_index)] * (xn - self.external_Z_array_x[external_x1_index]) * (yn - self.external_Z_array_y[external_y1_index])) / ((self.external_Z_array_x[external_x2_index] - self.external_Z_array_x[external_x1_index]) * (self.external_Z_array_y[external_y2_index] - self.external_Z_array_y[external_y1_index]))
                if type_ == 'scalar':
                    z_scalars = z
                else:
                    if z_scalars.ndim == 1:
                        z_scalars[n] = z
                    else:
                        z_scalars[(m, n)] = z

        return z_scalars

    def update_variogram_model(self, variogram_model, variogram_parameters=None, variogram_function=None, nlags=6, weight=False, anisotropy_scaling=1.0, anisotropy_angle=0.0):
        """Allows user to update variogram type and/or variogram model parameters."""
        if anisotropy_scaling != self.anisotropy_scaling or anisotropy_angle != self.anisotropy_angle:
            if self.verbose:
                print('Adjusting data for anisotropy...')
            self.anisotropy_scaling = anisotropy_scaling
            self.anisotropy_angle = anisotropy_angle
            self.X_ADJUSTED, self.Y_ADJUSTED = core.adjust_for_anisotropy(np.copy(self.X_ORIG), np.copy(self.Y_ORIG), self.XCENTER, self.YCENTER, self.anisotropy_scaling, self.anisotropy_angle)
        else:
            self.variogram_model = variogram_model
            if self.variogram_model not in self.variogram_dict.keys():
                if self.variogram_model != 'custom':
                    raise ValueError("Specified variogram model '%s' is not supported." % variogram_model)
            if self.variogram_model == 'custom':
                if variogram_function is None or not callable(variogram_function):
                    raise ValueError('Must specify callable function for custom variogram model.')
                else:
                    self.variogram_function = variogram_function
            else:
                self.variogram_function = self.variogram_dict[self.variogram_model]
            if self.verbose:
                print('Updating variogram mode...')
            self.lags, self.semivariance, self.variogram_model_parameters = core.initialize_variogram_model(self.X_ADJUSTED, self.Y_ADJUSTED, self.Z, self.variogram_model, variogram_parameters, self.variogram_function, nlags, weight)
            if self.verbose:
                if self.variogram_model == 'linear':
                    print("Using '%s' Variogram Model" % 'linear')
                    print('Slope:', self.variogram_model_parameters[0])
                    print('Nugget:', self.variogram_model_parameters[1], '\n')
                else:
                    if self.variogram_model == 'power':
                        print("Using '%s' Variogram Model" % 'power')
                        print('Scale:', self.variogram_model_parameters[0])
                        print('Exponent:', self.variogram_model_parameters[1])
                        print('Nugget:', self.variogram_model_parameters[2], '\n')
                    else:
                        if self.variogram_model == 'custom':
                            print('Using Custom Variogram Model')
                        else:
                            print("Using '%s' Variogram Model" % self.variogram_model)
                            print('Sill:', self.variogram_model_parameters[0])
                            print('Range:', self.variogram_model_parameters[1])
                            print('Nugget:', self.variogram_model_parameters[2])
            if self.enable_plotting:
                self.display_variogram_model()
            if self.verbose:
                print('Calculating statistics on variogram model fit...')
            self.delta, self.sigma, self.epsilon = core.find_statistics(self.X_ADJUSTED, self.Y_ADJUSTED, self.Z, self.variogram_function, self.variogram_model_parameters)
            self.Q1 = core.calcQ1(self.epsilon)
            self.Q2 = core.calcQ2(self.epsilon)
            self.cR = core.calc_cR(self.Q2, self.sigma)
            if self.verbose:
                print('Q1 =', self.Q1)
                print('Q2 =', self.Q2)
                print('cR =', self.cR, '\n')

    def display_variogram_model(self):
        """Displays variogram model with the actual binned data"""
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.lags, self.semivariance, 'r*')
        ax.plot(self.lags, self.variogram_function(self.variogram_model_parameters, self.lags), 'k-')
        plt.show()

    def switch_verbose(self):
        """Allows user to switch code talk-back on/off. Takes no arguments."""
        self.verbose = not self.verbose

    def switch_plotting(self):
        """Allows user to switch plot display on/off. Takes no arguments."""
        self.enable_plotting = not self.enable_plotting

    def get_epsilon_residuals(self):
        """Returns the epsilon residuals for the variogram fit."""
        return self.epsilon

    def plot_epsilon_residuals(self):
        """Plots the epsilon residuals for the variogram fit."""
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter((range(self.epsilon.size)), (self.epsilon), c='k', marker='*')
        ax.axhline(y=0.0)
        plt.show()

    def get_statistics(self):
        return (
         self.Q1, self.Q2, self.cR)

    def print_statistics(self):
        print('Q1 =', self.Q1)
        print('Q2 =', self.Q2)
        print('cR =', self.cR)

    def _get_kriging_matrix(self, n, n_withdrifts):
        """Assembles the kriging matrix."""
        xy = np.concatenate((self.X_ADJUSTED[:, np.newaxis], self.Y_ADJUSTED[:, np.newaxis]), axis=1)
        d = cdist(xy, xy, 'euclidean')
        if self.UNBIAS:
            a = np.zeros((n_withdrifts + 1, n_withdrifts + 1))
        else:
            a = np.zeros((n_withdrifts, n_withdrifts))
        a[:n, :n] = -self.variogram_function(self.variogram_model_parameters, d)
        np.fill_diagonal(a, 0.0)
        i = n
        if self.regional_linear_drift:
            a[:n, i] = self.X_ADJUSTED
            a[i, :n] = self.X_ADJUSTED
            i += 1
            a[:n, i] = self.Y_ADJUSTED
            a[i, :n] = self.Y_ADJUSTED
            i += 1
        if self.point_log_drift:
            for well_no in range(self.point_log_array.shape[0]):
                log_dist = np.log(np.sqrt((self.X_ADJUSTED - self.point_log_array[(well_no, 0)]) ** 2 + (self.Y_ADJUSTED - self.point_log_array[(well_no, 1)]) ** 2))
                if np.any(np.isinf(log_dist)):
                    log_dist[np.isinf(log_dist)] = -100.0
                a[:n, i] = -self.point_log_array[(well_no, 2)] * log_dist
                a[i, :n] = -self.point_log_array[(well_no, 2)] * log_dist
                i += 1

        if self.external_Z_drift:
            a[:n, i] = self.z_scalars
            a[i, :n] = self.z_scalars
            i += 1
        if self.specified_drift:
            for arr in self.specified_drift_data_arrays:
                a[:n, i] = arr
                a[i, :n] = arr
                i += 1

        if self.functional_drift:
            for func in self.functional_drift_terms:
                a[:n, i] = func(self.X_ADJUSTED, self.Y_ADJUSTED)
                a[i, :n] = func(self.X_ADJUSTED, self.Y_ADJUSTED)
                i += 1

        if i != n_withdrifts:
            print('WARNING: Error in creating kriging matrix. Kriging may fail.')
        if self.UNBIAS:
            a[n_withdrifts, :n] = 1.0
            a[:n, n_withdrifts] = 1.0
            a[n:n_withdrifts + 1, n:n_withdrifts + 1] = 0.0
        return a

    def _exec_vector(self, a, bd, xy, xy_orig, mask, n_withdrifts, spec_drift_grids):
        """Solves the kriging system as a vectorized operation. This method
        can take a lot of memory for large grids and/or large datasets."""
        npt = bd.shape[0]
        n = self.X_ADJUSTED.shape[0]
        zero_index = None
        zero_value = False
        a_inv = scipy.linalg.inv(a)
        if np.any(np.absolute(bd) <= self.eps):
            zero_value = True
            zero_index = np.where(np.absolute(bd) <= self.eps)
        else:
            if self.UNBIAS:
                b = np.zeros((npt, n_withdrifts + 1, 1))
            else:
                b = np.zeros((npt, n_withdrifts, 1))
            b[:, :n, 0] = -self.variogram_function(self.variogram_model_parameters, bd)
            if zero_value:
                b[(zero_index[0], zero_index[1], 0)] = 0.0
            i = n
            if self.regional_linear_drift:
                b[:, i, 0] = xy[:, 0]
                i += 1
                b[:, i, 0] = xy[:, 1]
                i += 1
            if self.point_log_drift:
                for well_no in range(self.point_log_array.shape[0]):
                    log_dist = np.log(np.sqrt((xy[:, 0] - self.point_log_array[(well_no, 0)]) ** 2 + (xy[:, 1] - self.point_log_array[(well_no, 1)]) ** 2))
                    if np.any(np.isinf(log_dist)):
                        log_dist[np.isinf(log_dist)] = -100.0
                    b[:, i, 0] = -self.point_log_array[(well_no, 2)] * log_dist
                    i += 1

            if self.external_Z_drift:
                b[:, i, 0] = self._calculate_data_point_zscalars(xy_orig[:, 0], xy_orig[:, 1])
                i += 1
            if self.specified_drift:
                for spec_vals in spec_drift_grids:
                    b[:, i, 0] = spec_vals.flatten()
                    i += 1

            if self.functional_drift:
                for func in self.functional_drift_terms:
                    b[:, i, 0] = func(xy[:, 0], xy[:, 1])
                    i += 1

            if i != n_withdrifts:
                print('WARNING: Error in setting up kriging system. Kriging may fail.')
            if self.UNBIAS:
                b[:, n_withdrifts, 0] = 1.0
            if (~mask).any():
                mask_b = np.repeat((mask[:, np.newaxis, np.newaxis]), (n_withdrifts + 1), axis=1)
                b = np.ma.array(b, mask=mask_b)
            if self.UNBIAS:
                x = np.dot(a_inv, b.reshape((npt, n_withdrifts + 1)).T).reshape((1, n_withdrifts + 1, npt)).T
            else:
                x = np.dot(a_inv, b.reshape((npt, n_withdrifts)).T).reshape((1, n_withdrifts, npt)).T
        zvalues = np.sum((x[:, :n, 0] * self.Z), axis=1)
        sigmasq = np.sum((x[:, :, 0] * -b[:, :, 0]), axis=1)
        return (
         zvalues, sigmasq)

    def _exec_loop(self, a, bd_all, xy, xy_orig, mask, n_withdrifts, spec_drift_grids):
        """Solves the kriging system by looping over all specified points.
        Less memory-intensive, but involves a Python-level loop."""
        npt = bd_all.shape[0]
        n = self.X_ADJUSTED.shape[0]
        zvalues = np.zeros(npt)
        sigmasq = np.zeros(npt)
        a_inv = scipy.linalg.inv(a)
        for j in np.nonzero(~mask)[0]:
            bd = bd_all[j]
            if np.any(np.absolute(bd) <= self.eps):
                zero_value = True
                zero_index = np.where(np.absolute(bd) <= self.eps)
            else:
                zero_index = None
                zero_value = False
            if self.UNBIAS:
                b = np.zeros((n_withdrifts + 1, 1))
            else:
                b = np.zeros((n_withdrifts, 1))
            b[:n, 0] = -self.variogram_function(self.variogram_model_parameters, bd)
            if zero_value:
                b[(zero_index[0], 0)] = 0.0
            i = n
            if self.regional_linear_drift:
                b[(i, 0)] = xy[(j, 0)]
                i += 1
                b[(i, 0)] = xy[(j, 1)]
                i += 1
            if self.point_log_drift:
                for well_no in range(self.point_log_array.shape[0]):
                    log_dist = np.log(np.sqrt((xy[(j, 0)] - self.point_log_array[(well_no, 0)]) ** 2 + (xy[(j, 1)] - self.point_log_array[(well_no, 1)]) ** 2))
                    if np.any(np.isinf(log_dist)):
                        log_dist[np.isinf(log_dist)] = -100.0
                    b[(i, 0)] = -self.point_log_array[(well_no, 2)] * log_dist
                    i += 1

            if self.external_Z_drift:
                b[(i, 0)] = self._calculate_data_point_zscalars((xy_orig[(j, 0)]), (xy_orig[(j, 1)]), type_='scalar')
                i += 1
            if self.specified_drift:
                for spec_vals in spec_drift_grids:
                    b[(i, 0)] = spec_vals.flatten()[i]
                    i += 1

            if self.functional_drift:
                for func in self.functional_drift_terms:
                    b[(i, 0)] = func(xy[(j, 0)], xy[(j, 1)])
                    i += 1

            if i != n_withdrifts:
                print('WARNING: Error in setting up kriging system. Kriging may fail.')
            if self.UNBIAS:
                b[(n_withdrifts, 0)] = 1.0
            x = np.dot(a_inv, b)
            zvalues[j] = np.sum(x[:n, 0] * self.Z)
            sigmasq[j] = np.sum(x[:, 0] * -b[:, 0])

        return (
         zvalues, sigmasq)

    def execute(self, style, xpoints, ypoints, mask=None, backend='vectorized', specified_drift_arrays=None):
        """Calculates a kriged grid and the associated variance. Includes drift terms.

        This is now the method that performs the main kriging calculation. Note that currently
        measurements (i.e., z values) are considered 'exact'. This means that, when a specified
        coordinate for interpolation is exactly the same as one of the data points, the variogram
        evaluated at the point is forced to be zero. Also, the diagonal of the kriging matrix is
        also always forced to be zero. In forcing the variogram evaluated at data points to be zero,
        we are effectively saying that there is no variance at that point (no uncertainty,
        so the value is 'exact').

        In the future, the code may include an extra 'exact_values' boolean flag that can be
        adjusted to specify whether to treat the measurements as 'exact'. Setting the flag
        to false would indicate that the variogram should not be forced to be zero at zero distance
        (i.e., when evaluated at data points). Instead, the uncertainty in the point will be
        equal to the nugget. This would mean that the diagonal of the kriging matrix would be set to
        the nugget instead of to zero.

        Inputs:
            style (string): Specifies how to treat input kriging points.
                Specifying 'grid' treats xpoints and ypoints as two arrays of
                x and y coordinates that define a rectangular grid.
                Specifying 'points' treats xpoints and ypoints as two arrays
                that provide coordinate pairs at which to solve the kriging system.
                Specifying 'masked' treats xpoints and ypoints as two arrays of
                x and y coordinates that define a rectangular grid and uses mask
                to only evaluate specific points in the grid.
            xpoints (array-like, dim N): If style is specific as 'grid' or 'masked',
                x-coordinates of MxN grid. If style is specified as 'points',
                x-coordinates of specific points at which to solve kriging system.
            ypoints (array-like, dim M): If style is specified as 'grid' or 'masked',
                y-coordinates of MxN grid. If style is specified as 'points',
                y-coordinates of specific points at which to solve kriging system.
                Note that in this case, xpoints and ypoints must have the same dimensions
                (i.e., M = N).
            mask (boolean array, dim MxN, optional): Specifies the points in the rectangular
                grid defined by xpoints and ypoints that are to be excluded in the
                kriging calculations. Must be provided if style is specified as 'masked'.
                False indicates that the point should not be masked, so the kriging system
                will be solved at the point.
                True indicates that the point should be masked, so the kriging system should
                will not be solved at the point.
            backend (string, optional): Specifies which approach to use in kriging.
                Specifying 'vectorized' will solve the entire kriging problem at once in a
                vectorized operation. This approach is faster but also can consume a
                significant amount of memory for large grids and/or large datasets.
                Specifying 'loop' will loop through each point at which the kriging system
                is to be solved. This approach is slower but also less memory-intensive.
                Default is 'vectorized'. Note that Cython backend is not supported for UK.
            specified_drift_arrays (list of array-like objects, optional): Specifies the drift
                values at the points at which the kriging system is to be evaluated. Required if
                'specified' drift provided in the list of drift terms when instantiating the
                UniversalKriging class. Must be a list of arrays in the same order as the list
                provided when instantiating the kriging object. Array(s) must be the same dimension
                as the specified grid or have the same number of points as the specified points;
                i.e., the arrays either must be dim MxN, where M is the number of y grid-points
                and N is the number of x grid-points, or dim M, where M is the number of points
                at which to evaluate the kriging system.
        Outputs:
            zvalues (numpy array, dim MxN or dim Nx1): Z-values of specified grid or at the
                specified set of points. If style was specified as 'masked', zvalues will
                be a numpy masked array.
            sigmasq (numpy array, dim MxN or dim Nx1): Variance at specified grid points or
                at the specified set of points. If style was specified as 'masked', sigmasq
                will be a numpy masked array.
        """
        if self.verbose:
            print('Executing Universal Kriging...\n')
        else:
            if style != 'grid':
                if style != 'masked':
                    if style != 'points':
                        raise ValueError("style argument must be 'grid', 'points', or 'masked'")
                    else:
                        n = self.X_ADJUSTED.shape[0]
                        n_withdrifts = n
                        xpts = np.atleast_1d(np.squeeze(np.array(xpoints, copy=True)))
                        ypts = np.atleast_1d(np.squeeze(np.array(ypoints, copy=True)))
                        nx = xpts.size
                        ny = ypts.size
                        if self.regional_linear_drift:
                            n_withdrifts += 2
                        if self.point_log_drift:
                            n_withdrifts += self.point_log_array.shape[0]
                        if self.external_Z_drift:
                            n_withdrifts += 1
                        if self.specified_drift:
                            n_withdrifts += len(self.specified_drift_data_arrays)
                        if self.functional_drift:
                            n_withdrifts += len(self.functional_drift_terms)
                        a = self._get_kriging_matrix(n, n_withdrifts)
                        if style in ('grid', 'masked'):
                            if style == 'masked':
                                if mask is None:
                                    raise IOError("Must specify boolean masking array when style is 'masked'.")
                                else:
                                    if mask.shape[0] != ny or mask.shape[1] != nx:
                                        if mask.shape[0] == nx and mask.shape[1] == ny:
                                            mask = mask.T
                                        else:
                                            raise ValueError('Mask dimensions do not match specified grid dimensions.')
                                mask = mask.flatten()
                            npt = ny * nx
                            grid_x, grid_y = np.meshgrid(xpts, ypts)
                            xpts = grid_x.flatten()
                            ypts = grid_y.flatten()
                        else:
                            if style == 'points':
                                if xpts.size != ypts.size:
                                    raise ValueError('xpoints and ypoints must have same dimensions when treated as listing discrete points.')
                                npt = nx
                            else:
                                raise ValueError("style argument must be 'grid', 'points', or 'masked'")
                    if specified_drift_arrays is None:
                        specified_drift_arrays = []
                else:
                    spec_drift_grids = []
                    if self.specified_drift:
                        if len(specified_drift_arrays) == 0:
                            raise ValueError("Must provide drift values for kriging points when using 'specified' drift capability.")
                        if type(specified_drift_arrays) is not list:
                            raise TypeError('Arrays for specified drift terms must be encapsulated in a list.')
                        for spec in specified_drift_arrays:
                            if style in ('grid', 'masked'):
                                if spec.ndim < 2:
                                    raise ValueError('Dimensions of drift values array do not match specified grid dimensions.')
                                else:
                                    if spec.shape[0] != ny or spec.shape[1] != nx:
                                        if spec.shape[0] == nx:
                                            if spec.shape[1] == ny:
                                                spec_drift_grids.append(np.squeeze(spec.T))
                                        else:
                                            raise ValueError('Dimensions of drift values array do not match specified grid dimensions.')
                                    else:
                                        spec_drift_grids.append(np.squeeze(spec))
                            else:
                                if style == 'points':
                                    if spec.ndim != 1:
                                        raise ValueError('Dimensions of drift values array do not match specified grid dimensions.')
                                    else:
                                        if spec.shape[0] != xpts.size:
                                            raise ValueError('Number of supplied drift values in array do not match specified number of kriging points.')
                                        else:
                                            spec_drift_grids.append(np.squeeze(spec))

                        if len(spec_drift_grids) != len(self.specified_drift_data_arrays):
                            raise ValueError('Inconsistent number of specified drift terms supplied.')
                    elif len(specified_drift_arrays) != 0:
                        print("WARNING: Provided specified drift values, but 'specified' drift was not initialized during instantiation of UniversalKriging class.")
            else:
                xy_points_original = np.concatenate((xpts[:, np.newaxis], ypts[:, np.newaxis]), axis=1)
                xpts, ypts = core.adjust_for_anisotropy(xpts, ypts, self.XCENTER, self.YCENTER, self.anisotropy_scaling, self.anisotropy_angle)
                xy_points = np.concatenate((xpts[:, np.newaxis], ypts[:, np.newaxis]), axis=1)
                xy_data = np.concatenate((self.X_ADJUSTED[:, np.newaxis], self.Y_ADJUSTED[:, np.newaxis]), axis=1)
                if style != 'masked':
                    mask = np.zeros(npt, dtype='bool')
                bd = cdist(xy_points, xy_data, 'euclidean')
                if backend == 'vectorized':
                    zvalues, sigmasq = self._exec_vector(a, bd, xy_points, xy_points_original, mask, n_withdrifts, spec_drift_grids)
                else:
                    if backend == 'loop':
                        zvalues, sigmasq = self._exec_loop(a, bd, xy_points, xy_points_original, mask, n_withdrifts, spec_drift_grids)
                    else:
                        raise ValueError('Specified backend {} is not supported for 2D universal kriging.'.format(backend))
            if style == 'masked':
                zvalues = np.ma.array(zvalues, mask=mask)
                sigmasq = np.ma.array(sigmasq, mask=mask)
            if style in ('masked', 'grid'):
                zvalues = zvalues.reshape((ny, nx))
                sigmasq = sigmasq.reshape((ny, nx))
        return (zvalues, sigmasq)