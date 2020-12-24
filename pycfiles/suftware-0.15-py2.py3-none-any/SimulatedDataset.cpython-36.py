# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tareen/Desktop/suftware_release_0P13_pip_test/suftware/src/SimulatedDataset.py
# Compiled at: 2018-04-12 16:13:56
# Size of source mod 2**32: 9324 bytes
import numpy as np, math, scipy as sp, scipy.stats as stats, sys, numbers
from suftware.src.utils import ControlledError, handle_errors, check
VALID_DISTRIBUTIONS = '\ngaussian\nnarrow\nwide\nfoothills\naccordian\ngoalposts\ntowers\nuniform\nbeta_convex\nbeta_concave\nexponential\ngamma\ntriangular\nlaplace\nvonmises\n'.split()
MAX_DATASET_SIZE = 1000000.0

class Results:
    pass


def gaussian_mixture(N, weights, mus, sigmas, bbox):
    if not bbox[1] > bbox[0]:
        raise AssertionError
    elif not len(weights) == len(mus) == len(sigmas):
        raise AssertionError
    xs = np.linspace(bbox[0], bbox[1], 10000.0)
    pdf_py = '0'
    pdf_js = '0'
    for m, s, w in zip(mus, sigmas, weights):
        pdf_py += '+(%f/%f)*np.exp(-0.5*np.power((x-(%f))/%f,2))' % (w, s, m, s)
        pdf_js += '+(%f/%f)*Math.exp(-0.5*Math.pow((x-(%f))/%f,2))' % (w, s, m, s)

    ps = np.zeros(len(xs))
    for i, x in enumerate(xs):
        ps[i] = eval(pdf_py)

    ps /= sum(ps)
    data = np.random.choice(xs, size=N, replace=True, p=ps)
    return (
     data, pdf_py, pdf_js)


