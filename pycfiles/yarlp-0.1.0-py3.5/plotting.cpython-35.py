# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/experiment/plotting.py
# Compiled at: 2018-04-01 15:02:11
# Size of source mod 2**32: 3492 bytes
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns, numpy as np

def plot_data(data, value, time, run, condition, title='', ax=None, ci=95):
    """
    Plot time series data using sns.tsplot

    Params
    ----------
    data (pd.DataFrame):
    value (str): value column
    time (str): time column
    condition (str): sns.tsplot condition
    title (str):
    ax (matplotlib axis):
    """
    if isinstance(data, list):
        data = pd.concat(data, ignore_index=True)
    sns.set(style='darkgrid', font_scale=1.5)
    plot = sns.tsplot(data=data, time=time, value=value, unit=run, condition=condition, ax=ax, ci=ci)
    plt.title(title)
    return plot


def normalize_timesteps(data, xname, rew, by, condition):
    """
    Normalize timesteps to fit in sns.tsplots
    """
    return_data = pd.DataFrame()
    ts = data.copy()
    for b in data[by].unique():
        x, y = subsample(ts[(ts[by] == b)][xname], ts[(ts[by] == b)][rew], np.linspace(0, ts[xname].max(), int(ts.shape[0] / 10)))
        units = [b] * x.shape[0]
        cond = [ts[(ts[by] == b)][condition].unique()[0]] * x.shape[0]
        data = pd.DataFrame({xname: x, by: units, 
         rew: y, condition: cond})
        return_data = return_data.append(data)

    return return_data


def subsample(t, vt, bins):
    """
    Given a data such that value vt[i] was observed at time t[i],
    group it into bins: (bins[j], bins[j+1]) such that values
    for bin j is equal to average of all vt[k], such that
    bin[j] <= t[k] < bin[j+1].

    Parameters
    ----------
    t: np.array
        times at which the values are observed
    vt: np.array
        values for those times
    bins: np.array
        endpoints of the bins.
        for n bins it shall be of length n + 1.

    Returns
    -------
    x: np.array
        endspoints of all the bins
    y: np.array
        average values in all bins
    """
    bin_idx = np.digitize(t, bins) - 1
    v_sums = np.zeros(len(bins), dtype=np.float32)
    v_cnts = np.zeros(len(bins), dtype=np.float32)
    np.add.at(v_sums, bin_idx, vt)
    np.add.at(v_cnts, bin_idx, 1)
    zs = np.where(v_cnts == 0)
    for zero_idx in zs:
        v_sums[zero_idx] = v_sums[(zero_idx - 1)]
        v_cnts[zero_idx] = v_cnts[(zero_idx - 1)]

    return (bins[1:], (v_sums / v_cnts)[1:])


def make_plots(data, env, run='run_name', condition='param_run'):
    """
    Make plots by second, timestep, and episode
    """
    figure, axes = plt.subplots(ncols=3, nrows=1, figsize=(18, 6))
    plot1 = plot_data(data, 'Smoothed_total_reward', 'Iteration', run, condition, env, axes[0])
    timestep_data = normalize_timesteps(data, 'timesteps_so_far', 'Smoothed_total_reward', run, condition)
    plot2 = plot_data(timestep_data, 'Smoothed_total_reward', 'timesteps_so_far', run, condition, env, axes[1])
    ts_data = normalize_timesteps(data, 'time_elapsed', 'Smoothed_total_reward', run, condition)
    plot3 = plot_data(ts_data, 'Smoothed_total_reward', 'time_elapsed', run, condition, env, axes[2])
    figure.add_subplot(plot1)
    figure.add_subplot(plot2)
    figure.add_subplot(plot3)
    plt.tight_layout()
    return figure