# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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