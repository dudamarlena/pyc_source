# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/forms/tests/test_conditions_field.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.forms import Form, ValidationError
from djblets.conditions.choices import BaseConditionChoice, BaseConditionIntegerChoice, BaseConditionStringChoice, ConditionChoices
from djblets.conditions.conditions import ConditionSet
from djblets.forms.fields import ConditionsField
from djblets.testing.testcases import TestCase

class ConditionsFieldTests(TestCase):
    """Unit tests for djblets.forms.fields.ConditionsField."""

    def test_init_with_choices_instance(self):
        """Testing ConditionsField initialization with choices instance"""
        choices = ConditionChoices([BaseConditionStringChoice])
        field = ConditionsField(choices=choices)
        self.assertIs(field.choices, choices)

    def test_init_with_choices_subclass(self):
        """Testing ConditionsField initialization with choices subclass"""

        class MyChoices(ConditionChoices):
            choice_classes = [
             BaseConditionStringChoice]

        field = ConditionsField(choices=MyChoices)
        self.assertIs(field.choices.__class__, MyChoices)

    def test_init_with_choice_kwargs(self):
        """Testing ConditionsField initialization with choice_kwargs"""
        choices = ConditionChoices([BaseConditionStringChoice])
        field = ConditionsField(choices=choices, choice_kwargs={b'abc': 123})
        self.assertEqual(field.widget.choice_kwargs, field.choice_kwargs)

    def test_init_with_missing_operators(self):
        """Testing ConditionsField initialization with choices missing
        operators
        """

        class MyChoice(BaseConditionChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        msg = b'MyChoice must define a non-empty "operators" attribute.'
        with self.assertRaisesMessage(ValueError, msg):
            ConditionsField(choices=choices)

    def test_choice_kwargs_with_multiple_instances(self):
        """Testing ConditionsField.choice_kwargs works with multiple instances
        """

        class MyForm(Form):
            conditions = ConditionsField(choices=ConditionChoices([BaseConditionStringChoice]))

        form1 = MyForm()
        form2 = MyForm()
        form1.fields[b'conditions'].choice_kwargs[b'a'] = 1
        self.assertNotIn(b'a', form2.fields[b'conditions'].choice_kwargs)

    def test_prepare_value_with_condition_set(self):
        """Testing ConditionsField.prepare_value with ConditionSet"""
        choices = ConditionChoices([BaseConditionStringChoice])
        field = ConditionsField(choices=choices)
        self.assertEqual(field.prepare_value(ConditionSet()), {b'mode': b'all', 
           b'conditions': []})

    def test_prepare_value_with_serialized_data(self):
        """Testing ConditionsField.prepare_value with serialized data"""
        choices = ConditionChoices([BaseConditionStringChoice])
        field = ConditionsField(choices=choices)
        data = {b'mode': b'all', 
           b'conditions': []}
        self.assertEqual(field.prepare_value(data), data)

    def test_to_python(self):
        """Testing ConditionsField.to_python"""

        class MyChoice(BaseConditionStringChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        condition_set = field.to_python({b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'my-choice', 
                            b'op': b'is', 
                            b'value': b'my-value'}]})
        self.assertEqual(condition_set.mode, ConditionSet.MODE_ANY)
        self.assertEqual(len(condition_set.conditions), 1)
        condition = condition_set.conditions[0]
        self.assertEqual(condition.choice.choice_id, b'my-choice')
        self.assertEqual(condition.operator.operator_id, b'is')
        self.assertEqual(condition.value, b'my-value')

    def test_to_python_with_choice_kwargs(self):
        """Testing ConditionsField.to_python with choice_kwargs set"""

        class MyChoice(BaseConditionStringChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices, choice_kwargs={b'abc': 123})
        condition_set = field.to_python({b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'my-choice', 
                            b'op': b'is', 
                            b'value': b'my-value'}]})
        self.assertEqual(condition_set.mode, ConditionSet.MODE_ANY)
        self.assertEqual(len(condition_set.conditions), 1)
        choice = condition_set.conditions[0].choice
        self.assertEqual(choice.choice_id, b'my-choice')
        self.assertEqual(choice.extra_state, {b'abc': 123})

    def test_to_python_with_mode_error(self):
        """Testing ConditionsField.to_python with mode error"""
        choices = ConditionChoices()
        field = ConditionsField(choices=choices)
        with self.assertRaises(ValidationError) as (cm):
            field.to_python({b'mode': b'invalid', 
               b'conditions': []})
        self.assertEqual(cm.exception.messages, [
         b'"invalid" is not a valid condition mode.'])
        self.assertEqual(cm.exception.code, b'invalid_mode')

    def test_to_python_with_choice_not_found_error(self):
        """Testing ConditionsField.to_python with choice not found error"""
        choices = ConditionChoices()
        field = ConditionsField(choices=choices)
        with self.assertRaises(ValidationError) as (cm):
            field.to_python({b'mode': b'any', 
               b'conditions': [
                             {b'choice': b'invalid-choice', 
                                b'op': b'is', 
                                b'value': b'my-value'}]})
        self.assertEqual(cm.exception.messages, [
         b'There was an error with one of your conditions.'])
        self.assertEqual(cm.exception.code, b'condition_errors')
        self.assertEqual(field.widget.condition_errors, {0: b'No condition choice was found matching "invalid-choice".'})

    def test_to_python_with_operator_not_found_error(self):
        """Testing ConditionsField.to_python with operator not found error"""

        class MyChoice(BaseConditionStringChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        with self.assertRaises(ValidationError) as (cm):
            field.to_python({b'mode': b'any', 
               b'conditions': [
                             {b'choice': b'my-choice', 
                                b'op': b'invalid-op', 
                                b'value': b'my-value'}]})
        self.assertEqual(cm.exception.messages, [
         b'There was an error with one of your conditions.'])
        self.assertEqual(cm.exception.code, b'condition_errors')
        self.assertEqual(field.widget.condition_errors, {0: b'No operator was found matching "invalid-op".'})

    def test_to_python_with_invalid_value_error(self):
        """Testing ConditionsField.to_python with invalid value error"""

        class MyChoice(BaseConditionIntegerChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        with self.assertRaises(ValidationError) as (cm):
            field.to_python({b'mode': b'any', 
               b'conditions': [
                             {b'choice': b'my-choice', 
                                b'op': b'is', 
                                b'value': b'invalid-value'}]})
        self.assertEqual(cm.exception.messages, [
         b'There was an error with one of your conditions.'])
        self.assertEqual(cm.exception.code, b'condition_errors')
        self.assertEqual(field.widget.condition_errors, {0: b'Enter a whole number.'})

    def test_to_python_with_value_required_error(self):
        """Testing ConditionsField.to_python with value required error"""

        class MyChoice(BaseConditionStringChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        with self.assertRaises(ValidationError) as (cm):
            field.to_python({b'mode': b'any', 
               b'conditions': [
                             {b'choice': b'my-choice', 
                                b'op': b'is'}]})
        self.assertEqual(cm.exception.messages, [
         b'There was an error with one of your conditions.'])
        self.assertEqual(cm.exception.code, b'condition_errors')
        self.assertEqual(field.widget.condition_errors, {0: b'A value is required.'})