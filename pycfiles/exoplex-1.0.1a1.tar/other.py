# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/minerals/other.py
# Compiled at: 2018-03-29 19:08:50
"""
Other minerals
^^^^^^^^^^^^^^

"""
from __future__ import absolute_import
from .. import mineral_helpers as helpers
from ..mineral import Mineral
from .SLB_2011 import periclase, wuestite, mg_perovskite, fe_perovskite

class ZSB_2013_mg_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb3', 
           'V_0': 2.445e-05, 
           'K_0': 250500000000.0, 
           'Kprime_0': 4.01, 
           'G_0': 172900000000.0, 
           'Gprime_0': 1.74, 
           'molar_mass': 0.1, 
           'n': 5, 
           'Debye_0': 905.9, 
           'grueneisen_0': 1.44, 
           'q_0': 1.09, 
           'eta_s_0': 2.13}
        self.uncertainties = {'err_K_0': 3000000000.0, 
           'err_Kprime_0': 0.1, 
           'err_G_0': 2000000000.0, 
           'err_Gprime_0': 0.0, 
           'err_Debye_0': 5.0, 
           'err_grueneisen_0': 0.05, 
           'err_q_0': 0.3, 
           'err_eta_s_0': 0.3}
        Mineral.__init__(self)


class ZSB_2013_fe_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb3', 
           'V_0': 2.549e-05, 
           'K_0': 272000000000.0, 
           'Kprime_0': 4.1, 
           'G_0': 133000000000.0, 
           'Gprime_0': 1.4, 
           'molar_mass': 0.1319, 
           'n': 5, 
           'Debye_0': 871.0, 
           'grueneisen_0': 1.57, 
           'q_0': 1.1, 
           'eta_s_0': 2.3}
        self.uncertainties = {'err_K_0': 40000000000.0, 
           'err_Kprime_0': 1.0, 
           'err_G_0': 40000000000.0, 
           'err_Gprime_0': 0.0, 
           'err_Debye_0': 26.0, 
           'err_grueneisen_0': 0.3, 
           'err_q_0': 1.0, 
           'err_eta_s_0': 1.0}
        Mineral.__init__(self)


class Speziale_fe_periclase(helpers.HelperSpinTransition):

    def __init__(self):
        helpers.HelperSpinTransition.__init__(self, 60000000000.0, Speziale_fe_periclase_LS(), Speziale_fe_periclase_HS())
        self.cite = 'Speziale et al. 2007'


class Speziale_fe_periclase_HS(Mineral):
    """
    Speziale et al. 2007, Mg#=83
    """

    def __init__(self):
        self.params = {'equation_of_state': 'mgd3', 
           'V_0': 2.29e-05, 
           'K_0': 157500000000.0, 
           'Kprime_0': 3.92, 
           'molar_mass': 0.04567, 
           'n': 2, 
           'Debye_0': 587, 
           'grueneisen_0': 1.46, 
           'q_0': 1.2}
        Mineral.__init__(self)


class Speziale_fe_periclase_LS(Mineral):
    """
    Speziale et al. 2007, Mg#=83
    """

    def __init__(self):
        self.params = {'equation_of_state': 'mgd3', 
           'V_0': 2.149e-05, 
           'K_0': 186000000000.0, 
           'Kprime_0': 4.6, 
           'molar_mass': 0.04567, 
           'n': 2, 
           'Debye_0': 587.0, 
           'grueneisen_0': 1.46, 
           'q_0': 1.2}
        Mineral.__init__(self)


class Liquid_Fe_Anderson(Mineral):
    """
    Anderson & Ahrens, 1994 JGR
    """

    def __init__(self):
        self.params = {'equation_of_state': 'bm4', 
           'V_0': 7.95626e-06, 
           'K_0': 109700000000.0, 
           'Kprime_0': 4.66, 
           'Kprime_prime_0': -4.3e-11, 
           'molar_mass': 0.055845}
        Mineral.__init__(self)


class Fe_Dewaele(Mineral):
    """
    Dewaele et al., 2006, Physical Review Letters
    """

    def __init__(self):
        self.params = {'equation_of_state': 'vinet', 
           'V_0': 6.75e-06, 
           'K_0': 163400000000.0, 
           'Kprime_0': 5.38, 
           'molar_mass': 0.055845, 
           'n': 1}
        Mineral.__init__(self)


class water(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'bm4', 
           'V_0': 1.8797e-05, 
           'K_0': 2060000000.0, 
           'Kprime_0': 6.29, 
           'molar_mass': 0.01801528, 
           'Kprime_prime_0': -1.89 / 2060000000.0, 
           'n': 1}
        Mineral.__init__(self)