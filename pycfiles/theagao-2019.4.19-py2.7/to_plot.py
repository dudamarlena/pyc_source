# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/theagao/to_plot.py
# Compiled at: 2019-04-19 04:41:21
import matplotlib.pyplot as plt

def plot_bar(task_data, x, width, color_list, label_list):
    """
    plot n bar of n task with m metrics
    :param task_data: a list, size of [n, m]
    :param x: np.array, shape: [m,0]
    :param width: scalar, width of one bar
    :param color_list: a list, size of [n]
    :param label_list: a list, m meatric names underneath x axis, size of [m]
    :return:
    """
    n_task = len(task_data)
    for i in range(n_task):
        plt.bar(x + width * i, task_data[i], width=width, color=color_list[i], align='center', label=label_list[i], alpha=0.5)

    return True