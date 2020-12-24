# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/tests/test_ordering.py
# Compiled at: 2018-06-14 23:17:51
from django.db import models
from django_evolution.tests.base_test_case import EvolutionTestCase

class OrderingTests(EvolutionTestCase):
    """Testing ordering of operations."""

    def test_deleting_model_and_foreign_key(self):
        """Testing ordering when deleting model and foreign key to model"""

        class Case41Anchor(models.Model):
            value = models.IntegerField()

        class Case41Model(models.Model):
            value = models.IntegerField()
            ref = models.ForeignKey(Case41Anchor)

        class UpdatedCase41Model(models.Model):
            value = models.IntegerField()

        self.set_base_model(Case41Model, extra_models=[
         (
          'Case41Anchor', Case41Anchor)])
        self.register_model(UpdatedCase41Model, name='TestModel')
        end_sig = self.create_test_proj_sig(UpdatedCase41Model, name='TestModel')
        end_sig['tests'].pop('Case41Anchor')
        self.perform_diff_test(end_sig, "The model tests.Case41Anchor has been deleted\nIn model tests.TestModel:\n    Field 'ref' has been deleted", [
         "DeleteField('TestModel', 'ref')",
         "DeleteModel('Case41Anchor')"])