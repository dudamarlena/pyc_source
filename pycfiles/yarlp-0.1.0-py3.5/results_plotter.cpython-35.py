# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/results_plotter.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 3080 bytes
import numpy as np, matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype'] = 'none'
from baselines.bench.monitor import load_results
X_TIMESTEPS = 'timesteps'
X_EPISODES = 'episodes'
X_WALLTIME = 'walltime_hrs'
POSSIBLE_X_AXES = [X_TIMESTEPS, X_EPISODES, X_WALLTIME]
EPISODES_WINDOW = 100
COLORS = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'pink',
 'brown', 'orange', 'teal', 'coral', 'lightblue', 'lime', 'lavender', 'turquoise',
 'darkgreen', 'tan', 'salmon', 'gold', 'lightpurple', 'darkred', 'darkblue']

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[(-1)] - window + 1, window)
    strides = a.strides + (a.strides[(-1)],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def window_func(x, y, window, func):
    yw = rolling_window(y, window)
    yw_func = func(yw, axis=-1)
    return (x[window - 1:], yw_func)


def ts2xy(ts, xaxis):
    if xaxis == X_TIMESTEPS:
        x = np.cumsum(ts.l.values)
        y = ts.r.values
    else:
        if xaxis == X_EPISODES:
            x = np.arange(len(ts))
            y = ts.r.values
        else:
            if xaxis == X_WALLTIME:
                x = ts.t.values / 3600.0
                y = ts.r.values
            else:
                raise NotImplementedError
    return (
     x, y)


def plot_curves(xy_list, xaxis, title):
    plt.figure(figsize=(8, 2))
    maxx = max(xy[0][(-1)] for xy in xy_list)
    minx = 0
    for i, (x, y) in enumerate(xy_list):
        color = COLORS[i]
        plt.scatter(x, y, s=2)
        x, y_mean = window_func(x, y, EPISODES_WINDOW, np.mean)
        plt.plot(x, y_mean, color=color)

    plt.xlim(minx, maxx)
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel('Episode Rewards')
    plt.tight_layout()


def plot_results(dirs, num_timesteps, xaxis, task_name):
    tslist = []
    for dir in dirs:
        ts = load_results(dir)
        ts = ts[(ts.l.cumsum() <= num_timesteps)]
        tslist.append(ts)

    xy_list = [ts2xy(ts, xaxis) for ts in tslist]
    plot_curves(xy_list, xaxis, task_name)


def main():
    import argparse, os
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--dirs', help='List of log directories', nargs='*', default=['./log'])
    parser.add_argument('--num_timesteps', type=int, default=int(10000000.0))
    parser.add_argument('--xaxis', help='Varible on X-axis', default=X_TIMESTEPS)
    parser.add_argument('--task_name', help='Title of plot', default='Breakout')
    args = parser.parse_args()
    args.dirs = [os.path.abspath(dir) for dir in args.dirs]
    plot_results(args.dirs, args.num_timesteps, args.xaxis, args.task_name)
    plt.show()


if __name__ == '__main__':
    main()