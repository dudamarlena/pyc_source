# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/tests/test_unique_together.py
# Compiled at: 2018-06-14 23:17:51
from django.db import models
from django_evolution.mutations import ChangeMeta
from django_evolution.tests.base_test_case import EvolutionTestCase

class NoUniqueTogetherBaseModel(models.Model):
    int_field1 = models.IntegerField()
    int_field2 = models.IntegerField()
    char_field1 = models.CharField(max_length=20)
    char_field2 = models.CharField(max_length=40)


class UniqueTogetherBaseModel(models.Model):
    int_field1 = models.IntegerField()
    int_field2 = models.IntegerField()
    char_field1 = models.CharField(max_length=20)
    char_field2 = models.CharField(max_length=40)

    class Meta:
        unique_together = [
         ('int_field1', 'char_field1')]


class UniqueTogetherTests(EvolutionTestCase):
    """Testing ChangeMeta with adding unique_together"""
    sql_mapping_key = 'unique_together'
    DIFF_TEXT = "In model tests.TestModel:\n    Meta property 'unique_together' has changed"

    def test_keeping_empty(self):
        """Testing ChangeMeta(unique_together) and keeping list empty"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                unique_together = []

        self.set_base_model(NoUniqueTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [])], None, None, None, expect_noop=True)
        return

    def test_setting_from_empty(self):
        """Testing ChangeMeta(unique_together) and setting to valid list"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                unique_together = [
                 ('int_field1', 'char_field1')]

        self.set_base_model(NoUniqueTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [
          ('int_field1', 'char_field1')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'unique_together', [('int_field1', 'char_field1')])"], 'setting_from_empty')

    def test_replace_list(self):
        """Testing ChangeMeta(unique_together) and replacing list"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                unique_together = [
                 ('int_field2', 'char_field2')]

        self.set_base_model(UniqueTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [
          ('int_field2', 'char_field2')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'unique_together', [('int_field2', 'char_field2')])"], 'replace_list')

    def test_append_list(self):
        """Testing ChangeMeta(unique_together) and appending list"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                unique_together = [
                 ('int_field1', 'char_field1'),
                 ('int_field2', 'char_field2')]

        self.set_base_model(UniqueTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [
          ('int_field1', 'char_field1'),
          ('int_field2', 'char_field2')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'unique_together', [('int_field1', 'char_field1'), ('int_field2', 'char_field2')])"], 'append_list')

    def test_removing(self):
        """Testing ChangeMeta(unique_together) and removing property"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

        self.set_base_model(UniqueTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'unique_together', [])"], 'removing')

    def test_set_remove(self):
        """Testing ChangeMeta(unique_together) and setting indexes and removing
        one
        """

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                unique_together = [
                 ('int_field1', 'char_field1')]

        self.set_base_model(NoUniqueTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [
          ('int_field1', 'char_field1'),
          ('int_field2', 'char_field2')]),
         ChangeMeta('TestModel', 'unique_together', [
          ('int_field1', 'char_field1')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'unique_together', [('int_field1', 'char_field1')])"], 'set_remove')

    def test_missing_indexes(self):
        """Testing ChangeMeta(unique_together) and old missing indexes"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                unique_together = [
                 ('char_field1', 'char_field2')]

        self.set_base_model(UniqueTogetherBaseModel)
        self.database_sig['tests_testmodel']['indexes'] = {}
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [
          ('char_field1', 'char_field2')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'unique_together', [('char_field1', 'char_field2')])"], 'ignore_missing_indexes', rescan_indexes=False)

    def test_upgrade_from_v1_sig_no_indexes(self):
        """Testing ChangeMeta(unique_together) and upgrade from v1 signature
        with no changes and no indexes in database"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                unique_together = [
                 ('int_field1', 'char_field1')]

        self.set_base_model(NoUniqueTogetherBaseModel)
        meta = self.start_sig['tests']['TestModel']['meta']
        del meta['__unique_together_applied']
        meta['unique_together'] = DestModel._meta.unique_together
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [
          ('int_field1', 'char_field1')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'unique_together', [('int_field1', 'char_field1')])"], 'upgrade_from_v1_sig', rescan_indexes=False)

    def test_upgrade_from_v1_sig_with_indexes(self):
        """Testing ChangeMeta(unique_together) and upgrade from v1 signature
        with no changes and with indexes in database"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                unique_together = [
                 ('int_field1', 'char_field1')]

        self.set_base_model(UniqueTogetherBaseModel)
        meta = self.start_sig['tests']['TestModel']['meta']
        del meta['__unique_together_applied']
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'unique_together', [
          ('int_field1', 'char_field1')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'unique_together', [('int_field1', 'char_field1')])"], None, rescan_indexes=False)
        return