# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/conditions/tests/test_conditions.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django import forms
from django.utils import six
from kgb import SpyAgency
from djblets.conditions.choices import BaseConditionChoice, ConditionChoices
from djblets.conditions.conditions import Condition, ConditionSet
from djblets.conditions.errors import ConditionChoiceNotFoundError, ConditionOperatorNotFoundError, InvalidConditionModeError, InvalidConditionValueError
from djblets.conditions.operators import BaseConditionOperator, ConditionOperators
from djblets.conditions.values import ConditionValueFormField
from djblets.testing.testcases import TestCase

class BasicTestOperator(BaseConditionOperator):
    operator_id = b'basic-test-op'


class BooleanTestOperator(BaseConditionOperator):
    operator_id = b'boolean-test-op'
    value_field = ConditionValueFormField(forms.BooleanField())


class NoValueTestOperator(BaseConditionOperator):
    operator_id = b'no-value-test-op'
    value_field = None


class EqualsTestOperator(BaseConditionOperator):
    operator_id = b'equals-test-op'

    def matches(self, match_value, condition_value):
        return match_value == condition_value


class BasicTestChoice(BaseConditionChoice):
    choice_id = b'basic-test-choice'
    operators = ConditionOperators([BasicTestOperator])
    default_value_field = ConditionValueFormField(forms.CharField())


class EqualsTestChoice(BaseConditionChoice):
    choice_id = b'equals-test-choice'
    operators = ConditionOperators([EqualsTestOperator])
    default_value_field = ConditionValueFormField(forms.CharField())


