# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expy_python\core.py
# Compiled at: 2019-04-17 08:47:56
# Size of source mod 2**32: 4450 bytes


def add(x, y):
    return x + y


import math, numpy as np, pandas as pd, scipy
import matplotlib.pyplot as plt
import time, datetime as dt, pyperclip
from pyperclip import copy
from pyperclip import paste

def p(a, b=''):
    print(b + '>>' + str(a))


import sympy as sym
from sympy import init_printing
from sympy import sqrt, sin, cos, tan, exp, log, diff
init_printing()
__DATAPATH__ = './data'
__LATEXPATH__ = './LaTeX'
__TEXDATAPATH__ = './LaTeX/data'
a_, b_, c_, d_, e_, f_, g_, h_, i_, j_, k_, l_, m_, n_, o_, p_, q_, r_, s_, t_, u_, v_, w_, x_, y_, z_ = sym.symbols('a b c d e f g h i j k l m n o p q r s t u v w x y z')
A_, B_, C_, D_, E_, F_, G_, H_, I_, J_, K_, L_, M_, N_, O_, P_, Q_, R_, S_, T_, U_, V_, W_, X_, Y_, Z_ = sym.symbols('A B C D E F G H I J K L M N O P Q R S T U V W X Y Z')
oo_, pi_ = sym.oo, sym.pi
lamda_, theta_ = sym.symbols('lamda theta')

def matplotlib_setup(name='test.jpg'):
    plt.rcParams['mathtext.default'] = 'regular'
    plt.rcParams['xtick.top'] = 'True'
    plt.rcParams['ytick.right'] = 'True'
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.rcParams['xtick.major.width'] = 1.0
    plt.rcParams['ytick.major.width'] = 1.0
    plt.rcParams['axes.grid'] = 'True'
    plt.rcParams['axes.xmargin'] = '0'
    plt.rcParams['axes.ymargin'] = '.05'
    plt.rcParams['axes.linewidth'] = 1.0
    plt.rcParams['savefig.bbox'] = 'tight'
    plt.rcParams['font.size'] = 8
    plt.rcParams['xtick.labelsize'] = 8
    plt.rcParams['ytick.labelsize'] = 8


def begin_plt():
    plt.figure(figsize=(3.14, 3.14))
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))
    plt.gca().xaxis.get_major_formatter().set_useOffset(False)
    plt.locator_params(axis='x', nbins=12)
    plt.locator_params(axis='y', nbins=12, rotation=30)
    plt.gca().yaxis.set_tick_params(which='both', direction='in', bottom=True, top=True,
      left=True,
      right=True)
    plt.xticks(rotation=70)


def end_plt(figname='test.jpg'):
    plt.tight_layout()
    plt.savefig(figname, dpi=600)
    return plt


def mkdf(in_data):
    ind = []
    col = in_data[0]
    data = []
    for i in in_data:
        ind.append(i[0])
        data.append(i[1:])

    if ind[1] == 0:
        return pd.DataFrame((data[1:]), index=None, columns=(col[1:]))
    if col[1] == 0:
        return pd.DataFrame((data[1:]), index=(ind[1:]), columns=None)
    return pd.DataFrame((data[1:]), index=(ind[1:]), columns=(col[1:]))


def reshape_df(arr, col_num, col=None):
    ind = []
    data = []
    for i in range(int(len(arr) / col_num)):
        n1 = i * col_num + 1
        n2 = (i + 1) * col_num
        ind.append(str(n1) + 'to' + str(n2))
        data.append([arr[n1 - 1:n2]])
    else:
        n1 = int(len(arr) / col_num) * col_num + 1
        n2 = int(len(arr) / col_num + 1) * col_num
        ind.append(str(n1) + 'to' + str(len(arr)))
        data.append([arr[n1 - 1:]])

    return pd.DataFrame(data, ind, col)