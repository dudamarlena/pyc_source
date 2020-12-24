# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/integrations/tests/test_configs.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging
from djblets.conditions import ConditionSet
from djblets.forms.fields import ConditionsField
from djblets.testing.decorators import add_fixtures
from kgb import SpyAgency
from reviewboard.integrations.forms import IntegrationConfigForm
from reviewboard.integrations.models import IntegrationConfig
from reviewboard.reviews.conditions import ReviewRequestConditionChoices
from reviewboard.testing.testcase import TestCase

class MyConfigForm(IntegrationConfigForm):
    my_conditions = ConditionsField(choices=ReviewRequestConditionChoices)


class IntegrationConfigTests(SpyAgency, TestCase):
    """Unit tests for reviewboard.integrations.models.IntegrationConfig."""

    def test_load_conditions(self):
        """Testing IntegrationConfig.load_conditions"""
        config = IntegrationConfig()
        config.settings[b'my_conditions'] = {b'mode': b'all', 
           b'conditions': [
                         {b'choice': b'branch', 
                            b'op': b'is', 
                            b'value': b'master'},
                         {b'choice': b'summary', 
                            b'op': b'contains', 
                            b'value': b'[WIP]'}]}
        condition_set = config.load_conditions(MyConfigForm, conditions_key=b'my_conditions')
        self.assertEqual(condition_set.mode, ConditionSet.MODE_ALL)
        conditions = condition_set.conditions
        self.assertEqual(len(conditions), 2)
        condition = conditions[0]
        self.assertEqual(condition.choice.choice_id, b'branch')
        self.assertEqual(condition.operator.operator_id, b'is')
        self.assertEqual(condition.value, b'master')
        condition = conditions[1]
        self.assertEqual(condition.choice.choice_id, b'summary')
        self.assertEqual(condition.operator.operator_id, b'contains')
        self.assertEqual(condition.value, b'[WIP]')

    def test_load_conditions_with_empty(self):
        """Testing IntegrationConfig.load_conditions with empty or missing
        data
        """
        config = IntegrationConfig()
        config.settings[b'conditions'] = None
        self.assertIsNone(config.load_conditions(MyConfigForm))
        return

    def test_load_conditions_with_bad_data(self):
        """Testing IntegrationConfig.load_conditions with bad data"""
        config = IntegrationConfig()
        config.settings[b'conditions'] = b'dfsafas'
        self.spy_on(logging.debug)
        self.spy_on(logging.exception)
        self.assertIsNone(config.load_conditions(MyConfigForm))
        self.assertTrue(logging.debug.spy.called)
        self.assertTrue(logging.exception.spy.called)

    @add_fixtures([b'test_users'])
    def test_match_conditions(self):
        """Testing IntegrationConfig.match_conditions"""
        config = IntegrationConfig()
        config.settings[b'my_conditions'] = {b'mode': b'all', 
           b'conditions': [
                         {b'choice': b'branch', 
                            b'op': b'is', 
                            b'value': b'master'},
                         {b'choice': b'summary', 
                            b'op': b'contains', 
                            b'value': b'[WIP]'}]}
        review_request = self.create_review_request(branch=b'master', summary=b'[WIP] This is a test.')
        self.assertTrue(config.match_conditions(MyConfigForm, conditions_key=b'my_conditions', review_request=review_request))
        review_request = self.create_review_request(branch=b'master', summary=b'This is a test.')
        self.assertFalse(config.match_conditions(MyConfigForm, conditions_key=b'my_conditions', review_request=review_request))

    @add_fixtures([b'test_users'])
    def test_match_conditions_sandbox(self):
        """Testing IntegrationConfig.match_conditions with exceptions
        sandboxed
        """
        config = IntegrationConfig()
        config.settings[b'my_conditions'] = {b'mode': b'all', 
           b'conditions': [
                         {b'choice': b'branch', 
                            b'op': b'is', 
                            b'value': b'master'},
                         {b'choice': b'summary', 
                            b'op': b'contains', 
                            b'value': b'[WIP]'}]}
        self.create_review_request(branch=b'master', summary=b'[WIP] This is a test.')
        self.spy_on(logging.exception)
        self.assertFalse(config.match_conditions(MyConfigForm, conditions_key=b'my_conditions', review_request=b'test'))
        self.assertTrue(logging.exception.spy.called)