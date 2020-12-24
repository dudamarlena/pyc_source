# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/reportor.py
# Compiled at: 2019-08-25 22:13:12
# Size of source mod 2**32: 1492 bytes
from collections import Counter
import numpy as np

def classification_report(y_true, y_pred, labels):
    """
    Similar to the one in sklearn.metrics,
    reports per classs recall, precision and F1 score
    """
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()
    corrects = Counter(yt for yt, yp in zip(y_true, y_pred) if yt == yp)
    y_true_counts = Counter(y_true)
    y_pred_counts = Counter(y_pred)
    report = ((lab, corrects[i] / max(1, y_true_counts[i]), corrects[i] / max(1, y_pred_counts[i]), y_true_counts[i]) for i, lab in enumerate(labels))
    report = [(l, r, p, 2 * r * p / max(1e-09, r + p), s) for l, r, p, s in report]
    print('{:<15}{:>10}{:>10}{:>10}{:>10}\n'.format('', 'recall', 'precision', 'f1-score', 'support'))
    formatter = '{:<15}{:>10.2f}{:>10.2f}{:>10.2f}{:>10d}'.format
    for r in report:
        print(formatter(*r))

    print('')
    report2 = list(zip(*[(r * s, p * s, f1 * s) for l, r, p, f1, s in report]))
    N = len(y_true)
    print(formatter('avg / total', sum(report2[0]) / N, sum(report2[1]) / N, sum(report2[2]) / N, N) + '\n')