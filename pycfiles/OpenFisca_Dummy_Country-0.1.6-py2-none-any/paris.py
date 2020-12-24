# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fpagnoux/dev/openfisca/openfisca-dummy-country/openfisca_dummy_country/dummy_extension/paris.py
# Compiled at: 2017-04-19 14:48:01
from openfisca_core.model_api import *
from openfisca_dummy_country.entities import Famille

class paris_logement_familles(Variable):
    column = FloatCol
    label = 'Allocation Paris Logement Famille'
    entity = Famille
    definition_period = MONTH

    def function(famille, period):
        condition = round_(famille('city_code', period).astype(int) / 1000) == 75
        return condition * 100