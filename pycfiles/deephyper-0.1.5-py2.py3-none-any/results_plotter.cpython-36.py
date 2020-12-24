# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/results_plotter.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 3497 bytes
import numpy as np, matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcParams['svg.fonttype'] = 'none'
from deephyper.search.nas.baselines.common import plot_util
X_TIMESTEPS = 'timesteps'
X_EPISODES = 'episodes'
X_WALLTIME = 'walltime_hrs'
Y_REWARD = 'reward'
Y_TIMESTEPS = 'timesteps'
POSSIBLE_X_AXES = [X_TIMESTEPS, X_EPISODES, X_WALLTIME]
EPISODES_WINDOW = 100
COLORS = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'pink',
 'brown', 'orange', 'teal', 'coral', 'lightblue', 'lime', 'lavender', 'turquoise',
 'darkgreen', 'tan', 'salmon', 'gold', 'darkred', 'darkblue']

def rolling_window(a, window):
    shape = a.shape[:-1] + (a.shape[(-1)] - window + 1, window)
    strides = a.strides + (a.strides[(-1)],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)


def window_func(x, y, window, func):
    yw = rolling_window(y, window)
    yw_func = func(yw, axis=(-1))
    return (x[window - 1:], yw_func)


def ts2xy(ts, xaxis, yaxis):
    if xaxis == X_TIMESTEPS:
        x = np.cumsum(ts.l.values)
    else:
        if xaxis == X_EPISODES:
            x = np.arange(len(ts))
        else:
            if xaxis == X_WALLTIME:
                x = ts.t.values / 3600.0
            else:
                raise NotImplementedError
            if yaxis == Y_REWARD:
                y = ts.r.values
            else:
                if yaxis == Y_TIMESTEPS:
                    y = ts.l.values
                else:
                    raise NotImplementedError
    return (
     x, y)


def plot_curves(xy_list, xaxis, yaxis, title):
    fig = plt.figure(figsize=(8, 2))
    maxx = max(xy[0][(-1)] for xy in xy_list)
    minx = 0
    for i, (x, y) in enumerate(xy_list):
        color = COLORS[(i % len(COLORS))]
        plt.scatter(x, y, s=2)
        x, y_mean = window_func(x, y, EPISODES_WINDOW, np.mean)
        plt.plot(x, y_mean, color=color)

    plt.xlim(minx, maxx)
    plt.title(title)
    plt.xlabel(xaxis)
    plt.ylabel(yaxis)
    plt.tight_layout()
    fig.canvas.mpl_connect('resize_event', lambda event: plt.tight_layout())
    plt.grid(True)


def split_by_task(taskpath):
    return taskpath['dirname'].split('/')[(-1)].split('-')[0]


def plot_results(dirs, num_timesteps=10000000.0, xaxis=X_TIMESTEPS, yaxis=Y_REWARD, title='', split_fn=split_by_task):
    results = plot_util.load_results(dirs)
    plot_util.plot_results(results, xy_fn=(lambda r: ts2xy(r['monitor'], xaxis, yaxis)), split_fn=split_fn, average_group=True, resample=(int(1000000.0)))


def main():
    import argparse, os
    parser = argparse.ArgumentParser(formatter_class=(argparse.ArgumentDefaultsHelpFormatter))
    parser.add_argument('--dirs', help='List of log directories', nargs='*', default=['./log'])
    parser.add_argument('--num_timesteps', type=int, default=(int(10000000.0)))
    parser.add_argument('--xaxis', help='Varible on X-axis', default=X_TIMESTEPS)
    parser.add_argument('--yaxis', help='Varible on Y-axis', default=Y_REWARD)
    parser.add_argument('--task_name', help='Title of plot', default='Breakout')
    args = parser.parse_args()
    args.dirs = [os.path.abspath(dir) for dir in args.dirs]
    plot_results(args.dirs, args.num_timesteps, args.xaxis, args.yaxis, args.task_name)
    plt.show()


if __name__ == '__main__':
    main()