# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/examples/nist_sre/analyze_data.py
# Compiled at: 2019-01-24 05:01:19
# Size of source mod 2**32: 6656 bytes
from __future__ import print_function, division, absolute_import
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import os
os.environ['ODIN'] = 'gpu,float32'
import shutil
from collections import defaultdict
import numpy as np, numba as nb, tensorflow as tf, seaborn as sns, pandas as pd
from sklearn.metrics import accuracy_score, log_loss, f1_score
from odin import fuel as F
from odin import nnet as N, backend as K
from odin import visual as V
from odin.utils import ctext, mpi, Progbar, catch_warnings_ignore, stdio, get_logpath, catch_warnings_ignore
from helpers import FEATURE_RECIPE, FEATURE_NAME, PATH_ACOUSTIC_FEATURES, MINIMUM_UTT_DURATION, ANALYSIS_DIR, Config, filter_utterances, prepare_dnn_data
stdio(get_logpath(name='analyze_data.log', increasing=True, odin_base=False,
  root=ANALYSIS_DIR))
print(ctext(FEATURE_RECIPE, 'lightyellow'))
print(ctext(FEATURE_NAME, 'lightyellow'))
assert os.path.isdir(os.path.join(PATH_ACOUSTIC_FEATURES, FEATURE_RECIPE))
figure_path = os.path.join(ANALYSIS_DIR, '%s_%s.pdf' % (
 FEATURE_RECIPE.replace('_', ''), FEATURE_NAME))
print(ctext(figure_path, 'lightyellow'))
ds = F.Dataset((os.path.join(PATH_ACOUSTIC_FEATURES, FEATURE_RECIPE)), read_only=True)
X = ds[FEATURE_NAME]
indices = {name:(start, end) for name, (start, end) in ds[('indices_%s' % FEATURE_NAME)].items() if '/' not in name if '/' not in name}
all_dataset = sorted(set(ds['dsname'].values()))
print('All dataset:', ctext(all_dataset, 'cyan'))
all_percentiles = [
 0.01, 0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]

def clipping_quartile(x, alpha=8):
    x = x.astype('int32')
    Q1 = np.percentile(x, q=25)
    Q3 = np.percentile(x, q=75)
    IQR = Q3 - Q1
    x = x[(x < Q3 + alpha * IQR)]
    x = x[(x > Q1 - alpha * IQR)]
    return x


def dataset_statistics(dsname):
    ids = {name:(start, end) for name, (start, end) in indices.items() if ds['dsname'][name] == dsname}
    name2spk = {name:ds['spkid'][name] for name in ids.keys()}
    s = []
    s.append('============' + ctext('%-12s' % dsname, 'lightyellow') + '============')
    s.append('#Files   :' + ctext(len(ids), 'cyan'))
    s.append('#Speakers:' + ctext(len(set(name2spk.values())), 'cyan'))
    sum1 = 0.0
    sum2 = 0.0
    n = 0
    spk_sum1 = defaultdict(float)
    spk_sum2 = defaultdict(float)
    spk_n = defaultdict(int)
    for name, (start, end) in ids.items():
        spkid = name2spk[name]
        n += end - start
        spk_n[spkid] += end - start
        x = X[start:end][:].astype('float64')
        s1 = np.sum(x, axis=0)
        s2 = np.sum((x ** 2), axis=0)
        sum1 += s1
        sum2 += s2
        spk_sum1[spkid] += s1
        spk_sum2[spkid] += s2

    data_mean = sum1 / n
    data_std = np.sqrt(sum2 / n - data_mean ** 2)
    spk_stats = {}
    for spkid in name2spk.values():
        n = spk_n[spkid]
        s1, s2 = spk_sum1[spkid], spk_sum2[spkid]
        mean = s1 / n
        std = np.sqrt(s2 / n - mean ** 2)
        spk_stats[spkid] = (mean, std)

    spk_mean = np.concatenate([x[0][None, :] for x in spk_stats.values()], axis=0).mean(0)
    spk_std = np.concatenate([x[1][None, :] for x in spk_stats.values()], axis=0).mean(0)
    all_length = np.array([(end - start) * Config.STEP_LENGTH for start, end in indices.values()])
    nutt_per_spk = defaultdict(int)
    dur_per_spk = defaultdict(list)
    for name, (start, end) in ids.items():
        spkid = name2spk[name]
        nutt_per_spk[spkid] += 1
        dur_per_spk[spkid].append((end - start) * Config.STEP_LENGTH)

    all_spk = sorted(nutt_per_spk.keys())
    spk_df = pd.DataFrame(data={'nutt_per_spk':[nutt_per_spk[spk] for spk in all_spk],  'sum_per_spk':[np.sum(dur_per_spk[spk]) for spk in all_spk], 
     'mean_per_spk':[np.mean(dur_per_spk[spk]) for spk in all_spk]})
    return (
     dsname, '\n'.join(s), (all_length, spk_df), (data_mean, data_std), (spk_mean, spk_std))


n_bin = 120
n_col = 3
linestyles = ['-', '--', '-.']

def plot_histogram(series, ax, title):
    V.plot_histogram(x=(clipping_quartile(series)), bins=n_bin, ax=ax, title=title,
      fontsize=4)


def plot_mean_std(_map, title):
    V.plot_figure(nrow=6, ncol=20)
    for i, dsname in enumerate(all_dataset):
        mean, _ = _map[dsname]
        plt.plot(mean, linewidth=1.0,
          linestyle=(linestyles[(i % len(linestyles))]),
          label=dsname)

    plt.legend()
    plt.suptitle('[%s]Mean' % title)
    V.plot_figure(nrow=6, ncol=20)
    for i, dsname in enumerate(all_dataset):
        _, std = _map[dsname]
        plt.plot(std, linewidth=1.0,
          linestyle=(linestyles[(i % len(linestyles))]),
          label=dsname)

    plt.legend()
    plt.suptitle('[%s]StandardDeviation' % title)


with catch_warnings_ignore(RuntimeWarning):
    with catch_warnings_ignore(FutureWarning):
        data_map = {}
        stats_map = {}
        spk_map = {}
        for dsname, text, data, stats, spk_stats in mpi.MPI(jobs=all_dataset, func=dataset_statistics, ncpu=None,
          batch=1):
            data_map[dsname] = data
            stats_map[dsname] = stats
            spk_map[dsname] = spk_stats
            print(text)

        for dsname in all_dataset:
            print('Plotting ...', ctext(dsname, 'cyan'))
            data = data_map[dsname]
            V.plot_figure(nrow=2, ncol=20)
            ax = plt.subplot(1, n_col, 1)
            plot_histogram((data[0]), ax, title='Duration')
            ax = plt.subplot(1, n_col, 2)
            plot_histogram((data[1]['sum_per_spk']), ax, title='Dur/Spk')
            ax = plt.subplot(1, n_col, 3)
            plot_histogram((data[1]['nutt_per_spk']), ax, title='#Utt/Spk')
            plt.suptitle(dsname, fontsize=8)

        plot_mean_std(_map=stats_map, title='Data')
        plot_mean_std(_map=spk_map, title='Speaker')
V.plot_save(figure_path, dpi=32)