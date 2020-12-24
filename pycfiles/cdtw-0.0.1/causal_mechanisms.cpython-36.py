# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/data/causal_mechanisms.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 11403 bytes
__doc__ = 'Defining a set of classes that represent causal functions/ mechanisms.\n\nAuthor: Diviyan Kalainathan\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import random, numpy as np
from scipy.stats import bernoulli
from sklearn.mixture import GaussianMixture as GMM
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.gaussian_process import GaussianProcessRegressor
import torch as th

class LinearMechanism(object):
    """LinearMechanism"""

    def __init__(self, ncauses, points, noise_function, d=4, noise_coeff=0.4):
        """Init the mechanism."""
        super(LinearMechanism, self).__init__()
        self.n_causes = ncauses
        self.points = points
        self.coefflist = []
        for i in range(ncauses):
            self.coefflist.append(random.random())

        self.noise = noise_coeff * noise_function(points)

    def __call__(self, causes):
        """Run the mechanism."""
        effect = np.zeros((self.points, 1))
        for par in range(causes.shape[1]):
            effect[:, 0] = effect[:, 0] + self.coefflist[par] * causes[:, par]

        effect[:, 0] = effect[:, 0] + self.noise[:, 0]
        return effect


class SigmoidAM_Mechanism(object):

    def __init__(self, ncauses, points, noise_function, d=4, noise_coeff=0.4):
        """Init the mechanism."""
        super(SigmoidAM_Mechanism, self).__init__()
        self.n_causes = ncauses
        self.points = points
        self.a = np.random.exponential(0.25) + 1
        ber = bernoulli.rvs(0.5)
        self.b = ber * np.random.uniform(-2, -0.5) + (1 - ber) * np.random.uniform(0.5, 2)
        self.c = np.random.uniform(-2, 2)
        self.noise = noise_coeff * noise_function(points)

    def mechanism(self, x):
        """Mechanism function."""
        result = np.zeros((
         self.points, 1))
        for i in range(self.points):
            result[(i, 0)] = self.a * self.b * (x[i] + self.c) / (1 + abs(self.b * (x[i] + self.c)))

        return result + self.noise

    def __call__(self, causes):
        """Run the mechanism."""
        effect = np.zeros((self.points, 1))
        for par in range(causes.shape[1]):
            effect[:, 0] = effect[:, 0] + self.mechanism(causes[:, par])[:, 0]

        effect[:, 0] = effect[:, 0] + self.noise[:, 0]
        return effect


class SigmoidMix_Mechanism(object):

    def __init__(self, ncauses, points, noise_function, d=4, noise_coeff=0.4):
        """Init the mechanism."""
        super(SigmoidMix_Mechanism, self).__init__()
        self.n_causes = ncauses
        self.points = points
        self.a = np.random.exponential(0.25) + 1
        ber = bernoulli.rvs(0.5)
        self.b = ber * np.random.uniform(-2, -0.5) + (1 - ber) * np.random.uniform(0.5, 2)
        self.c = np.random.uniform(-2, 2)
        self.noise = noise_coeff * noise_function(points)

    def mechanism(self, causes):
        """Mechanism function."""
        result = np.zeros((self.points, 1))
        for i in range(self.points):
            pre_add_effect = 0
            for c in range(causes.shape[1]):
                pre_add_effect += causes[(i, c)]

            pre_add_effect += self.noise[i]
            result[(i, 0)] = self.a * self.b * (pre_add_effect + self.c) / (1 + abs(self.b * (pre_add_effect + self.c)))

        return result

    def __call__(self, causes):
        """Run the mechanism."""
        effect = np.zeros((self.points, 1))
        effect[:, 0] = self.mechanism(causes)[:, 0]
        return effect


class Polynomial_Mechanism(object):

    def __init__(self, ncauses, points, noise_function, d=2, noise_coeff=0.4):
        """Init the mechanism."""
        super(Polynomial_Mechanism, self).__init__()
        self.n_causes = ncauses
        self.points = points
        self.d = d
        self.polycause = []
        for c in range(ncauses):
            self.coefflist = []
            for j in range(self.d + 1):
                self.coefflist.append(random.random())

            self.polycause.append(self.coefflist)

        self.ber = bernoulli.rvs(0.5)
        self.noise = noise_coeff * noise_function(points)

    def mechanism(self, x, par):
        """Mechanism function."""
        list_coeff = self.polycause[par]
        result = np.zeros((self.points, 1))
        for i in range(self.points):
            for j in range(self.d + 1):
                result[(i, 0)] += list_coeff[j] * np.power(x[i], j)

            result[(i, 0)] = min(result[(i, 0)], 1)
            result[(i, 0)] = max(result[(i, 0)], -1)

        return result

    def __call__(self, causes):
        """Run the mechanism."""
        effect = np.zeros((self.points, 1))
        for par in range(causes.shape[1]):
            effect[:, 0] = effect[:, 0] + self.mechanism(causes[:, par], par)[:, 0]

        if self.ber > 0:
            if causes.shape[1] > 0:
                effect[:, 0] = effect[:, 0] * self.noise[:, 0]
        else:
            effect[:, 0] = effect[:, 0] + self.noise[:, 0]
        return effect


