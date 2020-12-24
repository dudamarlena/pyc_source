# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/suftware_release_0P13_pip_test/suftware/src/DensityEstimator.py
# Compiled at: 2018-04-12 11:58:40
# Size of source mod 2**32: 41634 bytes
import scipy as sp, numpy as np, sys, time, pdb, numbers, pandas as pd
SMALL_NUM = 1e-06
MAX_NUM_GRID_POINTS = 1000
DEFAULT_NUM_GRID_POINTS = 100
MAX_NUM_POSTERIOR_SAMPLES = 1000
MAX_NUM_SAMPLES_FOR_Z = 1000
import suftware.src.deft_core as deft_core, suftware.src.laplacian as laplacian
from suftware.src.utils import ControlledError, enable_graphics, check, handle_errors, clean_numerical_input, LISTLIKE
from suftware.src.DensityEvaluator import DensityEvaluator

class DensityEstimator:
    __doc__ = "Estimates a 1D probability density from sampled data.\n\n    parameters\n    ----------\n    data: (set, list, or np.array of numbers)\n        An array of data from which the probability density will be estimated.\n        Infinite or NaN values will be discarded.\n\n    grid: (1D np.array)\n        An array of evenly spaced grid points on which the probability density\n        will be estimated. Default value is ``None``, in which case the grid is\n        set automatically.\n\n    grid_spacing: (float > 0)\n        The distance at which to space neighboring grid points. Default value\n        is ``None``, in which case this spacing is set automatically.\n\n    num_grid_points: (int)\n        The number of grid points to draw within the data domain. Restricted\n        to ``2*alpha <= num_grid_points <= 1000``. Default value is ``None``, in\n        which case the number of grid points is chosen automatically.\n\n    bounding_box: ([float, float])\n        The boundaries of the data domain, within which the probability density\n        will be estimated. Default value is ``None``, in which case the\n        bounding box is set automatically to encompass all of the data.\n\n    alpha: (int)\n        The order of derivative constrained in the definition of smoothness.\n        Restricted to ``1 <= alpha <= 4``. Default value is 3.\n\n    periodic: (bool)\n        Whether or not to impose periodic boundary conditions on the estimated\n        probability density. Default False, in which case no boundary\n        conditions are imposed.\n\n    num_posterior_samples: (int >= 0)\n        Number of samples to draw from the Bayesian posterior. Restricted to\n        0 <= num_posterior_samples <= MAX_NUM_POSTERIOR_SAMPLES.\n\n    max_t_step: (float > 0)\n        Upper bound on the amount by which the parameter ``t``\n        in the DEFT algorithm is incremented when tracing the MAP curve.\n        Default value is 1.0.\n\n    tollerance: (float > 0)\n        Sets the convergence criterion for the corrector algorithm used in\n        tracing the MAP curve.\n\n    resolution: (float > 0)\n        The maximum geodesic distance allowed for neighboring points\n        on the MAP curve.\n\n    sample_only_at_l_star: (boolean)\n        Specifies whether to let l vary when sampling from the Bayesian\n        posterior.\n\n    max_log_evidence_ratio_drop: (float > 0)\n        If set, MAP curve tracing will terminate prematurely when\n        max_log_evidence - current_log_evidence >  max_log_evidence_ratio_drop.\n\n    evaluation_method_for_Z: (string)\n        Method of evaluation of partition function Z. Possible values:\n        'Lap'      : Laplace approximation (default).\n        'Lap+Imp'  : Laplace approximation + importance sampling.\n        'Lap+Fey'  : Laplace approximation + Feynman diagrams.\n\n    num_samples_for_Z: (int >= 0)\n        Number of posterior samples to use when evaluating the paritation\n        function Z. Only has an affect when\n        ``evaluation_method_for_Z = 'Lap+Imp'``.\n\n    seed: (int)\n        Seed provided to the random number generator before density estimation\n        commences. For development purposes only.\n\n    print_t: (bool)\n        Whether to print the values of ``t`` while tracing the MAP curve.\n        For development purposes only.\n\n    attributes\n    ----------\n    grid:\n        The grid points at which the probability density was be estimated.\n        (1D np.array)\n\n    grid_spacing:\n        The distance between neighboring grid points.\n        (float > 0)\n\n    num_grid_points:\n        The number of grid points used.\n        (int)\n\n    bounding_box:\n        The boundaries of the data domain within which the probability density\n        was be estimated. ([float, float])\n\n    histogram:\n        A histogram of the data using ``grid`` for the centers of each bin.\n        (1D np.array)\n\n    values:\n        The values of the optimal (i.e., MAP) density at each grid point.\n        (1D np.array)\n\n    sample_values:\n        The values of the posterior sampled densities at each grid point.\n        The first index specifies grid points, the second posterior samples.\n        (2D np.array)\n\n    sample_weights:\n        The importance weights corresponding to each posterior sample.\n        (1D np.array)\n\n    "

    @handle_errors
    def __init__(self, data=None, grid=None, grid_spacing=None, num_grid_points=None, bounding_box=None, alpha=3, periodic=False, num_posterior_samples=100, max_t_step=1.0, tolerance=1e-06, resolution=0.1, sample_only_at_l_star=False, max_log_evidence_ratio_drop=20, evaluation_method_for_Z='Lap', num_samples_for_Z=1000, seed=None, print_t=False):
        self.alpha = alpha
        self.grid = grid
        self.grid_spacing = grid_spacing
        self.num_grid_points = num_grid_points
        self.bounding_box = bounding_box
        self.periodic = periodic
        self.Z_evaluation_method = evaluation_method_for_Z
        self.num_samples_for_Z = num_samples_for_Z
        self.max_t_step = max_t_step
        self.print_t = print_t
        self.tolerance = tolerance
        self.seed = seed
        self.resolution = resolution
        self.num_posterior_samples = num_posterior_samples
        self.sample_only_at_l_star = sample_only_at_l_star
        self.max_log_evidence_ratio_drop = max_log_evidence_ratio_drop
        self.data = data
        self.results = None
        self._inputs_check()
        self._clean_data()
        self._set_grid()
        self._run()
        self.histogram = self.results.R
        self.maxent = self.results.M
        self.phi_star_values = self.results.phi_star
        self.density_func = DensityEvaluator(self.phi_star_values, self.grid, self.bounding_box)
        self.values = self.evaluate(self.grid)
        if num_posterior_samples > 0:
            self.sample_field_values = self.results.phi_samples
            self.sample_weights = self.results.phi_weights
            self.sample_density_funcs = [DensityEvaluator(field_values=(self.sample_field_values[:, k]), grid=(self.grid), bounding_box=(self.bounding_box)) for k in range(self.num_posterior_samples)]
            self.sample_values = self.evaluate_samples((self.grid), resample=False)
            self.effective_sample_size = np.sum(self.sample_weights) ** 2 / np.sum(self.sample_weights ** 2)
            self.effective_sampling_efficiency = self.effective_sample_size / self.num_posterior_samples

    @handle_errors
    def plot(self, ax=None, save_as=None, resample=True, figsize=(4, 4), fontsize=12, title='', xlabel='', tight_layout=False, show_now=True, show_map=True, map_color='blue', map_linewidth=2, map_alpha=1, num_posterior_samples=None, posterior_color='dodgerblue', posterior_linewidth=1, posterior_alpha=0.2, show_histogram=True, histogram_color='orange', histogram_alpha=1, show_maxent=False, maxent_color='maroon', maxent_linewidth=1, maxent_alpha=1, backend='TkAgg'):
        """
        Plot the MAP density, the posterior sampled densities, and the
        data histogram.

        parameters
        ----------

        ax: (plt.Axes)
            A matplotlib axes object on which to draw. If None, one will be
            created

        save_as: (str)
            Name of file to save plot to. File type is determined by file
            extension.

        resample: (bool)
            If True, sampled densities will be ploted only after importance
            resampling.

        figsize: ([float, float])
            Figure size as (width, height) in inches.

        fontsize: (float)
            Size of font to use in plot annotation.

        title: (str)
            Plot title.

        xlabel: (str)
            Plot xlabel.

        tight_layout: (bool)
            Whether to call plt.tight_layout() after rendering graphics.

        show_now: (bool)
            Whether to show the plot immediately by calling plt.show().

        show_map: (bool)
            Whether to show the MAP density.

        map_color: (color spec)
            MAP density color.

        map_linewidth: (float)
            MAP density linewidth.

        map_alpha: (float)
            Map density opacity (between 0 and 1).

        num_posterior_samples: (int)
            Number of posterior samples to display. If this is greater than
            the number of posterior samples taken, all of the samples taken
            will be shown.

        posterior_color: (color spec)
            Sampled density color.

        posterior_linewidth: (float)
            Sampled density linewidth.

        posterior_alpha: (float)
            Sampled density opactity (between 0 and 1).

        show_histogram: (bool)
            Whether to show the (normalized) data histogram.

        histogram_color: (color spec)
            Face color of the data histogram.

        histogram_alpha: (float)
            Data histogram opacity (between 0 and 1).

        show_maxent: (bool)
            Whether to show the MaxEnt density estimate.

        maxent_color: (color spect)
            Line color of the MaxEnt density estimate.

        maxent_alpha: (float)
            MaxEnt opacity (between 0 and 1).

        backend: (str)
            Backend specification to send to sw.enable_graphics().

        returns
        -------

            None.

        """
        if 'matplotlib.pyplot' not in sys.modules:
            enable_graphics(backend=backend)
        else:
            import matplotlib.pyplot as plt
            if ax is None:
                fig, ax = plt.subplots(figsize=figsize)
                tight_layout = True
            if show_histogram:
                ax.bar((self.grid), (self.histogram),
                  width=(self.grid_spacing),
                  color=histogram_color,
                  alpha=histogram_alpha)
            if show_maxent:
                ax.plot((self.grid), (self.maxent),
                  color=maxent_color,
                  linewidth=maxent_linewidth,
                  alpha=maxent_alpha)
            if num_posterior_samples is None:
                num_posterior_samples = self.num_posterior_samples
            else:
                if num_posterior_samples > self.num_posterior_samples:
                    num_posterior_samples = self.num_posterior_samples
            if num_posterior_samples > 0:
                sample_values = self.evaluate_samples((self.grid), resample=resample)
                ax.plot((self.grid), (sample_values[:, :num_posterior_samples]),
                  color=posterior_color,
                  linewidth=posterior_linewidth,
                  alpha=posterior_alpha)
            if show_map:
                ax.plot((self.grid), (self.values),
                  color=map_color,
                  linewidth=map_linewidth,
                  alpha=map_alpha)
            ax.set_xlim(self.bounding_box)
            ax.set_title(title, fontsize=fontsize)
            ax.set_xlabel(xlabel, fontsize=fontsize)
            ax.set_yticks([])
            ax.tick_params('x', labelsize=fontsize)
            ax.format_coord = lambda x, y: ''
            if tight_layout:
                plt.tight_layout()
            if save_as is not None:
                plt.draw()
                plt.savefig(save_as)
            if show_now:
                plt.show()

    @handle_errors
    def evaluate(self, x):
        """
        Evaluate the optimal (i.e. MAP) density at the supplied value(s) of x.

        parameters
        ----------

        x: (number or list-like collection of numbers)
            The locations in the data domain at which to evaluate the MAP
            density.

        returns
        -------

        A float or 1D np.array representing the values of the MAP density at
        the specified locations.
        """
        x_arr, is_number = clean_numerical_input(x)
        values = self.density_func.evaluate(x_arr)
        if is_number:
            values = values[0]
        return values

    @handle_errors
    def evaluate_samples(self, x, resample=True):
        """
        Evaluate sampled densities at specified locations.

        parameters
        ----------

        x: (number or list-like collection of numbers)
            The locations in the data domain at which to evaluate sampled
            density.

        resample: (bool)
            Whether to use importance resampling, i.e., should the values
            returned be from the original samples (obtained using a Laplace
            approximated posterior) or should they be resampled to
            account for the deviation between the true Bayesian posterior
            and its Laplace approximation.

        returns
        -------

        A 1D np.array (if x is a number) or a 2D np.array (if x is list-like),
        representing the values of the posterior sampled densities at the
        specified locations. The first index corresponds to values in x, the
        second to sampled densities.
        """
        x_arr, is_number = clean_numerical_input(x)
        check(isinstance(resample, bool), 'type(resample) = %s. Must be bool.' % type(resample))
        check(self.num_posterior_samples > 0, 'Cannot evaluate samples because no posterior sampleshave been computed.')
        assert len(self.sample_density_funcs) == self.num_posterior_samples
        values = np.array([d.evaluate(x_arr) for d in self.sample_density_funcs]).T
        if resample:
            probs = self.sample_weights / self.sample_weights.sum()
            old_cols = np.array(range(self.num_posterior_samples))
            new_cols = np.random.choice(old_cols, size=(self.num_posterior_samples),
              replace=True,
              p=probs)
            values = values[:, new_cols]
        if is_number:
            values = values.ravel()
        return values

    @handle_errors
    def get_stats(self, use_weights=True, show_samples=False):
        """
        Computes summary statistics for the estimated density

        parameters
        ----------

        show_samples: (bool)
            If True, summary stats are computed for each posterior sample.
            If False, summary stats are returned for the "star" estimate,
            the histogram, and the maxent estimate, along with the mean and
            RMSD values of these stats across posterior samples.

        use_weights: (bool)
            If True, mean and RMSD are computed using importance weights.

        returns
        -------

        df: (pd.DataFrame)
            A pandas data frame listing summary statistics for the estimated
            probability densities. These summary statistics include
            "entropy" (in bits), "mean", "variance", "skewness", and
            "kurtosis". If ``show_samples = False``, results will be shown for
            the best estimate, as well as mean and RMDS values across all
            samples. If ``show_samples = True``, results will be shown for
            each sample. A column showing column weights will also be included.
        """
        check(isinstance(use_weights, bool), 'use_weights = %s; must be True or False.' % use_weights)
        check(isinstance(show_samples, bool), 'show_samples = %s; must be True or False.' % show_samples)

        def entropy(Q):
            h = self.grid_spacing
            eps = 1e-10
            assert all(Q >= 0)
            return np.sum(h * Q * np.log2(Q + eps))

        def mean(Q):
            x = self.grid
            h = self.grid_spacing
            return np.sum(h * Q * x)

        def variance(Q):
            mu = mean(Q)
            x = self.grid
            h = self.grid_spacing
            return np.sum(h * Q * (x - mu) ** 2)

        def skewness(Q):
            mu = mean(Q)
            x = self.grid
            h = self.grid_spacing
            return np.sum(h * Q * (x - mu) ** 3) / np.sum(h * Q * (x - mu) ** 2) ** 1.5

        def kurtosis(Q):
            mu = mean(Q)
            x = self.grid
            h = self.grid_spacing
            return np.sum(h * Q * (x - mu) ** 4) / np.sum(h * Q * (x - mu) ** 2) ** 2

        col2func_dict = {'entropy':entropy, 
         'mean':mean, 
         'variance':variance, 
         'skewness':skewness, 
         'kurtosis':kurtosis}
        cols = list(col2func_dict.keys())
        if show_samples:
            cols += ['weight']
        else:
            if show_samples:
                rows = ['sample %d' % n for n in range(self.num_posterior_samples)]
            else:
                rows = [
                 'star', 'histogram', 'maxent',
                 'posterior mean', 'posterior RMSD']
            df = pd.DataFrame(columns=cols, index=rows)
            if use_weights:
                ws = self.sample_weights
            else:
                ws = np.ones(self.num_posterior_samples)
        for col_num, col in enumerate(cols):
            if col == 'weight':
                df.loc[:, col] = ws
            else:
                func = col2func_dict[col]
                ys = np.zeros(self.num_posterior_samples)
                for n in range(self.num_posterior_samples):
                    ys[n] = func(self.sample_values[:, n])

                if show_samples:
                    df.loc[:, col] = ys
                else:
                    df.loc[('star', col)] = func(self.values)
                    df.loc[('histogram', col)] = func(self.histogram)
                    df.loc[('maxent', col)] = func(self.maxent)
                    mu = np.sum(ys * ws) / np.sum(ws)
                    df.loc[('posterior mean', col)] = mu
                    df.loc[('posterior RMSD', col)] = np.sqrt(np.sum(ws * (ys - mu) ** 2) / np.sum(ws))

        return df

    def _run(self):
        """
        Estimates the probability density from data using the DEFT algorithm.
        Also samples posterior densities
        """
        data = self.data
        G = self.num_grid_points
        h = self.grid_spacing
        alpha = self.alpha
        periodic = self.periodic
        Z_eval = self.Z_evaluation_method
        num_Z_samples = self.num_samples_for_Z
        DT_MAX = self.max_t_step
        print_t = self.print_t
        tollerance = self.tolerance
        resolution = self.resolution
        deft_seed = self.seed
        num_pt_samples = self.num_posterior_samples
        fix_t_at_t_star = self.sample_only_at_l_star
        max_log_evidence_ratio_drop = self.max_log_evidence_ratio_drop
        start_time = time.clock()
        if deft_seed is not None:
            np.random.seed(deft_seed)
        else:
            np.random.seed(None)
        laplacian_start_time = time.clock()
        if periodic:
            op_type = '1d_periodic'
        else:
            op_type = '1d_bilateral'
        Delta = laplacian.Laplacian(op_type, alpha, G)
        laplacian_compute_time = time.clock() - laplacian_start_time
        if print_t:
            print('Laplacian computed de novo in %f sec.' % laplacian_compute_time)
        counts, _ = np.histogram(data, self.bin_edges)
        N = sum(counts)
        num_nonempty_bins = sum(counts > 0)
        check(num_nonempty_bins > self.alpha, 'Histogram has %d nonempty bins; must be > %d.' % (
         num_nonempty_bins, self.alpha))
        t_start = min(0.0, sp.log(N) - 2.0 * alpha * sp.log(alpha / h))
        if print_t:
            print('t_start = %0.2f' % t_start)
        core_results = deft_core.run(counts, Delta, Z_eval, num_Z_samples, t_start, DT_MAX, print_t, tollerance, resolution, num_pt_samples, fix_t_at_t_star, max_log_evidence_ratio_drop)
        results = core_results
        results.h = h
        results.L = G * h
        results.R /= h
        results.M /= h
        results.Q_star /= h
        results.l_star = h * (sp.exp(-results.t_star) * N) ** (1 / (2.0 * alpha))
        for p in results.map_curve.points:
            p.Q /= h

        if not num_pt_samples == 0:
            results.Q_samples /= h
        results.Delta = Delta
        self.results = results

    def _inputs_check(self):
        """
        Check all inputs NOT having to do with the choice of grid
        :param self:
        :return: None
        """
        if self.grid_spacing is not None:
            check(isinstance(self.grid_spacing, numbers.Real), 'type(grid_spacing) = %s; must be a number' % type(self.grid_spacing))
            check(self.grid_spacing > 0, 'grid_spacing = %f; must be > 0.' % self.grid_spacing)
        else:
            if self.grid is not None:
                types = (
                 list, np.ndarray, np.matrix)
                check(isinstance(self.grid, types), 'type(grid) = %s; must be a list or np.ndarray' % type(self.grid))
                try:
                    self.grid = np.array(self.grid).ravel().astype(float)
                except:
                    raise ControlledError('Cannot cast grid as 1D np.array of floats.')

                check(2 * self.alpha <= len(self.grid) <= MAX_NUM_GRID_POINTS, 'len(grid) = %d; must have %d <= len(grid) <= %d.' % (
                 len(self.grid), 2 * self.alpha, MAX_NUM_GRID_POINTS))
                diffs = np.diff(self.grid)
                check(all(diffs > 0), 'grid is not monotonically increasing.')
                check(all(np.isclose(diffs, diffs.mean())), 'grid is not evenly spaced; grid spacing = %f +- %f' % (
                 diffs.mean(), diffs.std()))
            else:
                check(isinstance(self.alpha, int), 'type(alpha) = %s; must be int.' % type(self.alpha))
                check(1 <= self.alpha <= 4, 'alpha = %d; must have 1 <= alpha <= 4' % self.alpha)
                if self.num_grid_points is not None:
                    check(isinstance(self.num_grid_points, int), 'type(num_grid_points) = %s; must be int.' % type(self.num_grid_points))
                    check(2 * self.alpha <= self.num_grid_points <= MAX_NUM_GRID_POINTS, 'num_grid_points = %d; must have %d <= num_grid_poitns <= %d.' % (
                     self.num_grid_points, 2 * self.alpha, MAX_NUM_GRID_POINTS))
                if self.bounding_box is not None:
                    box_types = (
                     list, tuple, np.ndarray)
                    check(isinstance(self.bounding_box, box_types), 'type(bounding_box) = %s; must be one of %s' % (
                     type(self.bounding_box), box_types))
                    check(len(self.bounding_box) == 2, 'len(bounding_box) = %d; must be %d' % (
                     len(self.bounding_box), 2))
                    check(isinstance(self.bounding_box[0], numbers.Real) and isinstance(self.bounding_box[1], numbers.Real), 'bounding_box = %s; entries must be numbers' % repr(self.bounding_box))
                    check(self.bounding_box[0] < self.bounding_box[1], 'bounding_box = %s; entries must be sorted' % repr(self.bounding_box))
                    self.bounding_box = (
                     float(self.bounding_box[0]),
                     float(self.bounding_box[1]))
            check(isinstance(self.periodic, bool), 'type(periodic) = %s; must be bool' % type(self.periodic))
            Z_evals = [
             'Lap', 'Lap+Imp', 'Lap+Fey']
            check(self.Z_evaluation_method in Z_evals, 'Z_eval = %s; must be in %s' % (
             self.Z_evaluation_method, Z_evals))
            check(isinstance(self.num_samples_for_Z, numbers.Integral), 'type(self.num_samples_for_Z) = %s; ' % type(self.num_samples_for_Z) + 'must be integer.')
            self.num_samples_for_Z = int(self.num_samples_for_Z)
            check(0 <= self.num_samples_for_Z <= MAX_NUM_SAMPLES_FOR_Z, 'self.num_samples_for_Z = %d; ' % self.num_samples_for_Z + ' must satisfy 0 <= num_samples_for_Z <= %d.' % MAX_NUM_SAMPLES_FOR_Z)
            check(isinstance(self.max_t_step, numbers.Real), 'type(max_t_step) = %s; must be a number' % type(self.max_t_step))
            check(self.max_t_step > 0, 'maxt_t_step = %f; must be > 0.' % self.max_t_step)
            check(isinstance(self.print_t, bool), 'type(print_t) = %s; must be bool.' % type(self.print_t))
            check(isinstance(self.tolerance, numbers.Real), 'type(tolerance) = %s; must be number' % type(self.tolerance))
            check(self.tolerance > 0, 'tolerance = %f; must be > 0' % self.tolerance)
            check(isinstance(self.resolution, numbers.Real), 'type(resolution) = %s; must be number' % type(self.resolution))
            check(self.resolution > 0, 'resolution = %f; must be > 0' % self.resolution)
            if self.seed is not None:
                check(isinstance(self.seed, int), 'type(seed) = %s; must be int' % type(self.seed))
                check(0 <= self.seed <= 4294967295, 'seed = %d; must have 0 <= seed <= 2**32 - 1' % self.seed)
        check(isinstance(self.sample_only_at_l_star, bool), 'type(sample_only_at_l_star) = %s; must be bool.' % type(self.sample_only_at_l_star))
        check(isinstance(self.num_posterior_samples, numbers.Integral), 'type(num_posterior_samples) = %s; must be integer' % type(self.num_posterior_samples))
        self.num_posterior_samples = int(self.num_posterior_samples)
        check(0 <= self.num_posterior_samples <= MAX_NUM_POSTERIOR_SAMPLES, 'num_posterior_samples = %f; need ' % self.num_posterior_samples + '0 <= num_posterior_samples <= %d.' % MAX_NUM_POSTERIOR_SAMPLES)
        check(isinstance(self.max_log_evidence_ratio_drop, numbers.Real), 'type(max_log_evidence_ratio_drop) = %s; must be number' % type(self.max_log_evidence_ratio_drop))
        check(self.max_log_evidence_ratio_drop > 0, 'max_log_evidence_ratio_drop = %f; must be > 0' % self.max_log_evidence_ratio_drop)

    def _clean_data(self):
        """
        Sanitize the assigned data
        :param: self
        :return: None
        """
        data = self.data
        if isinstance(data, LISTLIKE):
            data = np.array(data).ravel()
        else:
            if isinstance(data, set):
                data = np.array(list(data)).ravel()
            else:
                raise ControlledError('Error: could not cast data into an np.array')
        check(all([isinstance(n, numbers.Real) for n in data]), 'not all entries in data are real numbers')
        data = data.astype(float)
        data = data[np.isfinite(data)]
        try:
            if not len(data) > 0:
                raise ControlledError('Input check failed, data must have length > 0: data = %s' % data)
        except ControlledError as e:
            print(e)
            sys.exit(1)

        try:
            data_spread = max(data) - min(data)
            if not np.isfinite(data_spread):
                raise ControlledError('Input check failed. Data[max]-Data[min] is not finite: Data spread = %s' % data_spread)
        except ControlledError as e:
            print(e)
            sys.exit(1)

        try:
            if not data_spread > 0:
                raise ControlledError('Input check failed. Data[max]-Data[min] must be > 0: data_spread = %s' % data_spread)
        except ControlledError as e:
            print(e)
            sys.exit(1)

        self.data = data

    def _set_grid(self):
        """
        Sets the grid based on user input
        """
        data = self.data
        grid = self.grid
        grid_spacing = self.grid_spacing
        num_grid_points = self.num_grid_points
        bounding_box = self.bounding_box
        alpha = self.alpha
        if grid is not None:
            num_grid_points = len(grid)
            assert num_grid_points >= 2 * alpha
            diffs = np.diff(grid)
            grid_spacing = diffs.mean()
            assert grid_spacing > 0
            assert all(np.isclose(diffs, grid_spacing))
            grid_padding = grid_spacing / 2
            lower_bound = grid[0] - grid_padding
            upper_bound = grid[(-1)] + grid_padding
            bounding_box = np.array([lower_bound, upper_bound])
            box_size = upper_bound - lower_bound
        if grid is None:
            assert bounding_box is not None and bounding_box[0] < bounding_box[1]
            lower_bound = bounding_box[0]
            upper_bound = bounding_box[1]
            box_size = upper_bound - lower_bound
        else:
            if not isinstance(data, np.ndarray):
                raise AssertionError
            elif not all(np.isfinite(data)):
                raise AssertionError
            else:
                if not min(data) < max(data):
                    raise AssertionError
                else:
                    data_max = max(data)
                    data_min = min(data)
                    data_span = data_max - data_min
                    lower_bound = data_min - 0.2 * data_span
                    upper_bound = data_max + 0.2 * data_span
                    if data_min >= 0:
                        if lower_bound < 0:
                            lower_bound = 0
                    if data_max <= 0:
                        if upper_bound > 0:
                            upper_bound = 0
                    if data_max <= 1:
                        if upper_bound > 1:
                            upper_bound = 1
                if data_max <= 100:
                    if upper_bound > 100:
                        upper_bound = 100
            lower_bound -= SMALL_NUM * data_span
            upper_bound += SMALL_NUM * data_span
            box_size = upper_bound - lower_bound
            bounding_box = np.array([lower_bound, upper_bound])
        if grid_spacing is not None:
            if not isinstance(grid_spacing, float):
                raise AssertionError
            else:
                if not np.isfinite(grid_spacing):
                    raise AssertionError
                elif not grid_spacing > 0:
                    raise AssertionError
                num_grid_points = np.floor(box_size / grid_spacing).astype(int)
                check(2 * self.alpha <= num_grid_points, 'Using grid_spacing = %f ' % grid_spacing + 'produces num_grid_points = %d, ' % num_grid_points + 'which is too small. Reduce grid_spacing or do not set.')
                check(num_grid_points <= MAX_NUM_GRID_POINTS, 'Using grid_spacing = %f ' % grid_spacing + 'produces num_grid_points = %d, ' % num_grid_points + 'which is too big. Increase grid_spacing or do not set.')
                grid_padding = (box_size - (num_grid_points - 1) * grid_spacing) / 2
                assert grid_spacing / 2 <= grid_padding < grid_spacing
            grid_start = lower_bound + grid_padding
            grid_stop = upper_bound - grid_padding
            grid = np.linspace(grid_start, grid_stop * (1 + SMALL_NUM), num_grid_points)
        else:
            if num_grid_points is not None:
                if not isinstance(num_grid_points, int):
                    raise AssertionError
                elif not 2 * alpha <= num_grid_points <= MAX_NUM_GRID_POINTS:
                    raise AssertionError
                grid_spacing = box_size / num_grid_points
                grid_padding = grid_spacing / 2
                grid_start = lower_bound + grid_padding
                grid_stop = upper_bound - grid_padding
                grid = np.linspace(grid_start, grid_stop * (1 + SMALL_NUM), num_grid_points)
            else:
                if not isinstance(data, np.ndarray):
                    raise AssertionError
                else:
                    assert all(np.isfinite(data))
                    assert min(data) < max(data)
                default_grid_spacing = box_size / DEFAULT_NUM_GRID_POINTS
                min_num_grid_points = 2 * alpha
                data.sort()
                diffs = np.diff(data)
                min_grid_spacing = min(diffs[(diffs > 0)])
                min_grid_spacing = min(min_grid_spacing, box_size / min_num_grid_points)
                grid_spacing = max(min_grid_spacing, default_grid_spacing)
                num_grid_points = np.floor(box_size / grid_spacing).astype(int)
                grid_padding = grid_spacing / 2
                grid_start = lower_bound + grid_padding
                grid_stop = upper_bound - grid_padding
                grid = np.linspace(grid_start, grid_stop * (1 + SMALL_NUM), num_grid_points)
        self.grid = grid
        self.grid_spacing = grid_spacing
        self.grid_padding = grid_padding
        self.num_grid_points = num_grid_points
        self.bounding_box = bounding_box
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.box_size = box_size
        check(2 * self.alpha <= self.num_grid_points <= MAX_NUM_GRID_POINTS, 'After setting grid, we find that num_grid_points = %d; must have %d <= len(grid) <= %d. ' % (
         self.num_grid_points, 2 * self.alpha, MAX_NUM_GRID_POINTS) + 'Something is wrong with input values of grid, grid_spacing, num_grid_points, or bounding_box.')
        self.bin_edges = np.concatenate(([lower_bound],
         grid[:-1] + grid_spacing / 2,
         [
          upper_bound]))