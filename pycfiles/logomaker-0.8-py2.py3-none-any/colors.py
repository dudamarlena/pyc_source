# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../logomaker/src/colors.py
# Compiled at: 2019-05-03 09:22:14
from __future__ import division
import numpy as np, pandas as pd
from matplotlib.colors import to_rgb
from logomaker.src.error_handling import check
from logomaker.src.matrix import ALPHABET_DICT
CHARS_TO_COLORS_DICT = {tuple('ACGT'): 'classic', 
   tuple('ACGU'): 'classic', 
   tuple('ACDEFGHIKLMNPQRSTVWY'): 'weblogo_protein'}
weblogo_blue = [
 0.02, 0.09, 0.74]
weblogo_pink = [0.83, 0.11, 0.75]
weblogo_green = [0.13, 0.83, 0.15]
weblogo_red = [0.83, 0.04, 0.08]
weblogo_black = [0, 0, 0]
three_ones = np.ones(3)
COLOR_SCHEME_DICT = {'classic': {'G': [
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
   'weblogo_protein': {'RHK': weblogo_blue, 
                       'DE': weblogo_red, 
                       'QN': weblogo_pink, 
                       'GCSTY': weblogo_green, 
                       'ILMAFVPW': weblogo_black}, 
   'skylign_protein': {'F': [
                           0.16, 0.99, 0.18], 
                       'Y': [
                           0.04, 0.4, 0.05], 
                       'L': [
                           0.99, 0.6, 0.25], 
                       'V': [
                           1.0, 0.8, 0.27], 
                       'I': [
                           0.8, 0.6, 0.24], 
                       'H': [
                           0.4, 0.02, 0.2], 
                       'W': [
                           0.42, 0.79, 0.42], 
                       'A': [
                           0.99, 0.6, 0.42], 
                       'S': [
                           0.04, 0.14, 0.98], 
                       'T': [
                           0.17, 1.0, 1.0], 
                       'M': [
                           0.8, 0.6, 0.8], 
                       'N': [
                           0.21, 0.4, 0.4], 
                       'Q': [
                           0.4, 0.41, 0.79], 
                       'R': [
                           0.59, 0.02, 0.04], 
                       'K': [
                           0.4, 0.2, 0.03], 
                       'E': [
                           0.79, 0.04, 0.22], 
                       'G': [
                           0.95, 0.94, 0.22], 
                       'D': [
                           0.99, 0.05, 0.11], 
                       'P': [
                           0.1, 0.61, 0.99], 
                       'C': [
                           0.09, 0.6, 0.6]}, 
   'dmslogo_charge': {'A': '#000000', 
                      'C': '#000000', 
                      'D': '#0000FF', 
                      'E': '#0000FF', 
                      'F': '#000000', 
                      'G': '#000000', 
                      'H': '#FF0000', 
                      'I': '#000000', 
                      'K': '#FF0000', 
                      'L': '#000000', 
                      'M': '#000000', 
                      'N': '#000000', 
                      'P': '#000000', 
                      'Q': '#000000', 
                      'R': '#FF0000', 
                      'S': '#000000', 
                      'T': '#000000', 
                      'V': '#000000', 
                      'W': '#000000', 
                      'Y': '#000000'}, 
   'dmslogo_funcgroup': {'A': '#f76ab4', 
                         'C': '#ff7f00', 
                         'D': '#e41a1c', 
                         'E': '#e41a1c', 
                         'F': '#84380b', 
                         'G': '#f76ab4', 
                         'H': '#3c58e5', 
                         'I': '#12ab0d', 
                         'K': '#3c58e5', 
                         'L': '#12ab0d', 
                         'M': '#12ab0d', 
                         'N': '#972aa8', 
                         'P': '#12ab0d', 
                         'Q': '#972aa8', 
                         'R': '#3c58e5', 
                         'S': '#ff7f00', 
                         'T': '#ff7f00', 
                         'V': '#12ab0d', 
                         'W': '#84380b', 
                         'Y': '#84380b'}, 
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

def list_color_schemes():
    """
    Provides user with a list of valid color_schemes built into Logomaker.

    returns
    -------
    colors_df: (dataframe)
        A pandas dataframe listing each color_scheme and the corresponding
        set of characters for which colors are specified.
    """
    names = list(COLOR_SCHEME_DICT.keys())
    colors_df = pd.DataFrame()
    for i, name in enumerate(names):
        color_scheme = COLOR_SCHEME_DICT[name]
        characters = list(('').join(list(color_scheme.keys())))
        characters.sort()
        colors_df.loc[(i, 'color_scheme')] = name
        colors_df.loc[(i, 'characters')] = ('').join(characters)

    return colors_df


def _restrict_dict(in_dict, keys_to_keep):
    """ Restricts a in_dict to keys that fall within keys_to_keep. """
    return dict([ (k, v) for k, v in in_dict.items() if k in keys_to_keep ])


def _expand_color_dict(color_dict):
    """ Expands the string keys in color_dict, returning new_dict that has
    the same values but whose keys are single characters. These single
    characters are both uppercase and lowercase versions of the characters
    in the color_dict keys. """
    new_dict = {}
    for key in color_dict.keys():
        value = color_dict[key]
        for char in key:
            new_dict[char.upper()] = value
            new_dict[char.lower()] = value

    return new_dict


def get_rgb(color_spec):
    """
    Safely returns an RGB np.ndarray given a valid color specification
    """
    rgb = None
    if isinstance(color_spec, str):
        try:
            rgb = np.array(to_rgb(color_spec))
        except:
            check(False, 'invalid choice: color_spec=%s' % color_spec)

    elif isinstance(color_spec, (list, tuple, np.ndarray)):
        check(len(color_spec) == 3, 'color_scheme, if array, must be of length 3.')
        check(all(0 <= x <= 1 for x in color_spec), 'Values of color_spec must be between 0 and 1 inclusive.')
        rgb = np.array(color_spec)
    else:
        check(False, 'type(color_spec) = %s is invalid.' % type(color_spec))
    return rgb


def get_color_dict(color_scheme, chars):
    """
    Return a color_dict constructed from a user-specified color_scheme and
    a list of characters
    """
    check(isinstance(chars, (str, list, tuple, np.ndarray)), 'chars must be a str or be array-like')
    check(len(chars) >= 1, 'chars must have length >= 1')
    chars = list(chars)
    chars.sort()
    for i, c in enumerate(chars):
        c = str(c)
        check(isinstance(c, str) and len(c) == 1, 'entry number %d in chars is %s; ' % (i, repr(c)) + 'must instead be a single character')

    if color_scheme is None:
        key = tuple(chars)
        color_scheme = CHARS_TO_COLORS_DICT.get(key, 'gray')
        color_dict = get_color_dict(color_scheme, chars)
    elif isinstance(color_scheme, dict):
        for key in color_scheme.keys():
            check(isinstance(key, str), 'color_scheme dict contains a key (%s) ' % repr(key) + 'that is not of type str.')

        color_dict = _expand_color_dict(color_scheme)
        for key in color_dict.keys():
            color_dict[key] = to_rgb(color_dict[key])

    elif isinstance(color_scheme, str):
        if color_scheme in COLOR_SCHEME_DICT.keys():
            tmp_dict = COLOR_SCHEME_DICT[color_scheme]
            color_dict = _expand_color_dict(tmp_dict)
            for c in color_dict.keys():
                color = color_dict[c]
                rgb = to_rgb(color)
                color_dict[c] = np.array(rgb)

        else:
            try:
                rgb = to_rgb(color_scheme)
                color_dict = dict([ (c, rgb) for c in chars ])
            except:
                check(False, 'invalid choice: color_scheme=%s' % color_scheme)

    elif isinstance(color_scheme, (list, tuple, np.ndarray)):
        check(len(color_scheme) == 3, 'color_scheme, if array, must be of length 3.')
        rgb = np.ndarray(color_scheme)
        color_dict = dict([ (c, rgb) for c in chars ])
    else:
        check(False, 'Error: color_scheme has invalid type %s' % type(color_scheme))
    if not set(chars) <= set(color_dict.keys()):
        for c in chars:
            if c not in color_dict:
                print " Warning: Character '%s' is not in color_dict. " % c + 'Using black.'
                color_dict[c] = to_rgb('black')

    return color_dict