class ConditionTests(SpyAgency, TestCase):
    """Unit tests for djblets.conditions.conditions.Condition."""

    def test_deserialize(self):
        """Testing Condition.deserialize"""
        choices = ConditionChoices([BasicTestChoice])
        condition = Condition.deserialize(choices, {b'choice': b'basic-test-choice', 
           b'op': b'basic-test-op', 
           b'value': b'my-value'})
        self.assertEqual(condition.choice.__class__, BasicTestChoice)
        self.assertEqual(condition.operator.__class__, BasicTestOperator)
        self.assertEqual(condition.value, b'my-value')
        self.assertEqual(condition.raw_value, b'my-value')

    def test_deserialize_with_choice_kwargs(self):
        """Testing Condition.deserialize with choice_kwargs"""
        choices = ConditionChoices([BasicTestChoice])
        condition = Condition.deserialize(choices, {b'choice': b'basic-test-choice', 
           b'op': b'basic-test-op', 
           b'value': b'my-value'}, choice_kwargs={b'abc': 123})
        self.assertEqual(condition.choice.__class__, BasicTestChoice)
        self.assertEqual(condition.choice.extra_state, {b'abc': 123})
        self.assertEqual(condition.operator.__class__, BasicTestOperator)
        self.assertEqual(condition.value, b'my-value')
        self.assertEqual(condition.raw_value, b'my-value')

    def test_deserialize_with_op_value_field(self):
        """Testing Condition.deserialize with operator's value_field"""

        class MyChoice(BaseConditionChoice):
            choice_id = b'my-choice'
            operators = ConditionOperators([BooleanTestOperator])
            default_value_field = ConditionValueFormField(forms.CharField())

        choices = ConditionChoices([MyChoice])
        condition = Condition.deserialize(choices, {b'choice': b'my-choice', 
           b'op': b'boolean-test-op', 
           b'value': True})
        self.assertEqual(condition.choice.__class__, MyChoice)
        self.assertEqual(condition.operator.__class__, BooleanTestOperator)
        self.assertEqual(condition.value, True)
        self.assertEqual(condition.raw_value, True)

    def test_deserialize_with_no_value_field(self):
        """Testing Condition.deserialize with no value_field"""

        class MyChoice(BaseConditionChoice):
            choice_id = b'my-choice'
            operators = ConditionOperators([NoValueTestOperator])
            default_value_field = ConditionValueFormField(forms.CharField())

        choices = ConditionChoices([MyChoice])
        condition = Condition.deserialize(choices, {b'choice': b'my-choice', 
           b'op': b'no-value-test-op', 
           b'value': True})
        self.assertEqual(condition.choice.__class__, MyChoice)
        self.assertEqual(condition.operator.__class__, NoValueTestOperator)
        self.assertEqual(condition.value, None)
        self.assertEqual(condition.raw_value, None)
        return

    def test_deserialize_with_missing_choice(self):
        """Testing Condition.deserialize with missing choice in data"""
        choices = ConditionChoices()
        with self.assertRaises(ConditionChoiceNotFoundError) as (cm):
            Condition.deserialize(choices, {b'op': b'my-op', 
               b'value': b'my-value'}, condition_index=1)
        e = cm.exception
        self.assertEqual(six.text_type(e), b'A choice is required.')
        self.assertEqual(e.condition_index, 1)

    def test_deserialize_with_missing_operator(self):
        """Testing Condition.deserialize with missing operator in data"""
        choices = ConditionChoices()
        with self.assertRaises(ConditionOperatorNotFoundError) as (cm):
            Condition.deserialize(choices, {b'choice': b'my-choice', 
               b'value': b'my-value'}, condition_index=1)
        e = cm.exception
        self.assertEqual(six.text_type(e), b'An operator is required.')
        self.assertEqual(e.condition_index, 1)

    def test_deserialize_with_missing_value(self):
        """Testing Condition.deserialize with missing value in data"""
        choices = ConditionChoices([BasicTestChoice])
        with self.assertRaises(InvalidConditionValueError) as (cm):
            Condition.deserialize(choices, {b'choice': b'basic-test-choice', 
               b'op': b'basic-test-op'}, condition_index=1)
        e = cm.exception
        self.assertEqual(six.text_type(e), b'A value is required.')
        self.assertEqual(e.condition_index, 1)

    def test_deserialize_with_invalid_choice(self):
        """Testing Condition.deserialize with invalid choice in data"""
        choices = ConditionChoices()
        with self.assertRaises(ConditionChoiceNotFoundError) as (cm):
            Condition.deserialize(choices, {b'choice': b'invalid-choice', 
               b'op': b'my-op', 
               b'value': b'my-value'}, condition_index=1)
        e = cm.exception
        self.assertEqual(six.text_type(e), b'No condition choice was found matching "invalid-choice".')
        self.assertEqual(e.choice_id, b'invalid-choice')
        self.assertEqual(e.condition_index, 1)

    def test_deserialize_with_invalid_operator(self):
        """Testing Condition.deserialize with invalid operator in data"""

        class MyChoice(BaseConditionChoice):
            choice_id = b'my-choice'
            operators = ConditionOperators()

        choices = ConditionChoices([MyChoice])
        with self.assertRaises(ConditionOperatorNotFoundError) as (cm):
            Condition.deserialize(choices, {b'choice': b'my-choice', 
               b'op': b'invalid-op', 
               b'value': b'my-value'}, condition_index=1)
        e = cm.exception
        self.assertEqual(six.text_type(e), b'No operator was found matching "invalid-op".')
        self.assertEqual(e.operator_id, b'invalid-op')
        self.assertEqual(e.condition_index, 1)

    def test_deserialize_with_invalid_value(self):
        """Testing Condition.deserialize with invalid value in data"""

        class MyChoice(BaseConditionChoice):
            choice_id = b'my-choice'
            operators = ConditionOperators([BasicTestOperator])
            default_value_field = ConditionValueFormField(forms.IntegerField())

        choices = ConditionChoices([MyChoice])
        with self.assertRaises(InvalidConditionValueError) as (cm):
            Condition.deserialize(choices, {b'choice': b'my-choice', 
               b'op': b'basic-test-op', 
               b'value': b'invalid-value'}, condition_index=1)
        e = cm.exception
        self.assertEqual(six.text_type(e), b'Enter a whole number.')
        self.assertEqual(e.code, b'invalid')
        self.assertEqual(e.condition_index, 1)

    def test_serialize(self):
        """Testing Condition.serialize"""

        class MyChoice(BaseConditionChoice):
            choice_id = b'my-choice'
            operators = ConditionOperators([BasicTestOperator])
            default_value_field = ConditionValueFormField(forms.IntegerField())

        choice = MyChoice()
        condition = Condition(choice, choice.get_operator(b'basic-test-op'), 123)
        self.assertEqual(condition.serialize(), {b'choice': b'my-choice', 
           b'op': b'basic-test-op', 
           b'value': 123})

    def test_serialize_without_value_field(self):
        """Testing Condition.serialize without a value_field"""

        class MyChoice(BaseConditionChoice):
            choice_id = b'my-choice'
            operators = ConditionOperators([BasicTestOperator])

        choice = MyChoice()
        condition = Condition(choice, choice.get_operator(b'basic-test-op'))
        self.assertEqual(condition.serialize(), {b'choice': b'my-choice', 
           b'op': b'basic-test-op'})

    def test_matches_with_match(self):
        """Testing Condition.matches with match"""
        choice = EqualsTestChoice()
        condition = Condition(choice, choice.get_operator(b'equals-test-op'), b'abc123')
        self.assertTrue(condition.matches(b'abc123'))

    def test_matches_with_no_match(self):
        """Testing Condition.matches with no match"""
        choice = EqualsTestChoice()
        condition = Condition(choice, choice.get_operator(b'equals-test-op'), b'abc123')
        self.assertFalse(condition.matches(b'def123'))


