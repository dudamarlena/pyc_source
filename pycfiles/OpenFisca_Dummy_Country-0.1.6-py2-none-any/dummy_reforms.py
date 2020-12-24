# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fpagnoux/dev/openfisca/openfisca-dummy-country/openfisca_dummy_country/dummy_reforms.py
# Compiled at: 2017-04-19 14:48:01
from openfisca_core.model_api import *

class neutralization_rsa(Reform):

    def apply(self):
        self.neutralize_variable('rsa')


class salaire_net(Variable):
    definition_period = MONTH

    def function(individu, period):
        salaire_brut = individu('salaire_brut', period)
        return salaire_brut


class remove_social_cotisations(Reform):

    def apply(self):
        self.update_variable(salaire_net)