# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/functions.py
# Compiled at: 2013-11-12 16:48:22
from __future__ import division
import sys, os, inspect, traceback, pdb

def between(value, v_min, v_max):
    """More useful than you mght think.
    Takes into account if v_min or v_max are None.
    If one of them is they are taken as -infinity or
    +infinity respectively.
    """
    if v_min == None and v_max == None:
        raise ValueError
    if v_min == None:
        return value < v_max
    else:
        if v_max == None:
            return value > v_min
        return v_min < value < v_max


def reform_text(data_list):
    """put all text objects that are next to eachother into single strings.
    This simplifies a list of data"""
    all_txt = []
    out = []
    for item in data_list:
        if type(item) == str:
            all_txt.append(item)
        else:
            if all_txt:
                out.append(('').join(all_txt))
                all_txt = []
            out.append(item)

    if all_txt:
        out.append(('').join(all_txt))
    return out