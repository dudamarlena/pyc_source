# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/color.py
# Compiled at: 2019-03-13 14:05:20
from __future__ import division
import numpy as np, matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
three_zeros = np.zeros(3)
three_ones = np.ones(3)
color_scheme_dict = {'classic': {'G': [
                   1, 0.65, 0], 
               'TU': [
                    1, 0, 0], 
               'C': [
                   0, 0, 1], 
               'A': [
                   0, 0.5, 0]}, 
   'grays': {'A': 0.2 * three_ones, 
             'C': 0.4 * three_ones, 
             'G': 0.6 * three_ones, 
             'TU': 0.8 * three_ones}, 
   'base_pairing': {'TAU': [
                          1, 0.55, 0], 
                    'GC': [
                         0, 0, 1]}, 
   'hydrophobicity': {'RKDENQ': [
                               0, 0, 1], 
                      'SGHTAP': [
                               0, 0.5, 0], 
                      'YVMCLFIW': [
                                 0, 0, 0]}, 
   'chemistry': {'GSTYC': [
                         0, 0.5, 0], 
                 'QN': [
                      0.5, 0, 0.5], 
                 'KRH': [
                       0, 0, 1], 
                 'DE': [
                      1, 0, 0], 
                 'AVLIPWFM': [
                            0, 0, 0]}, 
   'charge': {'KRH': [
                    0, 0, 1], 
              'DE': [
                   1, 0, 0], 
              'GSTYCQNAVLIPWFM': [
                                0.5, 0.5, 0.5]}, 
   'NajafabadiEtAl2017': {'DEC': [
                                0.42, 0.16, 0.42], 
                          'PG': [
                               0.47, 0.47, 0.0], 
                          'MIWALFV': [
                                    0.13, 0.35, 0.61], 
                          'NTSQ': [
                                 0.25, 0.73, 0.28], 
                          'RK': [
                               0.74, 0.18, 0.12], 
                          'HY': [
                               0.09, 0.47, 0.46]}}

def restrict_dict(in_dict, keys_to_keep):
    return dict([ (k, v) for k, v in in_dict.iteritems() if k in keys_to_keep ])


def cmap_to_color_scheme(chars, cmap_name):
    cmap = plt.get_cmap(cmap_name)
    num_char = len(chars)
    vals = np.linspace(0, 1, 2 * num_char + 1)[1::2]
    color_scheme = {}
    for n, char in enumerate(chars):
        color = cmap(vals[n])[:3]
        color_scheme[char] = color

    return color_scheme


def expand_color_dict(color_dict):
    new_dict = {}
    for key in color_dict.keys():
        value = color_dict[key]
        for char in key:
            new_dict[char.upper()] = value
            new_dict[char.lower()] = value

    return new_dict


def get_color_dict(color_scheme, chars, alpha, shuffle_colors=False):
    """
    get color_dict: each key is 1 char, each value is a 4-vector of rgba values
    This is the main function that OldLogo interfaces with
    """
    is_color = None
    try:
        color = to_rgb(color_scheme)
        is_color = True
    except:
        pass

    color_dict = {}
    if is_color:
        for char in chars:
            color_dict[char] = color

    else:
        if type(color_scheme) == dict:
            color_dict = expand_color_dict(color_scheme)
        elif type(color_scheme) == str:
            if color_scheme == 'none':
                for char in chars:
                    color_dict[char] = [
                     0, 0, 0, 0]

                alpha = 0
            elif color_scheme == 'random':
                for char in chars:
                    color_dict[char] = np.random.rand(3)

            elif color_scheme in color_scheme_dict:
                color_dict = color_scheme_dict[color_scheme]
                color_dict = expand_color_dict(color_dict)
            else:
                cmap_name = color_scheme
                color_dict = cmap_to_color_scheme(chars, cmap_name)
        else:
            assert False, 'color_scheme has invalid type.'
        if not set(chars) <= set(color_dict.keys()):
            for c in chars:
                if c not in color_dict:
                    message = "Warning: Character '%s' is not in color_dict. Using black." % c
                    print message
                    color_dict[c] = to_rgb('black')

        if shuffle_colors:
            chars = color_dict.keys()
            values = color_dict.values()
            np.random.shuffle(chars)
            color_dict = dict(zip(chars, values))
        if alpha is None:
            alpha = 1.0
        for key in color_dict:
            rgb = color_dict[key]
            rgba = np.array(list(rgb)[:3] + [alpha])
            color_dict[key] = rgba

    return color_dict