class SimulatedDataset:
    __doc__ = '\n    Simulates data from a variety of distributions.\n\n    parameters\n    ----------\n\n    distribution: (str)\n        The distribution from which to draw data. Run sw.SimulatedDataset.list()\n        to which distributions are available.\n\n    num_data_points: (int > 0)\n        The number of data points to simulate. Must satisfy\n        0 <= N <= MAX_DATASET_SIZE.\n\n    seed: (int)\n        Seed passed to random number generator.\n\n    attributes\n    ----------\n\n    data: (np.array)\n        The simulated dataset\n\n    bounding_box: ([float, float])\n        Bounding box within which data is generated.\n\n    distribution: (str)\n        Name of the simualted distribution\n\n    pdf_js: (str)\n        Formula for probability density in JavaScript\n\n    pdf_py: (str)\n        Formula for probaiblity density in Python.\n\n    periodic: (bool)\n        Whether the simulated distribution is periodic within bounding_box.\n\n    '

    @handle_errors
    def __init__(self, distribution='gaussian', num_data_points=100, seed=None):
        check(distribution in self.list(), 'distribution = %s is not valid' % distribution)
        check(isinstance(num_data_points, numbers.Integral), 'num_data_points = %s is not an integer.' % num_data_points)
        num_data_points = int(num_data_points)
        check(0 < num_data_points <= MAX_DATASET_SIZE, 'num_data_points = %d; must have 0 < num_data_points <= %d.' % (
         num_data_points, MAX_DATASET_SIZE))
        try:
            np.random.seed(seed)
        except TypeError:
            raise ControlledError('type(seed) = %s; invalid type.' % type(seed))
        except ValueError:
            raise ControlledError('seed = %s; invalid value.' % seed)

        periodic = False
        if distribution == 'gaussian':
            description = 'Gaussian distribution'
            mus = [0.0]
            sigmas = [1.0]
            weights = [1.0]
            bounding_box = [-5, 5]
            data, pdf_py, pdf_js = gaussian_mixture(num_data_points, weights, mus, sigmas, bounding_box)
        else:
            if distribution == 'narrow':
                description = 'Gaussian mixture, narrow separation'
                mus = [-1.25, 1.25]
                sigmas = [1.0, 1.0]
                weights = [1.0, 1.0]
                bounding_box = [-6, 6]
                data, pdf_py, pdf_js = gaussian_mixture(num_data_points, weights, mus, sigmas, bounding_box)
            else:
                if distribution == 'wide':
                    description = 'Gaussian mixture, wide separation'
                    mus = [-2.0, 2.0]
                    sigmas = [1.0, 1.0]
                    weights = [1.0, 0.5]
                    bounding_box = [-6.0, 6.0]
                    data, pdf_py, pdf_js = gaussian_mixture(num_data_points, weights, mus, sigmas, bounding_box)
                else:
                    if distribution == 'foothills':
                        description = 'Foothills (Gaussian mixture)'
                        mus = [0.0, 5.0, 8.0, 10, 11]
                        sigmas = [2.0, 1.0, 0.5, 0.25, 0.125]
                        weights = [1.0, 1.0, 1.0, 1.0, 1.0]
                        bounding_box = [-5, 12]
                        data, pdf_py, pdf_js = gaussian_mixture(num_data_points, weights, mus, sigmas, bounding_box)
                    else:
                        if distribution == 'accordian':
                            description = 'Accordian (Gaussian mixture)'
                            mus = [0.0, 5.0, 8.0, 10, 11, 11.5]
                            sigmas = [2.0, 1.0, 0.5, 0.25, 0.125, 0.0625]
                            weights = [16.0, 8.0, 4.0, 2.0, 1.0, 0.5]
                            bounding_box = [-5, 13]
                            data, pdf_py, pdf_js = gaussian_mixture(num_data_points, weights, mus, sigmas, bounding_box)
                        else:
                            if distribution == 'goalposts':
                                description = 'Goalposts (Gaussian mixture)'
                                mus = [-20, 20]
                                sigmas = [1.0, 1.0]
                                weights = [1.0, 1.0]
                                bounding_box = [-25, 25]
                                data, pdf_py, pdf_js = gaussian_mixture(num_data_points, weights, mus, sigmas, bounding_box)
                            else:
                                if distribution == 'towers':
                                    description = 'Towers (Gaussian mixture)'
                                    mus = [-20, -15, -10, -5, 0, 5, 10, 15, 20]
                                    sigmas = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
                                    weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                                    bounding_box = [-25, 25]
                                    data, pdf_py, pdf_js = gaussian_mixture(num_data_points, weights, mus, sigmas, bounding_box)
                                else:
                                    if distribution == 'uniform':
                                        data = stats.uniform.rvs(size=num_data_points)
                                        bounding_box = [0, 1]
                                        description = 'Uniform distribution'
                                        pdf_js = '1.0'
                                        pdf_py = '1.0'
                                    else:
                                        if distribution == 'beta_convex':
                                            data = stats.beta.rvs(a=0.5, b=0.5, size=num_data_points)
                                            bounding_box = [0, 1]
                                            description = 'Convex beta distribtuion'
                                            pdf_js = 'Math.pow(x,-0.5)*Math.pow(1-x,-0.5)*math.gamma(1)/(math.gamma(0.5)*math.gamma(0.5))'
                                            pdf_py = 'np.power(x,-0.5)*np.power(1-x,-0.5)*math.gamma(1)/(math.gamma(0.5)*math.gamma(0.5))'
                                        else:
                                            if distribution == 'beta_concave':
                                                data = stats.beta.rvs(a=2, b=2, size=num_data_points)
                                                bounding_box = [0, 1]
                                                description = 'Concave beta distribution'
                                                pdf_js = 'Math.pow(x,1)*Math.pow(1-x,1)*math.gamma(4)/(math.gamma(2)*math.gamma(2))'
                                                pdf_py = 'np.power(x,1)*np.power(1-x,1)*math.gamma(4)/(math.gamma(2)*math.gamma(2))'
                                            else:
                                                if distribution == 'exponential':
                                                    data = stats.expon.rvs(size=num_data_points)
                                                    bounding_box = [0, 5]
                                                    description = 'Exponential distribution'
                                                    pdf_js = 'Math.exp(-x)'
                                                    pdf_py = 'np.exp(-x)'
                                                else:
                                                    if distribution == 'gamma':
                                                        data = stats.gamma.rvs(a=3, size=num_data_points)
                                                        bounding_box = [0, 10]
                                                        description = 'Gamma distribution'
                                                        pdf_js = 'Math.pow(x,2)*Math.exp(-x)/math.gamma(3)'
                                                        pdf_py = 'np.power(x,2)*np.exp(-x)/math.gamma(3)'
                                                    else:
                                                        if distribution == 'triangular':
                                                            data = stats.triang.rvs(c=0.5, size=num_data_points)
                                                            bounding_box = [0, 1]
                                                            description = 'Triangular distribution'
                                                            pdf_js = '2-4*Math.abs(x - 0.5)'
                                                            pdf_py = '2-4*np.abs(x - 0.5)'
                                                        else:
                                                            if distribution == 'laplace':
                                                                data = stats.laplace.rvs(size=num_data_points)
                                                                bounding_box = [-5, 5]
                                                                description = 'Laplace distribution'
                                                                pdf_js = '0.5*Math.exp(- Math.abs(x))'
                                                                pdf_py = '0.5*np.exp(- np.abs(x))'
                                                            else:
                                                                if distribution == 'vonmises':
                                                                    data = stats.vonmises.rvs(1, size=num_data_points)
                                                                    bounding_box = [-3.14159, 3.14159]
                                                                    periodic = True
                                                                    description = 'von Mises distribution'
                                                                    pdf_js = 'Math.exp(Math.cos(x))/7.95493'
                                                                    pdf_py = 'np.exp(np.cos(x))/7.95493'
                                                                else:
                                                                    raise ControlledError('Distribution type "%s" not recognized.' % distribution)
        attributes = {'data':data, 
         'bounding_box':bounding_box, 
         'distribution':distribution, 
         'pdf_js':pdf_js, 
         'pdf_py':pdf_py, 
         'periodic':periodic}
        for key, value in attributes.items():
            setattr(self, key, value)

    @staticmethod
    @handle_errors
    def list():
        """
        Return list of valid distributions.
        """
        return VALID_DISTRIBUTIONS