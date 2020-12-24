# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/utils/latex_printer.py
# Compiled at: 2018-11-09 14:52:59
# Size of source mod 2**32: 1829 bytes
__doc__ = '\nCreated on Mon Jan 22 10:47:38 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import numpy as np
from .to_precision import std_notation

def round_to_2(x):
    if x == 0:
        return x
    return round(x, -int(np.floor(np.log10(np.abs(x)))) + 1)


def round_to_reference(x, y):
    return round(x, -int(np.floor(np.log10(np.abs(y)))) + 1)


def str_digits(y):
    if np.abs(y) < 1:
        return -int(np.floor(np.log10(np.abs(y)))) + 1
    return int(np.floor(np.log10(np.abs(y)))) + 1


def extra_digits(x, y):
    try:
        return int(np.floor(np.log10(np.abs(x)))) - int(np.floor(np.log10(np.abs(y))))
    except:
        return 0


def round_tex(x, err_low, err_up, mode=None):
    if np.isnan(x):
        return 'NaN'
    else:
        y = np.min((np.abs(err_low), np.abs(err_up)))
        digs = extra_digits(x, y) + 2
        if np.abs(err_low - err_up) / np.mean([err_low, err_up]) > 0.05:
            txt = std_notation(x, digs) + '_{-' + std_notation(err_low, 2) + '}^{+' + std_notation(err_up, 2) + '}'
        else:
            txt = std_notation(x, digs) + '\\pm' + std_notation(np.max((np.abs(err_low), np.abs(err_up))), 2)
    if mode is None:
        return txt
    return (
     txt, std_notation(mode, digs))


def round_txt_separately(x, err_low, err_up):
    if np.isnan(x):
        return 'NaN'
    y = np.min((np.abs(err_low), np.abs(err_up)))
    digs = extra_digits(x, y) + 2
    txt1 = std_notation(x, digs)
    txt2 = std_notation(err_low, 2)
    txt3 = std_notation(err_up, 2)
    return (
     txt1, txt2, txt3)