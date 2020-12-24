# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/minerals/Murakami_2013.py
# Compiled at: 2018-03-29 19:08:50
"""
Murakami_2013
^^^^^^^^^^^^^

Minerals from Murakami 2013 and references therein.

"""
from __future__ import absolute_import
from .. import mineral_helpers as helpers
from ..mineral import Mineral

class periclase(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 1.124e-05, 
           'K_0': 161000000000.0, 
           'Kprime_0': 3.9, 
           'G_0': 130900000000.0, 
           'Gprime_0': 1.92, 
           'molar_mass': 0.0403, 
           'n': 2, 
           'Debye_0': 773.0, 
           'grueneisen_0': 1.5, 
           'q_0': 1.5, 
           'eta_s_0': 2.3}
        Mineral.__init__(self)


class wuestite(Mineral):
    """
    Murakami 2013 and references therein
    """

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 1.206e-05, 
           'K_0': 152000000000.0, 
           'Kprime_0': 4.9, 
           'G_0': 47000000000.0, 
           'Gprime_0': 0.7, 
           'molar_mass': 0.0718, 
           'n': 2, 
           'Debye_0': 455.0, 
           'grueneisen_0': 1.28, 
           'q_0': 1.5, 
           'eta_s_0': 0.8}
        Mineral.__init__(self)


class mg_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 2.445e-05, 
           'K_0': 253000000000.0, 
           'Kprime_0': 4.1, 
           'G_0': 172900000000.0, 
           'Gprime_0': 1.56, 
           'molar_mass': 0.1, 
           'n': 5, 
           'Debye_0': 1100.0, 
           'grueneisen_0': 1.4, 
           'q_0': 1.4, 
           'eta_s_0': 2.6}
        Mineral.__init__(self)


class fe_perovskite(Mineral):

    def __init__(self):
        self.params = {'equation_of_state': 'slb2', 
           'V_0': 2.549e-05, 
           'K_0': 281000000000.0, 
           'Kprime_0': 4.1, 
           'G_0': 138000000000.0, 
           'Gprime_0': 1.7, 
           'molar_mass': 0.1319, 
           'n': 5, 
           'Debye_0': 841.0, 
           'grueneisen_0': 1.48, 
           'q_0': 1.4, 
           'eta_s_0': 2.1}
        Mineral.__init__(self)


mg_bridgmanite = mg_perovskite
fe_bridgmanite = fe_perovskite