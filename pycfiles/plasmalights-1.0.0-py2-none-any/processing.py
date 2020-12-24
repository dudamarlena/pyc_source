# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plasma/utils/processing.py
# Compiled at: 2017-02-17 21:50:27
__doc__ = '\n#########################################################\nThis file containts classes to handle data processing\n\nAuthor: Julian Kates-Harbeck, jkatesharbeck@g.harvard.edu\n\nThis work was supported by the DOE CSGF program.\n#########################################################\n'
from __future__ import print_function
import itertools, numpy as np
from scipy.interpolate import UnivariateSpline

def resample_signal(t, sig, tmin, tmax, dt):
    order = np.argsort(t)
    t = t[order]
    sig = sig[order]
    tt = np.arange(tmin, tmax, dt)
    f = UnivariateSpline(t, sig, s=0, k=1, ext=0)
    sig_interp = f(tt)
    if np.any(np.isnan(sig_interp)):
        print('signals contains nan')
    if np.any(t[1:] - t[:-1] <= 0):
        print('non increasing')
        idx = np.where(t[1:] - t[:-1] <= 0)[0][0]
        print(t[idx - 10:idx + 10])
    return (
     tt, sig_interp)


def cut_signal(t, sig, tmin, tmax):
    mask = np.logical_and(t >= tmin, t <= tmax)
    return (
     t[mask], sig[mask])


def cut_and_resample_signal(t, sig, tmin, tmax, dt):
    t, sig = cut_signal(t, sig, tmin, tmax)
    return resample_signal(t, sig, tmin, tmax, dt)


def get_individual_shot_file(prepath, shot_num, ext='.txt'):
    return prepath + str(shot_num) + ext


def append_to_filename(path, to_append):
    ending_idx = path.rfind('.')
    new_path = path[:ending_idx] + to_append + path[ending_idx:]
    return new_path


def train_test_split(x, frac, do_shuffle=False):
    if not isinstance(x, np.ndarray):
        return train_test_split_robust(x, frac, do_shuffle)
    mask = np.array(range(len(x))) < frac * len(x)
    if do_shuffle:
        np.random.shuffle(mask)
    return (x[mask], x[(~mask)])


def train_test_split_robust(x, frac, do_shuffle=False):
    mask = np.array(range(len(x))) < frac * len(x)
    if do_shuffle:
        np.random.shuffle(mask)
    train = []
    test = []
    for i, _x in enumerate(x):
        if mask[i]:
            train.append(_x)
        else:
            test.append(_x)

    return (
     train, test)


def train_test_split_all(x, frac, do_shuffle=True):
    groups = []
    length = len(x[0])
    mask = np.array(range(length)) < frac * length
    if do_shuffle:
        np.random.shuffle(mask)
    for item in x:
        groups.append((item[mask], item[(~mask)]))

    return groups


def concatenate_sublists(superlist):
    return list(itertools.chain.from_iterable(superlist))


def get_signal_slices(signals_superlist):
    indices_superlist = []
    signals_so_far = 0
    for sublist in signals_superlist:
        indices_sublist = signals_so_far + np.array(range(len(sublist)))
        signals_so_far += len(sublist)
        indices_superlist.append(indices_sublist)

    return indices_superlist