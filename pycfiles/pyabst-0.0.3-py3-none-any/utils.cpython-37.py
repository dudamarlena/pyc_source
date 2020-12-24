# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\pyabsorb\utils.py
# Compiled at: 2019-10-22 07:45:23
# Size of source mod 2**32: 2032 bytes
import re
from .lmnts import atomZlist, atomWeightlist

def get_z(atom='Fe'):
    return atomZlist[atom]


def get_wt(atom='Fe'):
    return atomWeightlist[atom] / 12.0107 * 12


def formula_parser(formula):
    """
    Takes a string containing a brute formula, e.g. e.g. Sr0.85Pr0.15TiO3 or CaO.
    Returns a dictionary of atom labels and stoichiometric coefficients & formula weight.
    """
    stoi_dict = {}
    fw = 0.0
    formula.replace("'", '')
    formula.replace('"', '')
    is_stoi = re.search('\\.', formula)
    if is_stoi is None:
        mix = [a for a in re.split('([A-Z][a-z]*\\d*)', formula) if a]
    else:
        mix = [a for a in re.split('([A-Z][a-z]*[\\d\\.\\d+]*)', formula) if a]
    for aok in mix:
        if any([ch.isdigit() for ch in aok]) == True:
            u, v, w = re.split('(\\d.*)', aok)
            v = float(v)
            if u in stoi_dict:
                stoi_dict['%s' % u] = stoi_dict[('%s' % u)] + v
            else:
                stoi_dict['%s' % u] = v
            fw += get_wt(u) * v

    return (
     stoi_dict, fw)