# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/minerals/SLB_2011_ZSB_2013.py
# Compiled at: 2018-03-29 19:08:50
"""
SLB_2011_ZSB_2013
^^^^^^^^^^^^^^^^^

Minerals from Stixrude & Lithgow-Bertelloni 2011, Zhang, Stixrude & Brodholt 2013, and references therein.

"""
from __future__ import absolute_import
from .. import mineral_helpers as helpers
from ..mineral import Mineral

class stishovite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb3', 
           'V_0': 1.402e-05, 
           'K_0': 314000000000.0, 
           'Kprime_0': 3.8, 
           'G_0': 220000000000.0, 
           'Gprime_0': 1.9, 
           'molar_mass': 0.0601, 
           'n': 3, 
           'Debye_0': 1108.0, 
           'grueneisen_0': 1.37, 
           'q_0': 2.8, 
           'eta_s_0': 4.6}
        self.uncertainties = {'err_K_0': 8000000000.0, 
           'err_Kprime_0': 0.1, 
           'err_G_0': 12000000000.0, 
           'err_Gprime_0': 0.1, 
           'err_Debye_0': 13.0, 
           'err_grueneisen_0': 0.17, 
           'err_q_0': 2.2, 
           'err_eta_s_0': 1.0}
        Mineral.__init__(self)


class periclase(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb3', 
           'V_0': 1.124e-05, 
           'K_0': 161000000000.0, 
           'Kprime_0': 3.8, 
           'G_0': 131000000000.0, 
           'Gprime_0': 2.1, 
           'molar_mass': 0.0403, 
           'n': 2, 
           'Debye_0': 767.0, 
           'grueneisen_0': 1.36, 
           'q_0': 1.7, 
           'eta_s_0': 2.8}
        self.uncertainties = {'err_K_0': 3000000000.0, 
           'err_Kprime_0': 0.2, 
           'err_G_0': 1000000000.0, 
           'err_Gprime_0': 0.1, 
           'err_Debye_0': 9.0, 
           'err_grueneisen_0': 0.05, 
           'err_q_0': 0.2, 
           'err_eta_s_0': 0.2}
        Mineral.__init__(self)


class wuestite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb3', 
           'V_0': 1.226e-05, 
           'K_0': 179000000000.0, 
           'Kprime_0': 4.9, 
           'G_0': 59000000000.0, 
           'Gprime_0': 1.4, 
           'molar_mass': 0.0718, 
           'n': 2, 
           'Debye_0': 454.0, 
           'grueneisen_0': 1.53, 
           'q_0': 1.7, 
           'eta_s_0': -0.1}
        self.uncertainties = {'err_K_0': 1000000000.0, 
           'err_Kprime_0': 0.2, 
           'err_G_0': 1000000000.0, 
           'err_Gprime_0': 0.1, 
           'err_Debye_0': 21.0, 
           'err_grueneisen_0': 0.13, 
           'err_q_0': 1.0, 
           'err_eta_s_0': 1.0}
        Mineral.__init__(self)


class mg_perovskite(Mineral):

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


class fe_perovskite(Mineral):

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


mg_bridgmanite = mg_perovskite
fe_bridgmanite = fe_perovskite