# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/minerals/Murakami_etal_2012.py
# Compiled at: 2018-03-29 19:08:50
"""
Murakami_etal_2012
^^^^^^^^^^^^^^^^^^

Minerals from Murakami et al. (2012) supplementary table 5 and references therein, V_0 from
Stixrude & Lithgow-Bertolloni 2005. Some information from personal communication with Murakami.

"""
from __future__ import absolute_import
from .. import mineral_helpers as helpers
from ..mineral import Mineral

class mg_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 2.445e-05, 
           'K_0': 281000000000.0, 
           'Kprime_0': 4.1, 
           'G_0': 173000000000.0, 
           'Gprime_0': 1.56, 
           'molar_mass': 0.1, 
           'n': 5, 
           'Debye_0': 1070.0, 
           'grueneisen_0': 1.48, 
           'q_0': 1.4, 
           'eta_s_0': 2.4}
        Mineral.__init__(self)


class mg_perovskite_3rdorder(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb3', 
           'V_0': 2.445e-05, 
           'K_0': 281000000000.0, 
           'Kprime_0': 4.1, 
           'G_0': 171420000000.0, 
           'Gprime_0': 1.83, 
           'molar_mass': 0.1, 
           'n': 5, 
           'Debye_0': 1070.0, 
           'grueneisen_0': 1.48, 
           'q_0': 1.4, 
           'eta_s_0': 2.4}
        Mineral.__init__(self)


class fe_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 2.4607e-05, 
           'K_0': 251900000000.0, 
           'Kprime_0': 4.01, 
           'G_0': 164700000000.0, 
           'Gprime_0': 1.58, 
           'molar_mass': 0.102, 
           'n': 5, 
           'Debye_0': 1054.0, 
           'grueneisen_0': 1.48, 
           'q_0': 1.4, 
           'eta_s_0': 2.4}
        Mineral.__init__(self)


class mg_periclase(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 1.124e-05, 
           'K_0': 161000000000.0, 
           'Kprime_0': 3.9, 
           'G_0': 131000000000.0, 
           'Gprime_0': 1.92, 
           'molar_mass': 0.0403, 
           'n': 2, 
           'Debye_0': 773.0, 
           'grueneisen_0': 1.5, 
           'q_0': 1.5, 
           'eta_s_0': 3.0}
        Mineral.__init__(self)


class fe_periclase(helpers.HelperSpinTransition):

    def __init__(self):
        helpers.HelperSpinTransition.__init__(self, 63000000000.0, fe_periclase_LS(), fe_periclase_HS())


class fe_periclase_3rd(helpers.HelperSpinTransition):

    def __init__(self):
        helpers.HelperSpinTransition.__init__(self, 63000000000.0, fe_periclase_LS(), fe_periclase_HS())


class fe_periclase_HS(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 1.1412e-05, 
           'K_0': 159100000000.0, 
           'Kprime_0': 4.11, 
           'G_0': 105430000000.0, 
           'Gprime_0': 1.773, 
           'molar_mass': 0.047, 
           'n': 2, 
           'Debye_0': 706.0, 
           'grueneisen_0': 1.45, 
           'q_0': 1.5, 
           'eta_s_0': 2.54}
        Mineral.__init__(self)


class fe_periclase_LS(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 1.1171e-05, 
           'K_0': 170000000000.0, 
           'Kprime_0': 4.0, 
           'G_0': 116340000000.0, 
           'Gprime_0': 1.668, 
           'molar_mass': 0.047, 
           'n': 2, 
           'Debye_0': 706.0, 
           'grueneisen_0': 1.45, 
           'q_0': 1.5, 
           'eta_s_0': 2.54}
        Mineral.__init__(self)


class fe_periclase_HS_3rd(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb3', 
           'V_0': 1.1412e-05, 
           'K_0': 159100000000.0, 
           'Kprime_0': 4.11, 
           'G_0': 129350000000.0, 
           'Gprime_0': 1.993, 
           'molar_mass': 0.0469, 
           'n': 2, 
           'Debye_0': 706.0, 
           'grueneisen_0': 1.45, 
           'q_0': 1.5, 
           'eta_s_0': 2.54}
        Mineral.__init__(self)


class fe_periclase_LS_3rd(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb3', 
           'V_0': 1.1171e-05, 
           'K_0': 170000000000.0, 
           'Kprime_0': 4.0, 
           'G_0': 151670000000.0, 
           'Gprime_0': 1.754, 
           'molar_mass': 0.0469, 
           'n': 2, 
           'Debye_0': 706.0, 
           'grueneisen_0': 1.45, 
           'q_0': 1.5, 
           'eta_s_0': 2.54}
        Mineral.__init__(self)


mg_bridgmanite = mg_perovskite
fe_bridgmanite = fe_perovskite
mg_bridgmanite_3rdorder = mg_perovskite_3rdorder