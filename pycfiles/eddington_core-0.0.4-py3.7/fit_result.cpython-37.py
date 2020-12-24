# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_core/fit_result.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 2138 bytes
from dataclasses import dataclass, field
import numpy as np
import scipy.stats as stats
from eddington_core.print_util import to_precise_string

@dataclass(repr=False)
class FitResult:
    a0: np.ndarray
    a: np.ndarray
    aerr: np.ndarray
    arerr = field(init=False)
    arerr: np.ndarray
    acov: np.ndarray
    degrees_of_freedom: int
    chi2: float
    chi2_reduced = field(init=False)
    chi2_reduced: float
    p_probability = field(init=False)
    p_probability: float
    precision = 3
    precision: int
    _FitResult__repr_string = field(default=None, init=False, repr=False)
    _FitResult__repr_string: str

    def __post_init__(self):
        self.arerr = np.abs(self.aerr / self.a) * 100
        self.chi2_reduced = self.chi2 / self.degrees_of_freedom
        self.p_probability = stats.chi2.sf(self.chi2, self.degrees_of_freedom)

    def __repr__(self):
        if self._FitResult__repr_string is None:
            self._FitResult__repr_string = self.build_repr_string()
        return self._FitResult__repr_string

    def build_repr_string(self):
        old_precision = np.get_printoptions()['precision']
        np.set_printoptions(precision=(self.precision))
        a_value_string = '\n'.join([self._FitResult__a_value_string(i, a, aerr, arerr) for i, (a, aerr, arerr) in enumerate(zip(self.a, self.aerr, self.arerr))])
        repr_string = f"Results:\n========\n\nInitial parameters' values:\n\t{' '.join((str(i) for i in self.a0))}\nFitted parameters' values:\n{a_value_string}\nFitted parameters covariance:\n{self.acov}\nChi squared: {to_precise_string(self.chi2, self.precision)}\nDegrees of freedom: {self.degrees_of_freedom}\nChi squared reduced: {to_precise_string(self.chi2_reduced, self.precision)}\nP-probability: {to_precise_string(self.p_probability, self.precision)}\n"
        np.set_printoptions(precision=old_precision)
        return repr_string

    def __a_value_string(self, i, a, aerr, arerr):
        a_string = to_precise_string(a, self.precision)
        aerr_string = to_precise_string(aerr, self.precision)
        arerr_string = to_precise_string(arerr, self.precision)
        return f"\ta[{i}] = {a_string} ± {aerr_string} ({arerr_string}% error)"