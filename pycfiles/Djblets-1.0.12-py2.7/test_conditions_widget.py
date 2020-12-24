# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/forms/tests/test_conditions_widget.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import copy
from django.utils import six
from django.utils.datastructures import MultiValueDict
from djblets.conditions.choices import BaseConditionChoice, BaseConditionIntegerChoice, ConditionChoices
from djblets.conditions.operators import BaseConditionOperator, ConditionOperators
from djblets.conditions.values import ConditionValueCharField, ConditionValueIntegerField
from djblets.forms.fields import ConditionsField
from djblets.testing.testcases import TestCase

class ConditionsWidgetTests(TestCase):
    """Unit tests for djblets.forms.widgets.ConditionsWidget."""

    def test_deepcopy(self):
        """Testing ConditionsWidget.__deepcopy__"""

        class MyChoice(BaseConditionIntegerChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        widget1 = field.widget
        widget2 = copy.deepcopy(widget1)
        widget1.mode_widget.attrs[b'foo'] = True
        widget1.choice_widget.attrs[b'foo'] = True
        widget1.operator_widget.attrs[b'foo'] = True
        widget1.condition_errors[0] = b'This is a test.'
        self.assertEqual(widget2.mode_widget.attrs, {})
        self.assertEqual(widget2.choice_widget.attrs, {})
        self.assertEqual(widget2.operator_widget.attrs, {})
        self.assertEqual(widget2.condition_errors, {})
        self.assertIs(widget1.choices, widget2.choices)

    def test_value_from_datadict(self):
        """Testing ConditionsWidget.value_from_datadict"""

        class MyChoice(BaseConditionIntegerChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        data = MultiValueDict(b'')
        data.update({b'my_conditions_mode': b'any', 
           b'my_conditions_last_id': b'1', 
           b'my_conditions_choice[0]': b'my-choice', 
           b'my_conditions_operator[0]': b'is', 
           b'my_conditions_value[0]': b'my-value-1', 
           b'my_conditions_choice[1]': b'my-choice', 
           b'my_conditions_operator[1]': b'is-not', 
           b'my_conditions_value[1]': b'my-value-2'})
        self.assertEqual(field.widget.value_from_datadict(data, MultiValueDict(b''), b'my_conditions'), {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'my-choice', 
                            b'op': b'is', 
                            b'value': b'my-value-1'},
                         {b'choice': b'my-choice', 
                            b'op': b'is-not', 
                            b'value': b'my-value-2'}]})

    def test_value_from_datadict_with_missing_data(self):
        """Testing ConditionsWidget.value_from_datadict with missing data"""

        class MyChoice(BaseConditionIntegerChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        data = MultiValueDict(b'')
        self.assertEqual(field.widget.value_from_datadict(data, MultiValueDict(b''), b'my_conditions'), {b'mode': None, 
           b'conditions': []})
        return

    def test_value_from_datadict_with_missing_last_id(self):
        """Testing ConditionsWidget.value_from_datadict with missing last_id"""

        class MyChoice(BaseConditionIntegerChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        data = MultiValueDict(b'')
        data.update({b'my_conditions_mode': b'any', 
           b'my_conditions_choice[0]': b'my-choice', 
           b'my_conditions_operator[0]': b'is', 
           b'my_conditions_value[0]': b'my-value-1', 
           b'my_conditions_choice[1]': b'my-choice', 
           b'my_conditions_operator[1]': b'is-not', 
           b'my_conditions_value[1]': b'my-value-2'})
        self.assertEqual(field.widget.value_from_datadict(data, MultiValueDict(b''), b'my_conditions'), {b'mode': b'any', 
           b'conditions': []})

    def test_value_from_datadict_with_missing_choice_rows(self):
        """Testing ConditionsWidget.value_from_datadict with missing choice
        rows
        """

        class MyChoice(BaseConditionIntegerChoice):
            choice_id = b'my-choice'

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        data = MultiValueDict(b'')
        data.update({b'my_conditions_mode': b'any', 
           b'my_conditions_last_id': b'5', 
           b'my_conditions_choice[5]': b'my-choice', 
           b'my_conditions_operator[5]': b'is-not', 
           b'my_conditions_value[5]': b'my-value'})
        self.assertEqual(field.widget.value_from_datadict(data, MultiValueDict(b''), b'my_conditions'), {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'my-choice', 
                            b'op': b'is-not', 
                            b'value': b'my-value'}]})

    def test_get_context(self):
        """Testing ConditionsWidget.get_context"""

        class MyOperator1(BaseConditionOperator):
            operator_id = b'my-op-1'
            name = b'My Op 1'
            value_field = ConditionValueIntegerField()

        class MyOperator2(BaseConditionOperator):
            operator_id = b'my-op-2'
            name = b'My Op 2'
            value_field = ConditionValueCharField()

        class MyOperator3(BaseConditionOperator):
            operator_id = b'my-op-3'
            name = b'My Op 3'

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice-1'
            name = b'My Choice 1'
            operators = ConditionOperators([MyOperator1, MyOperator2])

        class MyChoice2(BaseConditionChoice):
            choice_id = b'my-choice-2'
            name = b'My Choice 2'
            operators = ConditionOperators([MyOperator3])

        choices = ConditionChoices([MyChoice1, MyChoice2])
        field = ConditionsField(choices=choices)
        result = field.widget.get_context(b'my_conditions', {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'my-choice-1', 
                            b'op': b'my-op-1', 
                            b'value': b'my-value-1'},
                         {b'choice': b'my-choice-2', 
                            b'op': b'my-op-3'}]}, {b'id': b'my-conditions'})
        self.assertEqual(set(result), {
         b'field_id', b'field_name', b'rendered_mode', b'rendered_rows',
         b'serialized_choices', b'serialized_rows'})
        self.assertEqual(result[b'field_id'], b'my-conditions')
        self.assertEqual(result[b'field_name'], b'my_conditions')
        self.assertHTMLEqual(result[b'rendered_mode'], b'<ul id="my_conditions_mode">\n<li><label for="my_conditions_mode_0"><input id="my_conditions_mode_0" name="my_conditions_mode" type="radio" value="always" /> Always match</label></li>\n<li><label for="my_conditions_mode_1"><input id="my_conditions_mode_1" name="my_conditions_mode" type="radio" value="all" /> Match <b>all</b> of the following:</label></li>\n<li><label for="my_conditions_mode_2"><input checked="checked" id="my_conditions_mode_2" name="my_conditions_mode" type="radio" value="any" /> Match <b>any</b> of the following:</label></li>\n</ul>')
        rendered_rows = result[b'rendered_rows']
        self.assertEqual(len(rendered_rows), 2)
        rendered_row = rendered_rows[0]
        self.assertEqual(set(six.iterkeys(rendered_row)), {
         b'choice', b'operator', b'error'})
        self.assertHTMLEqual(rendered_row[b'choice'], b'<select id="my-conditions_choice_0" name="my_conditions_choice[0]">\n<option value="my-choice-1" selected="selected">My Choice 1</option>\n<option value="my-choice-2">My Choice 2</option>\n</select>')
        self.assertHTMLEqual(rendered_row[b'operator'], b'<select id="my-conditions_operator_0" name="my_conditions_operator[0]">\n<option value="my-op-1" selected="selected">My Op 1</option>\n<option value="my-op-2">My Op 2</option>\n</select>')
        self.assertIsNone(rendered_row[b'error'])
        rendered_row = rendered_rows[1]
        self.assertEqual(set(six.iterkeys(rendered_row)), {
         b'choice', b'operator', b'error'})
        self.assertHTMLEqual(rendered_row[b'choice'], b'<select id="my-conditions_choice_1" name="my_conditions_choice[1]">\n<option value="my-choice-1">My Choice 1</option>\n<option value="my-choice-2" selected="selected">My Choice 2</option>\n</select>')
        self.assertHTMLEqual(rendered_row[b'operator'], b'<select id="my-conditions_operator_1" name="my_conditions_operator[1]">\n<option value="my-op-3" selected="selected">My Op 3</option>\n</select>')
        self.assertIsNone(rendered_row[b'error'])
        serialized_choices = result[b'serialized_choices']
        self.assertEqual(len(serialized_choices), 2)
        serialized_choice = serialized_choices[0]
        self.assertEqual(set(six.iterkeys(serialized_choice)), {
         b'id', b'name', b'valueField', b'operators'})
        self.assertEqual(serialized_choice[b'id'], b'my-choice-1')
        self.assertEqual(serialized_choice[b'name'], b'My Choice 1')
        self.assertEqual(serialized_choice[b'valueField'], {})
        self.assertEqual(serialized_choice[b'valueField'], {})
        serialized_operators = serialized_choice[b'operators']
        self.assertEqual(len(serialized_operators), 2)
        serialized_operator = serialized_operators[0]
        self.assertEqual(set(six.iterkeys(serialized_operator)), {
         b'id', b'name', b'useValue', b'valueField'})
        self.assertEqual(serialized_operator[b'id'], b'my-op-1')
        self.assertEqual(serialized_operator[b'name'], b'My Op 1')
        self.assertTrue(serialized_operator[b'useValue'])
        serialized_value_field = serialized_operator[b'valueField']
        self.assertEqual(set(six.iterkeys(serialized_value_field)), {
         b'model', b'view'})
        serialized_value_model = serialized_value_field[b'model']
        self.assertEqual(serialized_value_model[b'className'], b'Djblets.Forms.ConditionValueField')
        self.assertHTMLEqual(serialized_value_model[b'data'][b'fieldHTML'], b'<input name="XXX" type="number" />')
        serialized_value_view = serialized_value_field[b'view']
        self.assertEqual(serialized_value_view[b'className'], b'Djblets.Forms.ConditionValueFormFieldView')
        self.assertEqual(serialized_value_view[b'data'], {})
        serialized_operator = serialized_operators[1]
        self.assertEqual(set(six.iterkeys(serialized_operator)), {
         b'id', b'name', b'useValue', b'valueField'})
        self.assertEqual(serialized_operator[b'id'], b'my-op-2')
        self.assertEqual(serialized_operator[b'name'], b'My Op 2')
        self.assertTrue(serialized_operator[b'useValue'])
        serialized_value_field = serialized_operator[b'valueField']
        self.assertEqual(set(six.iterkeys(serialized_value_field)), {
         b'model', b'view'})
        serialized_value_model = serialized_value_field[b'model']
        self.assertEqual(serialized_value_model[b'className'], b'Djblets.Forms.ConditionValueField')
        self.assertHTMLEqual(serialized_value_model[b'data'][b'fieldHTML'], b'<input name="XXX" type="text" />')
        serialized_value_view = serialized_value_field[b'view']
        self.assertEqual(serialized_value_view[b'className'], b'Djblets.Forms.ConditionValueFormFieldView')
        self.assertEqual(serialized_value_view[b'data'], {})
        self.assertEqual(serialized_choices[1], {b'id': b'my-choice-2', 
           b'name': b'My Choice 2', 
           b'operators': [
                        {b'id': b'my-op-3', 
                           b'name': b'My Op 3', 
                           b'useValue': False}], 
           b'valueField': {}})
        serialized_rows = result[b'serialized_rows']
        self.assertEqual(len(serialized_rows), 2)
        self.assertEqual(serialized_rows[0], {b'choiceID': b'my-choice-1', 
           b'operatorID': b'my-op-1', 
           b'valid': True, 
           b'value': b'my-value-1'})
        self.assertEqual(serialized_rows[1], {b'choiceID': b'my-choice-2', 
           b'operatorID': b'my-op-3', 
           b'valid': True, 
           b'value': None})
        return

    def test_get_context_with_invalid_choice(self):
        """Testing ConditionsWidget.get_context with invalid choice"""

        class MyOperator1(BaseConditionOperator):
            operator_id = b'my-op-1'
            name = b'My Op 1'
            value_field = ConditionValueIntegerField()

        class MyOperator2(BaseConditionOperator):
            operator_id = b'my-op-2'
            name = b'My Op 2'
            value_field = ConditionValueCharField()

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice-1'
            name = b'My Choice 1'
            operators = ConditionOperators([MyOperator1, MyOperator2])

        choices = ConditionChoices([MyChoice1])
        field = ConditionsField(choices=choices)
        result = field.widget.get_context(b'my_conditions', {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'invalid-choice', 
                            b'op': b'my-op-1', 
                            b'value': b'my-value-1'}]}, {b'id': b'my-conditions'})
        rendered_rows = result[b'rendered_rows']
        self.assertEqual(len(rendered_rows), 1)
        rendered_row = rendered_rows[0]
        self.assertEqual(set(six.iterkeys(rendered_row)), {
         b'choice', b'operator', b'error'})
        self.assertHTMLEqual(rendered_row[b'choice'], b'<select disabled="disabled" id="my-conditions_choice_0" name="my_conditions_choice[0]">\n<option value="my-choice-1">My Choice 1</option>\n<option value="invalid-choice" selected="selected">invalid-choice</option>\n</select><input name="my_conditions_choice[0]" type="hidden" value="invalid-choice" />')
        self.assertHTMLEqual(rendered_row[b'operator'], b'<select disabled="disabled" id="my-conditions_operator_0" name="my_conditions_operator[0]">\n<option value="my-op-1" selected="selected">my-op-1</option>\n</select><input name="my_conditions_operator[0]" type="hidden" value="my-op-1" />')
        self.assertEqual(rendered_row[b'error'], b'This choice no longer exists. You will need to delete the condition in order to make changes.')
        serialized_choices = result[b'serialized_choices']
        self.assertEqual(len(serialized_choices), 1)
        self.assertEqual(serialized_choices[0][b'id'], b'my-choice-1')
        serialized_rows = result[b'serialized_rows']
        self.assertEqual(serialized_rows, [
         {b'choiceID': b'invalid-choice', 
            b'operatorID': b'my-op-1', 
            b'valid': False, 
            b'value': b'my-value-1', 
            b'error': b'This choice no longer exists. You will need to delete the condition in order to make changes.'}])

    def test_get_context_with_invalid_operator(self):
        """Testing ConditionsWidget.get_context with invalid operator"""

        class MyOperator1(BaseConditionOperator):
            operator_id = b'my-op-1'
            name = b'My Op 1'
            value_field = ConditionValueIntegerField()

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice'
            name = b'My Choice'
            operators = ConditionOperators([MyOperator1])

        choices = ConditionChoices([MyChoice1])
        field = ConditionsField(choices=choices)
        result = field.widget.get_context(b'my_conditions', {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'my-choice', 
                            b'op': b'invalid-op', 
                            b'value': b'my-value-1'}]}, {b'id': b'my-conditions'})
        rendered_rows = result[b'rendered_rows']
        self.assertEqual(len(rendered_rows), 1)
        rendered_row = rendered_rows[0]
        self.assertEqual(set(six.iterkeys(rendered_row)), {
         b'choice', b'operator', b'error'})
        self.assertHTMLEqual(rendered_row[b'choice'], b'<select disabled="disabled" id="my-conditions_choice_0" name="my_conditions_choice[0]">\n<option value="my-choice" selected="selected">My Choice</option>\n</select><input name="my_conditions_choice[0]" type="hidden" value="my-choice" />')
        self.assertHTMLEqual(rendered_row[b'operator'], b'<select disabled="disabled" id="my-conditions_operator_0" name="my_conditions_operator[0]">\n<option value="invalid-op" selected="selected">invalid-op</option>\n</select><input name="my_conditions_operator[0]" type="hidden" value="invalid-op" />')
        self.assertEqual(rendered_row[b'error'], b'This operator no longer exists. You will need to delete the condition in order to make changes.')
        serialized_choices = result[b'serialized_choices']
        self.assertEqual(len(serialized_choices), 1)
        self.assertEqual(serialized_choices[0][b'id'], b'my-choice')
        serialized_rows = result[b'serialized_rows']
        self.assertEqual(serialized_rows, [
         {b'choiceID': b'my-choice', 
            b'operatorID': b'invalid-op', 
            b'valid': False, 
            b'value': b'my-value-1', 
            b'error': b'This operator no longer exists. You will need to delete the condition in order to make changes.'}])

    def test_get_context_with_condition_errors(self):
        """Testing ConditionsWidget.get_context with condition errors"""

        class MyOperator1(BaseConditionOperator):
            operator_id = b'my-op-1'
            name = b'My Op 1'
            value_field = ConditionValueIntegerField()

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice'
            name = b'My Choice'
            operators = ConditionOperators([MyOperator1])

        choices = ConditionChoices([MyChoice1])
        field = ConditionsField(choices=choices)
        field.widget.condition_errors[0] = b'This is an error.'
        result = field.widget.get_context(b'my_conditions', {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'my-choice', 
                            b'op': b'my-op-1', 
                            b'value': b'my-value-1'}]}, {b'id': b'my-conditions'})
        rendered_rows = result[b'rendered_rows']
        self.assertEqual(len(rendered_rows), 1)
        rendered_row = rendered_rows[0]
        self.assertEqual(set(six.iterkeys(rendered_row)), {
         b'choice', b'operator', b'error'})
        self.assertHTMLEqual(rendered_row[b'choice'], b'<select id="my-conditions_choice_0" name="my_conditions_choice[0]">\n<option value="my-choice" selected="selected">My Choice</option>\n</select>')
        self.assertHTMLEqual(rendered_row[b'operator'], b'<select id="my-conditions_operator_0" name="my_conditions_operator[0]">\n<option value="my-op-1" selected="selected">My Op 1</option>\n</select>')
        self.assertEqual(rendered_row[b'error'], b'This is an error.')
        serialized_choices = result[b'serialized_choices']
        self.assertEqual(len(serialized_choices), 1)
        self.assertEqual(serialized_choices[0][b'id'], b'my-choice')
        serialized_rows = result[b'serialized_rows']
        self.assertEqual(serialized_rows, [
         {b'choiceID': b'my-choice', 
            b'operatorID': b'my-op-1', 
            b'valid': True, 
            b'value': b'my-value-1', 
            b'error': b'This is an error.'}])

    def test_render(self):
        """Testing ConditionsWidget.render"""

        class MyOperator(BaseConditionOperator):
            operator_id = b'my-op'
            name = b'My Op'
            value_field = ConditionValueIntegerField()

        class MyChoice(BaseConditionChoice):
            choice_id = b'my-choice'
            name = b'My Choice'
            operators = ConditionOperators([MyOperator])

        choices = ConditionChoices([MyChoice])
        field = ConditionsField(choices=choices)
        rendered = field.widget.render(b'my_conditions', {b'mode': b'any', 
           b'conditions': [
                         {b'choice': b'my-choice', 
                            b'op': b'my-op', 
                            b'value': b'my-value-1'}]}, {b'id': b'my-conditions'})
        self.assertIn(b'<div class="conditions-field" id="my-conditions">', rendered)
        self.assertIn(b'<input type="hidden" name="my_conditions_last_id" value="1">', rendered)
        self.assertRegexpMatches(rendered, b'<option value="my-choice" selected(="selected")?>My Choice</option>')
        self.assertRegexpMatches(rendered, b'<option value="my-op" selected(="selected")?>My Op</option>')
        self.assertIn(b'<span class="conditions-field-value"></span>', rendered)