# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/CDS.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 7173 bytes
__doc__ = '\nConditional Distribution Similarity Statistic\nUsed to infer causal directions\nAuthor : José A.R. Fonollosa\nRef : Fonollosa, José AR, "Conditional distribution variability measures for causality detection", 2016.\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import numpy as np
from collections import Counter
from .model import PairwiseModel
import pandas as pd
BINARY = 'Binary'
CATEGORICAL = 'Categorical'
NUMERICAL = 'Numerical'

def count_unique(x):
    try:
        if type(x) == np.ndarray:
            return len(np.unique(x))
        else:
            return len(set(x))
    except TypeError as e:
        print(x)
        raise e


def numerical(tp):
    assert type(tp) is str
    return tp == NUMERICAL


def len_discretized_values(x, tx, ffactor, maxdev):
    return len(discretized_values(x, tx, ffactor, maxdev))


def discretized_values(x, tx, ffactor, maxdev):
    if numerical(tx) and count_unique(x) > 2 * ffactor * maxdev + 1:
        vmax = ffactor * maxdev
        vmin = -ffactor * maxdev
        return range(vmin, vmax + 1)
    else:
        return sorted(list(set(x)))


def discretized_sequence(x, tx, ffactor, maxdev, norm=True):
    if not norm or numerical(tx) and count_unique(x) > len_discretized_values(x, tx, ffactor, maxdev):
        if norm:
            x = (x - np.mean(x)) / np.std(x)
            xf = x[(abs(x) < maxdev)]
            x = (x - np.mean(xf)) / np.std(xf)
        x = np.round(x * ffactor)
        vmax = ffactor * maxdev
        vmin = -ffactor * maxdev
        x[x > vmax] = vmax
        x[x < vmin] = vmin
    return x


def discretized_sequences(x, y, ffactor=3, maxdev=3):
    return (
     discretized_sequence(x, 'Numerical', ffactor, maxdev),
     discretized_sequence(y, 'Numerical', ffactor, maxdev))


class CDS(PairwiseModel):
    """CDS"""

    def __init__(self, ffactor=2, maxdev=3, minc=12):
        super(CDS, self).__init__()
        self.ffactor = ffactor
        self.maxdev = maxdev
        self.minc = minc

    def predict_proba(self, dataset, **kwargs):
        """ Infer causal relationships between 2 variables using the CDS statistic

        Args:
            dataset (tuple): Couple of np.ndarray variables to classify

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        a, b = dataset
        return self.cds_score(b, a) - self.cds_score(a, b)

    def cds_score(self, x_te, y_te):
        """ Computes the cds statistic from variable 1 to variable 2

        Args:
            x_te (numpy.ndarray): Variable 1
            y_te (numpy.ndarray): Variable 2

        Returns:
            float: CDS fit score
        """
        if type(x_te) == np.ndarray:
            x_te, y_te = pd.Series(x_te.reshape(-1)), pd.Series(y_te.reshape(-1))
        xd, yd = discretized_sequences(x_te, y_te, self.ffactor, self.maxdev)
        cx = Counter(xd)
        cy = Counter(yd)
        yrange = sorted(cy.keys())
        ny = len(yrange)
        py = np.array([cy[i] for i in yrange], dtype=float)
        py = py / py.sum()
        pyx = []
        for a in cx:
            if cx[a] > self.minc:
                yx = y_te[(xd == a)]
                if count_unique(y_te) > len_discretized_values(y_te, 'Numerical', self.ffactor, self.maxdev):
                    yx = (yx - np.mean(yx)) / np.std(y_te)
                    yx = discretized_sequence(yx, 'Numerical', (self.ffactor), (self.maxdev), norm=False)
                    cyx = Counter(yx.astype(int))
                    pyxa = np.array([cyx[i] for i in discretized_values(y_te, 'Numerical', self.ffactor, self.maxdev)], dtype=float)
                else:
                    cyx = Counter(yx)
                    pyxa = [cyx[i] for i in yrange]
                    pyxax = np.array(([0] * (ny - 1) + pyxa + [0] * (ny - 1)), dtype=float)
                    xcorr = [sum(py * pyxax[i:i + ny]) for i in range(2 * ny - 1)]
                    imax = xcorr.index(max(xcorr))
                    pyxa = np.array(([0] * (2 * ny - 2 - imax) + pyxa + [0] * imax), dtype=float)
                assert pyxa.sum() == cx[a]
                pyxa = pyxa / pyxa.sum()
                pyx.append(pyxa)

        if len(pyx) == 0:
            return 0
        else:
            pyx = np.array(pyx)
            pyx = pyx - pyx.mean(axis=0)
            return np.std(pyx)