def computeGaussKernel(x):
    """Compute the gaussian kernel on a 1D vector."""
    xnorm = np.power(euclidean_distances(x, x), 2)
    return np.exp(-xnorm / 2.0)


class GaussianProcessAdd_Mechanism(object):

    def __init__(self, ncauses, points, noise_function, noise_coeff=0.4):
        """Init the mechanism."""
        super(GaussianProcessAdd_Mechanism, self).__init__()
        self.n_causes = ncauses
        self.points = points
        self.noise = noise_coeff * noise_function(points)
        self.nb_step = 0

    def mechanism(self, x):
        """Mechanism function."""
        self.nb_step += 1
        x = np.reshape(x, (x.shape[0], 1))
        if self.nb_step < 5:
            cov = computeGaussKernel(x)
            mean = np.zeros((1, self.points))[0, :]
            y = np.random.multivariate_normal(mean, cov)
        else:
            if self.nb_step == 5:
                cov = computeGaussKernel(x)
                mean = np.zeros((1, self.points))[0, :]
                y = np.random.multivariate_normal(mean, cov)
                self.gpr = GaussianProcessRegressor()
                self.gpr.fit(x, y)
                y = self.gpr.predict(x)
            else:
                y = self.gpr.predict(x)
        return y

    def __call__(self, causes):
        """Run the mechanism."""
        effect = np.zeros((self.points, 1))
        for par in range(causes.shape[1]):
            effect[:, 0] = effect[:, 0] + self.mechanism(causes[:, par])

        effect[:, 0] = effect[:, 0] + self.noise[:, 0]
        return effect


class GaussianProcessMix_Mechanism(object):

    def __init__(self, ncauses, points, noise_function, noise_coeff=0.4):
        """Init the mechanism."""
        super(GaussianProcessMix_Mechanism, self).__init__()
        self.n_causes = ncauses
        self.points = points
        self.noise = noise_coeff * noise_function(points)
        self.nb_step = 0

    def mechanism(self, x):
        """Mechanism function."""
        self.nb_step += 1
        x = np.reshape(x, (x.shape[0], x.shape[1]))
        if self.nb_step < 2:
            cov = computeGaussKernel(x)
            mean = np.zeros((1, self.points))[0, :]
            y = np.random.multivariate_normal(mean, cov)
        else:
            if self.nb_step == 2:
                cov = computeGaussKernel(x)
                mean = np.zeros((1, self.points))[0, :]
                y = np.random.multivariate_normal(mean, cov)
                self.gpr = GaussianProcessRegressor()
                self.gpr.fit(x, y)
                y = self.gpr.predict(x)
            else:
                y = self.gpr.predict(x)
        return y

    def __call__(self, causes):
        """Run the mechanism."""
        effect = np.zeros((self.points, 1))
        if causes.shape[1] > 0:
            mix = np.hstack((causes, self.noise))
            effect[:, 0] = self.mechanism(mix)
        else:
            effect[:, 0] = self.mechanism(self.noise)
        return effect


class NN_Mechanism(object):

    def __init__(self, ncauses, points, noise_function, nh=20, noise_coeff=0.4):
        """Init the mechanism."""
        super(NN_Mechanism, self).__init__()
        self.n_causes = ncauses
        self.points = points
        self.noise = noise_coeff * noise_function(points)
        self.nb_step = 0
        self.nh = nh

    def mechanism(self, x):
        """Mechanism function."""
        layers = []
        layers.append(th.nn.modules.Linear(self.n_causes + 1, self.nh))
        layers.append(th.nn.Tanh())
        layers.append(th.nn.modules.Linear(self.nh, 1))
        self.layers = (th.nn.Sequential)(*layers)
        data = x.astype('float32')
        data = th.from_numpy(data)
        return np.reshape(self.layers(data).data, (x.shape[0],))

    def __call__(self, causes):
        """Run the mechanism."""
        effect = np.zeros((self.points, 1))
        if causes.shape[1] > 0:
            mix = np.hstack((causes, self.noise))
            effect[:, 0] = self.mechanism(mix)
        else:
            effect[:, 0] = self.mechanism(self.noise)
        return effect


def gmm_cause(points, k=4, p1=2, p2=2):
    """Init a root cause with a Gaussian Mixture Model w/ a spherical covariance type."""
    g = GMM(k, covariance_type='spherical')
    g.fit(np.random.randn(300, 1))
    g.means_ = p1 * np.random.randn(k, 1)
    g.covars_ = np.power(abs(p2 * np.random.randn(k, 1) + 1), 2)
    g.weights_ = abs(np.random.rand(k))
    g.weights_ = g.weights_ / sum(g.weights_)
    return g.sample(points)[0].reshape(-1)


def gaussian_cause(points):
    """Init a root cause with a Gaussian."""
    return np.random.randn(points, 1)[:, 0]


def normal_noise(points):
    """Init a noise variable."""
    return np.random.rand(1) * np.random.randn(points, 1) + random.sample([2, -2], 1)


def uniform_noise(points):
    """Init a uniform noise variable."""
    return np.random.rand(1) * np.random.uniform(size=(points, 1)) + random.sample([2, -2], 1)