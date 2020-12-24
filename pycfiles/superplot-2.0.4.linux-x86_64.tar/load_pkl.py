# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/michael/anaconda2/lib/python2.7/site-packages/superplot/example/load_pkl.py
# Compiled at: 2017-08-19 22:58:02
"""
======================
Display a pickled plot
======================
This script demonstrates how a pickled plot file can be loaded from disk and
displayed.

For usage, see `python load_pkl.py --help`.
"""
from argparse import ArgumentParser as arg_parser
from pickle import load
import matplotlib.pyplot as plt

def show_pickle(pickle_name):
    """
    Load and show a pickled plot.

    :param pickle__name: Name of pickled plot
    :type pickle_name: str
    """
    fig_handle = load(open(pickle_name, 'rb'))
    plt.show()


if __name__ == '__main__':
    parser = arg_parser(description='Display a pickled plot.')
    parser.add_argument('pickle_name', type=str, help='Pickled figure to display')
    args = parser.parse_args()
    show_pickle(args.pickle_name)