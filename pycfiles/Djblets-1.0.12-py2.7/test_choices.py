# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/conditions/tests/test_choices.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from djblets.conditions.choices import BaseConditionChoice, BaseConditionStringChoice, ConditionChoiceMatchListItemsMixin, ConditionChoices
from djblets.conditions.errors import ConditionChoiceNotFoundError, ConditionOperatorNotFoundError
from djblets.conditions.operators import BaseConditionOperator, ConditionOperators
from djblets.testing.testcases import TestCase

class BaseConditionChoiceTests(TestCase):
    """Unit tests for djblets.conditions.choices.BaseConditionChoice."""

    def test_get_operator(self):
        """Testing BaseConditionChoice.get_operator"""

        class MyOperator(BaseConditionOperator):
            operator_id = b'my-op'

        class MyChoice(BaseConditionChoice):
            operators = ConditionOperators([
             MyOperator])

        choice = MyChoice()
        self.assertEqual(choice.get_operator(b'my-op').__class__, MyOperator)

    def test_get_operator_with_invalid_id(self):
        """Testing BaseConditionChoice.get_operator with invalid ID"""

        class MyChoice(BaseConditionChoice):
            operators = ConditionOperators()

        choice = MyChoice()
        with self.assertRaises(ConditionOperatorNotFoundError):
            choice.get_operator(b'invalid')

    def test_get_operators(self):
        """Testing BaseConditionChoice.get_operators"""

        class MyOperator1(BaseConditionOperator):
            operator_id = b'my-op-1'

        class MyOperator2(BaseConditionOperator):
            operator_id = b'my-op-2'

        class MyChoice(BaseConditionChoice):
            operators = ConditionOperators([
             MyOperator1,
             MyOperator2])

        choice = MyChoice()
        operators = list(choice.get_operators())
        self.assertEqual(len(operators), 2)
        self.assertEqual(operators[0].__class__, MyOperator1)
        self.assertEqual(operators[1].__class__, MyOperator2)


class ConditionChoiceMatchListItemsMixinTests(TestCase):
    """Unit tests for ConditionChoiceMatchListItemsMixin."""

    def test_matches_with_all_required_and_match(self):
        """Testing ConditionChoiceMatchListItemsMixin.matches with
        require_match_all_items=True and match
        """

        class MyChoice(ConditionChoiceMatchListItemsMixin, BaseConditionStringChoice):
            require_match_all_items = True

        choice = MyChoice()
        self.assertTrue(choice.matches(operator=choice.get_operator(b'contains'), match_value=[
         b'foo1', b'foo2', b'foo3'], condition_value=b'foo', value_state_cache={}))

    def test_matches_with_all_required_and_no_match(self):
        """Testing ConditionChoiceMatchListItemsMixin.matches with
        require_match_all_items=True and no match
        """

        class MyChoice(ConditionChoiceMatchListItemsMixin, BaseConditionStringChoice):
            require_match_all_items = True

        choice = MyChoice()
        self.assertFalse(choice.matches(operator=choice.get_operator(b'contains'), match_value=[
         b'foo1', b'foo2', b'bar1'], condition_value=b'foo', value_state_cache={}))

    def test_matches_with_any_required_and_match(self):
        """Testing ConditionChoiceMatchListItemsMixin.matches with
        require_match_all_items=False and match
        """

        class MyChoice(ConditionChoiceMatchListItemsMixin, BaseConditionStringChoice):
            require_match_all_items = False

        choice = MyChoice()
        self.assertTrue(choice.matches(operator=choice.get_operator(b'contains'), match_value=[
         b'foo1', b'foo2', b'bar1', b'bar2'], condition_value=b'foo', value_state_cache={}))

    def test_matches_with_any_required_and_no_match(self):
        """Testing ConditionChoiceMatchListItemsMixin.matches with
        require_match_all_items=False and no match
        """

        class MyChoice(ConditionChoiceMatchListItemsMixin, BaseConditionStringChoice):
            require_match_all_items = False

        choice = MyChoice()
        self.assertFalse(choice.matches(operator=choice.get_operator(b'contains'), match_value=[
         b'foo1', b'foo2'], condition_value=b'bar', value_state_cache={}))


class ConditionChoicesTests(TestCase):
    """Unit tests for djblets.conditions.choices.ConditionChoices."""

    def test_init_with_class_choices(self):
        """Testing ConditionChoices initialization with class-defined choices
        """

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice-1'

        class MyChoices(ConditionChoices):
            choice_classes = [
             MyChoice1]

        choices = MyChoices()
        self.assertEqual(list(choices), [MyChoice1])

    def test_init_with_caller_choices(self):
        """Testing ConditionChoices initialization with caller-defined choices
        """

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice-1'

        class MyChoice2(BaseConditionChoice):
            choice_id = b'my-choice-2'

        class MyChoices(ConditionChoices):
            choice_classes = [
             MyChoice1]

        choices = MyChoices([MyChoice2])
        self.assertEqual(list(choices), [MyChoice2])

    def test_get_choice(self):
        """Testing ConditionChoices.get_choice"""

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice-1'

        choices = ConditionChoices([MyChoice1])
        self.assertEqual(choices.get_choice(b'my-choice-1').__class__, MyChoice1)

    def test_get_choice_with_invalid_id(self):
        """Testing ConditionChoices.get_choice with invalid ID"""
        choices = ConditionChoices()
        with self.assertRaises(ConditionChoiceNotFoundError):
            choices.get_choice(b'invalid')

    def test_get_choice_with_kwargs(self):
        """Testing ConditionChoices.get_choice with kwargs for extra state"""

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice-1'

        choices = ConditionChoices([MyChoice1])
        choice = choices.get_choice(b'my-choice-1', choice_kwargs={b'abc': 123})
        self.assertEqual(choice.extra_state, {b'abc': 123})

    def test_get_choices(self):
        """Testing ConditionChoices.get_choices"""

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice-1'

        class MyChoice2(BaseConditionChoice):
            choice_id = b'my-choice-2'

        choices = ConditionChoices([MyChoice1, MyChoice2])
        choices = list(choices.get_choices())
        self.assertEqual(len(choices), 2)
        self.assertEqual(choices[0].__class__, MyChoice1)
        self.assertEqual(choices[1].__class__, MyChoice2)

    def test_get_choices_with_kwargs(self):
        """Testing ConditionChoices.get_choices with kwargs"""

        class MyChoice1(BaseConditionChoice):
            choice_id = b'my-choice-1'

        class MyChoice2(BaseConditionChoice):
            choice_id = b'my-choice-2'

        choices = ConditionChoices([MyChoice1, MyChoice2])
        choices = list(choices.get_choices(choice_kwargs={b'abc': 123}))
        self.assertEqual(len(choices), 2)
        self.assertEqual(choices[0].extra_state, {b'abc': 123})
        self.assertEqual(choices[1].extra_state, {b'abc': 123})