# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/irekua_rest_api/tests/test_entailments.py
# Compiled at: 2019-10-28 01:56:48
# Size of source mod 2**32: 2514 bytes
from uuid import uuid4
from random import choice
from rest_framework.test import APITestCase
from irekua_database.utils import simple_JSON_schema
from irekua_database.models import TermType, EntailmentType, Term
from irekua_rest_api.serializers import entailments
from .utils import BaseTestCase, Users, Actions, create_permission_mapping_from_lists

class EntailmentTestCase(BaseTestCase, APITestCase):
    serializer = entailments.CreateSerializer
    permissions = create_permission_mapping_from_lists({Actions.LIST: Users.ALL_AUTHENTICATED_USERS, 
     Actions.CREATE: [
                      Users.ADMIN,
                      Users.CURATOR], 
     
     Actions.RETRIEVE: Users.ALL_AUTHENTICATED_USERS, 
     Actions.UPDATE: [
                      Users.ADMIN,
                      Users.CURATOR], 
     
     Actions.PARTIAL_UPDATE: [
                              Users.ADMIN,
                              Users.CURATOR], 
     
     Actions.DESTROY: [
                       Users.ADMIN,
                       Users.CURATOR]})

    def setUp(self):
        super().setUp()
        term_type_1 = TermType.objects.create(name=(str(uuid4())),
          description='Random term type',
          is_categorical=True,
          metadata_schema=(simple_JSON_schema()),
          synonym_metadata_schema=(simple_JSON_schema()))
        term_type_2 = TermType.objects.create(name=(str(uuid4())),
          description='Random term type',
          is_categorical=True,
          metadata_schema=(simple_JSON_schema()),
          synonym_metadata_schema=(simple_JSON_schema()))
        EntailmentType.objects.create(source_type=term_type_1,
          target_type=term_type_2,
          metadata_schema=(simple_JSON_schema()))
        self.type_1_terms = [Term.objects.create(term_type=term_type_1, value=(str(uuid4())), description='Random term', metadata={}) for _ in range(40)]
        self.type_2_terms = [Term.objects.create(term_type=term_type_2, value=(str(uuid4())), description='Random term', metadata={}) for _ in range(40)]

    def generate_random_json_data(self):
        term_1 = choice(self.type_1_terms)
        term_2 = choice(self.type_2_terms)
        data = {'source':term_1.pk, 
         'target':term_2.pk, 
         'description':'Random entailment', 
         'metadata':{}}
        return data