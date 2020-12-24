# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/minerals/Matas_etal_2007.py
# Compiled at: 2018-03-29 19:08:50
"""
Matas_etal_2007
^^^^^^^^^^^^^^^

Minerals from Matas et al. 2007 and references therein. See Table 1 and 2.
"""
from __future__ import absolute_import
from ..mineral import Mineral

class mg_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'mgd2', 
           'V_0': 2.443e-05, 
           'K_0': 250000000000.0, 
           'Kprime_0': 4.0, 
           'G_0': 175000000000.0, 
           'Gprime_0': 1.8, 
           'molar_mass': 0.102, 
           'n': 5, 
           'Debye_0': 1070.0, 
           'grueneisen_0': 1.48, 
           'q_0': 1.4}
        Mineral.__init__(self)


class fe_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'mgd2', 
           'V_0': 2.534e-05, 
           'K_0': 250000000000.0, 
           'Kprime_0': 4.0, 
           'G_0': 135000000000.0, 
           'Gprime_0': 1.3, 
           'molar_mass': 0.1319, 
           'n': 5, 
           'Debye_0': 841.0, 
           'grueneisen_0': 1.48, 
           'q_0': 1.4}
        Mineral.__init__(self)


class al_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'mgd2', 
           'V_0': 2.458e-05, 
           'K_0': 249000000000.0, 
           'Kprime_0': 4.0, 
           'G_0': 165000000000.0, 
           'Gprime_0': 1.8, 
           'molar_mass': 0.1005, 
           'n': 5, 
           'Debye_0': 1021.0, 
           'grueneisen_0': 1.48, 
           'q_0': 1.4}
        Mineral.__init__(self)


class ca_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'mgd2', 
           'V_0': 2.745e-05, 
           'K_0': 236000000000.0, 
           'Kprime_0': 3.9, 
           'G_0': 165000000000.0, 
           'Gprime_0': 2.46, 
           'molar_mass': 0.11616, 
           'n': 5, 
           'Debye_0': 984.0, 
           'grueneisen_0': 1.53, 
           'q_0': 1.6}
        Mineral.__init__(self)


class periclase(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'mgd2', 
           'V_0': 1.125e-05, 
           'K_0': 160100000000.0, 
           'Kprime_0': 3.83, 
           'G_0': 130000000000.0, 
           'Gprime_0': 2.2, 
           'molar_mass': 0.0403, 
           'n': 2, 
           'Debye_0': 673.0, 
           'grueneisen_0': 1.41, 
           'q_0': 1.3}
        Mineral.__init__(self)


class wuestite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'mgd2', 
           'V_0': 1.226e-05, 
           'K_0': 160100000000.0, 
           'Kprime_0': 3.83, 
           'G_0': 46000000000.0, 
           'Gprime_0': 0.6, 
           'molar_mass': 0.0718, 
           'n': 2, 
           'Debye_0': 673.0, 
           'grueneisen_0': 1.41, 
           'q_0': 1.3}
        Mineral.__init__(self)


ca_bridgmanite = ca_perovskite
mg_bridgmanite = mg_perovskite
fe_bridgmanite = fe_perovskite
al_bridgmanite = al_perovskite