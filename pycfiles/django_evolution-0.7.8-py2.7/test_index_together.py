# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/django_evolution/tests/test_index_together.py
# Compiled at: 2018-06-14 23:17:51
from django.db import models
from django.utils.unittest import SkipTest
from django_evolution.mutations import ChangeMeta
from django_evolution.tests.base_test_case import EvolutionTestCase
from django_evolution.support import supports_index_together
if not supports_index_together:
    raise SkipTest('index_together is not supported on this version of Django')

class NoIndexTogetherBaseModel(models.Model):
    int_field1 = models.IntegerField()
    int_field2 = models.IntegerField()
    char_field1 = models.CharField(max_length=20)
    char_field2 = models.CharField(max_length=40)


class IndexTogetherBaseModel(models.Model):
    int_field1 = models.IntegerField()
    int_field2 = models.IntegerField()
    char_field1 = models.CharField(max_length=20)
    char_field2 = models.CharField(max_length=40)

    class Meta:
        index_together = [
         ('int_field1', 'char_field1')]


class IndexTogetherTests(EvolutionTestCase):
    """Testing ChangeMeta with adding index_together"""
    sql_mapping_key = 'index_together'
    DIFF_TEXT = "In model tests.TestModel:\n    Meta property 'index_together' has changed"

    def test_keeping_empty(self):
        """Testing ChangeMeta(index_together) and keeping list empty"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                index_together = []

        self.set_base_model(NoIndexTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'index_together', [])], None, None, None, expect_noop=True)
        return

    def test_setting_from_empty(self):
        """Testing ChangeMeta(index_together) and setting to valid list"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                index_together = [
                 ('int_field1', 'char_field1')]

        self.set_base_model(NoIndexTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'index_together', [
          ('int_field1', 'char_field1')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'index_together', [('int_field1', 'char_field1')])"], 'setting_from_empty')

    def test_replace_list(self):
        """Testing ChangeMeta(index_together) and replacing list"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                index_together = [
                 ('int_field2', 'char_field2')]

        self.set_base_model(IndexTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'index_together', [
          ('int_field2', 'char_field2')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'index_together', [('int_field2', 'char_field2')])"], 'replace_list')

    def test_append_list(self):
        """Testing ChangeMeta(index_together) and appending list"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                index_together = [
                 ('int_field1', 'char_field1'),
                 ('int_field2', 'char_field2')]

        self.set_base_model(IndexTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'index_together', [
          ('int_field1', 'char_field1'),
          ('int_field2', 'char_field2')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'index_together', [('int_field1', 'char_field1'), ('int_field2', 'char_field2')])"], 'append_list')

    def test_removing(self):
        """Testing ChangeMeta(index_together) and removing property"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

        self.set_base_model(IndexTogetherBaseModel)
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'index_together', [])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'index_together', [])"], 'removing')

    def test_missing_indexes(self):
        """Testing ChangeMeta(index_together) and old missing indexes"""

        class DestModel(models.Model):
            int_field1 = models.IntegerField()
            int_field2 = models.IntegerField()
            char_field1 = models.CharField(max_length=20)
            char_field2 = models.CharField(max_length=40)

            class Meta:
                index_together = [
                 ('char_field1', 'char_field2')]

        self.set_base_model(IndexTogetherBaseModel)
        self.database_sig['tests_testmodel']['indexes'] = {}
        self.perform_evolution_tests(DestModel, [
         ChangeMeta('TestModel', 'index_together', [
          ('char_field1', 'char_field2')])], self.DIFF_TEXT, [
         "ChangeMeta('TestModel', 'index_together', [('char_field1', 'char_field2')])"], 'ignore_missing_indexes', rescan_indexes=False)