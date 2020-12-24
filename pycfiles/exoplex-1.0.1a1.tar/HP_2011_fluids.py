# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/minerals/HP_2011_fluids.py
# Compiled at: 2018-03-29 19:08:50
"""

HP_2011_fluids
^^^^^^^^

Fluids from Holland and Powell 2011 and references therein.
CORK parameters:
CHO gases from Holland and Powell, 1991. ["CO2",304.2,0.0738],["CH4",190.6,0.0460],["H2",41.2,0.0211],["CO",132.9,0.0350]
H2O and S2 from Wikipedia, 2012/10/23. ["H2O",647.096,0.22060],["S2",1314.00,0.21000]
H2S from ancyclopedia.airliquide.com, 2012/10/23. ["H2S",373.15,0.08937]

NB: Units for cork[i] in Holland and Powell datasets are
a = kJ^2/kbar*K^(1/2)/mol^2 -> multiply by 1e-2
b = kJ/kbar/mol -> multiply by 1e-5
c = kJ/kbar^1.5/mol -> multiply by 1e-9
d = kJ/kbar^2/mol -> multiply by 1e-13

Individual terms are divided through by P, P, P^1.5, P^2, so
[0][j] -> multiply by 1e6
[1][j] -> multiply by 1e3
[2][j] -> multiply by 1e3
[3][j] -> multiply by 1e3

cork_P: kbar -> multiply by 1e8
"""
from __future__ import absolute_import
from ..mineral import Mineral
from ..processchemistry import read_masses, dictionarize_formula, formula_mass
atomic_masses = read_masses()

class CO2(Mineral):

    def __init__(self):
        formula = 'CO2'
        formula = dictionarize_formula(formula)
        self.params = {'name': 'carbon dioxide', 
           'formula': formula, 
           'equation_of_state': 'cork', 
           'cork_params': [
                         [
                          54.5963, -8.6392], [0.918301], [-0.0330558, 0.00230524], [0.000693054, -8.38293e-05]], 
           'cork_T': 304.2, 
           'cork_P': 7380000.0, 
           'H_0': -393510.0, 
           'S_0': 213.7, 
           'Cp': [
                87.8, -0.002644, 706400.0, -998.9]}
        Mineral.__init__(self)


class CH4(Mineral):

    def __init__(self):
        formula = 'CH4'
        formula = dictionarize_formula(formula)
        self.params = {'name': 'methane', 
           'formula': formula, 
           'equation_of_state': 'cork', 
           'cork_params': [
                         [
                          54.5963, -8.6392], [0.918301], [-0.0330558, 0.00230524], [0.000693054, -8.38293e-05]], 
           'cork_T': 190.6, 
           'cork_P': 4600000.0, 
           'H_0': -74810.0, 
           'S_0': 186.26, 
           'Cp': [
                150.1, 0.002063, 3427700.0, -2650.4]}
        Mineral.__init__(self)


class O2(Mineral):

    def __init__(self):
        formula = 'O2'
        formula = dictionarize_formula(formula)
        self.params = {'name': 'oxygen gas', 
           'formula': formula, 
           'equation_of_state': 'cork', 
           'cork_params': [
                         [
                          54.5963, -8.6392], [0.918301], [-0.0330558, 0.00230524], [0.000693054, -8.38293e-05]], 
           'cork_T': 0.0, 
           'cork_P': 100000.0, 
           'H_0': 0.0, 
           'S_0': 205.2, 
           'Cp': [
                48.3, -0.000691, 499200.0, -420.7]}
        Mineral.__init__(self)


class H2(Mineral):

    def __init__(self):
        formula = 'H2'
        formula = dictionarize_formula(formula)
        self.params = {'name': 'hydrogen gas', 
           'formula': formula, 
           'equation_of_state': 'cork', 
           'cork_params': [
                         [
                          54.5963, -8.6392], [0.918301], [-0.0330558, 0.00230524], [0.000693054, -8.38293e-05]], 
           'cork_T': 41.2, 
           'cork_P': 2110000.0, 
           'H_0': 0.0, 
           'S_0': 130.7, 
           'Cp': [
                23.3, 0.004627, 0.0, 76.3]}
        Mineral.__init__(self)


class S2(Mineral):

    def __init__(self):
        formula = 'S2'
        formula = dictionarize_formula(formula)
        self.params = {'name': 'sulfur gas', 
           'formula': formula, 
           'equation_of_state': 'cork', 
           'cork_params': [
                         [
                          54.5963, -8.6392], [0.918301], [-0.0330558, 0.00230524], [0.000693054, -8.38293e-05]], 
           'cork_T': 1314.0, 
           'cork_P': 21000000.0, 
           'H_0': 128540.0, 
           'S_0': 231.0, 
           'Cp': [
                37.1, 0.002398, -161000.0, -65.0]}
        Mineral.__init__(self)


class H2S(Mineral):

    def __init__(self):
        formula = 'H2S'
        formula = dictionarize_formula(formula)
        self.params = {'name': 'hydrogen sulfide', 
           'formula': formula, 
           'equation_of_state': 'cork', 
           'cork_params': [
                         [
                          54.5963, -8.6392], [0.918301], [-0.0330558, 0.00230524], [0.000693054, -8.38293e-05]], 
           'cork_T': 373.15, 
           'cork_P': 8937000.0, 
           'H_0': 128540.0, 
           'S_0': 231.0, 
           'Cp': [
                47.4, 0.01024, 615900.0, -397.8]}
        Mineral.__init__(self)