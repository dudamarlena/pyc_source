# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plasma/models/targets.py
# Compiled at: 2017-02-17 21:50:27
import numpy as np, abc

class Target(object):
    activation = 'linear'
    loss = 'mse'

    @abc.abstractmethod
    def remapper(ttd, T_warning):
        return -ttd

    @abc.abstractmethod
    def threshold_range(T_warning):
        return np.logspace(-1, 4, 100)


class BinaryTarget(Target):
    activation = 'sigmoid'
    loss = 'binary_crossentropy'

    @staticmethod
    def remapper(ttd, T_warning, as_array_of_shots=True):
        binary_ttd = 0 * ttd
        mask = ttd < np.log10(T_warning)
        binary_ttd[mask] = 1.0
        binary_ttd[~mask] = 0.0
        return binary_ttd

    @staticmethod
    def threshold_range(T_warning):
        return np.logspace(-6, 0, 100)


class TTDTarget(Target):
    activation = 'linear'
    loss = 'mse'

    @staticmethod
    def remapper(ttd, T_warning):
        mask = ttd < np.log10(T_warning)
        ttd[~mask] = np.log10(T_warning)
        return -ttd

    @staticmethod
    def threshold_range(T_warning):
        return np.linspace(-np.log10(T_warning), 6, 100)


class TTDLinearTarget(Target):
    activation = 'linear'
    loss = 'mse'

    @staticmethod
    def remapper(ttd, T_warning):
        ttd = 10 ** ttd
        mask = ttd < T_warning
        ttd[~mask] = 0
        ttd[mask] = T_warning - ttd[mask]
        return ttd

    @staticmethod
    def threshold_range(T_warning):
        return np.logspace(-6, np.log10(T_warning), 100)


class HingeTarget(Target):
    activation = 'linear'
    loss = 'squared_hinge'

    @staticmethod
    def remapper(ttd, T_warning, as_array_of_shots=True):
        binary_ttd = 0 * ttd
        mask = ttd < np.log10(T_warning)
        binary_ttd[mask] = 1.0
        binary_ttd[~mask] = -1.0
        return binary_ttd

    @staticmethod
    def threshold_range(T_warning):
        return np.concatenate((np.linspace(-2, -1.06, 100), np.linspace(-1.06, -0.96, 100), np.linspace(-0.96, 2, 50)))