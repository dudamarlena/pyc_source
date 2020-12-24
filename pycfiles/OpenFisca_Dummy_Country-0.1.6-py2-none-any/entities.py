# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fpagnoux/dev/openfisca/openfisca-core/openfisca_core/tests/dummy_country/entities.py
# Compiled at: 2017-03-19 05:34:13
from openfisca_core.entities import build_entity
Famille = build_entity(key='famille', plural='familles', label='Famille', roles=[
 {'key': 'parent', 
    'plural': 'parents', 
    'label': 'Parents', 
    'subroles': [
               'demandeur', 'conjoint']},
 {'key': 'enfant', 
    'plural': 'enfants', 
    'label': 'Enfants'}])
Individu = build_entity(key='individu', plural='individus', label='Individu', is_person=True)
entities = [
 Individu, Famille]