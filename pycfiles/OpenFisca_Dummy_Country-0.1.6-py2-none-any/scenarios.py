# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fpagnoux/dev/openfisca/openfisca-core/openfisca_core/tests/dummy_country/scenarios.py
# Compiled at: 2017-03-01 05:26:33
from openfisca_core import conv
from openfisca_core.scenarios import AbstractScenario

class Scenario(AbstractScenario):

    def init_single_entity(self, axes=None, enfants=None, famille=None, parent1=None, parent2=None, period=None):
        if enfants is None:
            enfants = []
        assert parent1 is not None
        famille = famille.copy() if famille is not None else {}
        individus = []
        for index, individu in enumerate([parent1, parent2] + (enfants or [])):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                individu['id'] = id = ('ind{}').format(index)
            individus.append(individu)
            if index <= 1:
                famille.setdefault('parents', []).append(id)
            else:
                famille.setdefault('enfants', []).append(id)

        conv.check(self.make_json_or_python_to_attributes())(dict(axes=axes, period=period, test_case=dict(familles=[
         famille], individus=individus)))
        return self