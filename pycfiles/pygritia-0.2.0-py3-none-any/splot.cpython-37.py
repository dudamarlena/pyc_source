# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/basic/splot.py
# Compiled at: 2019-02-23 17:07:30
# Size of source mod 2**32: 777 bytes
import matplotlib.pyplot as plt
colors = [
 'black', 'red', 'green', 'blue', 'orange', 'violet',
 'darkred', 'darkgreen', 'navy', 'brown', 'chocolate', 'darkorange',
 'gold', 'olive', 'maroon']

def xy_plot(x_list, y_list, xlabel='x', ylabel='y', fsave='test.pdf'):
    plt.figure()
    plt.plot(x_list, y_list)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(fsave)


def xy2_plot(x_list, y_list, pattern_list, label_list, xlabel='x', ylabel='y', fsave='test.pdf'):
    plt.figure()
    for x, y, pattern, label in zip(x_list, y_list, pattern_list, label_list):
        plt.plot(x, y, pattern, label=label)

    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(fsave)