class ConditionSetTests(TestCase):
    """Unit tests for djblets.conditions.conditions.ConditionSet."""

    def test_deserialize(self):
        """Testing ConditionSet.deserialize"""
        choices = ConditionChoices([BasicTestChoice])
        condition_set = ConditionSet.deserialize(choices, {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'basic-test-choice', 
                            b'op': b'basic-test-op', 
                            b'value': b'my-value'}]})
        self.assertEqual(condition_set.mode, ConditionSet.MODE_ANY)
        self.assertEqual(len(condition_set.conditions), 1)
        self.assertEqual(condition_set.conditions[0].choice.choice_id, b'basic-test-choice')

    def test_deserialize_with_choice_kwargs(self):
        """Testing ConditionSet.deserialize with choice_kwargs"""
        choices = ConditionChoices([BasicTestChoice])
        condition_set = ConditionSet.deserialize(choices, {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'basic-test-choice', 
                            b'op': b'basic-test-op', 
                            b'value': b'my-value'}]}, choice_kwargs={b'abc': 123})
        self.assertEqual(condition_set.mode, ConditionSet.MODE_ANY)
        self.assertEqual(len(condition_set.conditions), 1)
        choice = condition_set.conditions[0].choice
        self.assertEqual(choice.choice_id, b'basic-test-choice')
        self.assertEqual(choice.extra_state, {b'abc': 123})

    def test_deserialize_with_invalid_mode(self):
        """Testing ConditionSet.deserialize with invalid mode"""
        choices = ConditionChoices([BasicTestChoice])
        with self.assertRaises(InvalidConditionModeError):
            ConditionSet.deserialize(choices, {b'mode': b'invalid', 
               b'conditions': [
                             {b'choice': b'basic-test-choice', 
                                b'op': b'basic-test-op', 
                                b'value': b'my-value'}]})

    def test_matches_with_always_mode(self):
        """Testing ConditionSet.matches with "always" mode"""
        condition_set = ConditionSet(ConditionSet.MODE_ALWAYS, [])
        self.assertTrue(condition_set.matches(value=b'abc123'))

    def test_matches_with_all_mode_and_match(self):
        """Testing ConditionSet.matches with "all" mode and match"""
        choice = EqualsTestChoice()
        condition_set = ConditionSet(ConditionSet.MODE_ALL, [
         Condition(choice, choice.get_operator(b'equals-test-op'), b'abc123'),
         Condition(choice, choice.get_operator(b'equals-test-op'), b'abc123')])
        self.assertTrue(condition_set.matches(value=b'abc123'))

    def test_matches_with_all_mode_and_no_match(self):
        """Testing ConditionSet.matches with "all" mode and no match"""
        choice = EqualsTestChoice()
        condition_set = ConditionSet(ConditionSet.MODE_ALL, [
         Condition(choice, choice.get_operator(b'equals-test-op'), b'abc123'),
         Condition(choice, choice.get_operator(b'equals-test-op'), b'def123')])
        self.assertFalse(condition_set.matches(value=b'abc123'))

    def test_matches_with_any_mode_and_match(self):
        """Testing ConditionSet.matches with "any" mode and match"""
        choice = EqualsTestChoice()
        condition_set = ConditionSet(ConditionSet.MODE_ANY, [
         Condition(choice, choice.get_operator(b'equals-test-op'), b'abc123'),
         Condition(choice, choice.get_operator(b'equals-test-op'), b'def123')])
        self.assertTrue(condition_set.matches(value=b'abc123'))

    def test_matches_with_any_mode_and_no_match(self):
        """Testing ConditionSet.matches with "any" mode and no match"""
        choice = EqualsTestChoice()
        condition_set = ConditionSet(ConditionSet.MODE_ANY, [
         Condition(choice, choice.get_operator(b'equals-test-op'), b'abc123'),
         Condition(choice, choice.get_operator(b'equals-test-op'), b'def123')])
        self.assertFalse(condition_set.matches(value=b'foo'))

    def test_matches_with_custom_value_kwargs(self):
        """Testing ConditionSet.matches with custom value keyword arguments"""

        class CustomEqualsChoice(EqualsTestChoice):
            value_kwarg = b'my_value'

        choice = CustomEqualsChoice()
        condition_set = ConditionSet(ConditionSet.MODE_ALL, [
         Condition(choice, choice.get_operator(b'equals-test-op'), b'abc123')])
        self.assertTrue(condition_set.matches(my_value=b'abc123'))
        self.assertFalse(condition_set.matches(value=b'abc123'))

    def test_matches_with_all_mode_and_custom_value_kwargs_multiple(self):
        """Testing ConditionSet.matches with "all" mode and multiple custom
        value keyword arguments across multiple choices
        """

        class CustomEqualsChoice1(EqualsTestChoice):
            value_kwarg = b'my_value1'

        class CustomEqualsChoice2(EqualsTestChoice):
            value_kwarg = b'my_value2'

        choice1 = CustomEqualsChoice1()
        choice2 = CustomEqualsChoice2()
        condition_set = ConditionSet(ConditionSet.MODE_ALL, [
         Condition(choice1, choice1.get_operator(b'equals-test-op'), b'abc123'),
         Condition(choice2, choice2.get_operator(b'equals-test-op'), b'def456')])
        self.assertTrue(condition_set.matches(my_value1=b'abc123', my_value2=b'def456'))
        self.assertFalse(condition_set.matches(my_value1=b'abc123'))
        self.assertFalse(condition_set.matches(my_value2=b'def456'))
        self.assertFalse(condition_set.matches(my_value1=b'abc123', my_value2=b'xxx'))

    def test_matches_with_any_mode_and_custom_value_kwargs_multiple(self):
        """Testing ConditionSet.matches with "any" mode and multiple custom
        value keyword arguments across multiple choices
        """

        class CustomEqualsChoice1(EqualsTestChoice):
            value_kwarg = b'my_value1'

        class CustomEqualsChoice2(EqualsTestChoice):
            value_kwarg = b'my_value2'

        choice1 = CustomEqualsChoice1()
        choice2 = CustomEqualsChoice2()
        condition_set = ConditionSet(ConditionSet.MODE_ANY, [
         Condition(choice1, choice1.get_operator(b'equals-test-op'), b'abc123'),
         Condition(choice2, choice2.get_operator(b'equals-test-op'), b'def456')])
        self.assertTrue(condition_set.matches(my_value1=b'abc123', my_value2=b'def456'))
        self.assertTrue(condition_set.matches(my_value1=b'abc123'))
        self.assertTrue(condition_set.matches(my_value2=b'def456'))
        self.assertTrue(condition_set.matches(my_value1=b'abc123', my_value2=b'xxx'))
        self.assertFalse(condition_set.matches(my_value1=b'xxx', my_value2=b'xxx'))

    def test_serialize(self):
        """Testing ConditionSet.serialize"""
        basic_choice = BasicTestChoice()
        equals_choice = EqualsTestChoice()
        condition_set = ConditionSet(ConditionSet.MODE_ALL, [
         Condition(basic_choice, basic_choice.get_operator(b'basic-test-op'), b'abc123'),
         Condition(equals_choice, equals_choice.get_operator(b'equals-test-op'), b'def123')])
        result = condition_set.serialize()
        self.assertEqual(result, {b'mode': b'all', 
           b'conditions': [
                         {b'choice': b'basic-test-choice', 
                            b'op': b'basic-test-op', 
                            b'value': b'abc123'},
                         {b'choice': b'equals-test-choice', 
                            b'op': b'equals-test-op', 
                            b'value': b'def123'}]})