# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/conditions/tests/test_operators.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
import re
from djblets.conditions.choices import BaseConditionChoice
from djblets.conditions.errors import ConditionOperatorNotFoundError
from djblets.conditions.operators import AnyOperator, BaseConditionOperator, ConditionOperators, ContainsAnyOperator, ContainsOperator, DoesNotContainAnyOperator, DoesNotContainOperator, DoesNotMatchRegexOperator, EndsWithOperator, GreaterThanOperator, IsNotOneOfOperator, IsNotOperator, IsOneOfOperator, IsOperator, LessThanOperator, MatchesRegexOperator, StartsWithOperator, UnsetOperator
from djblets.conditions.values import BaseConditionValueField, ConditionValueIntegerField
from djblets.testing.testcases import TestCase

class BaseConditionOperatorTests(TestCase):
    """Unit tests for djblets.conditions.operators.BaseConditionOperator."""

    def test_value_field_with_default(self):
        """Testing BaseConditionOperator.value_field with default choice field
        """

        class MyOperator(BaseConditionOperator):
            operator_id = b'my-op'

        class MyChoice(BaseConditionChoice):
            operators = ConditionOperators([
             MyOperator])
            default_value_field = BaseConditionValueField()

        choice = MyChoice()
        op = choice.get_operator(b'my-op')
        self.assertEqual(op.value_field, choice.default_value_field)
        self.assertFalse(op.has_custom_value_field)

    def test_value_field_with_default_as_function(self):
        """Testing BaseConditionOperator.value_field with default choice field
        as a function
        """

        class MyOperator(BaseConditionOperator):
            operator_id = b'my-op'

        class MyChoice(BaseConditionChoice):
            operators = ConditionOperators([
             MyOperator])

            def default_value_field(self, **kwargs):
                return _my_value_field

        _my_value_field = BaseConditionValueField()
        choice = MyChoice()
        op = choice.get_operator(b'my-op')
        self.assertEqual(op.value_field, _my_value_field)
        self.assertFalse(op.has_custom_value_field)

    def test_value_field_with_custom(self):
        """Testing BaseConditionOperator.value_field with custom choice field
        """

        class MyOperator(BaseConditionOperator):
            operator_id = b'my-op'
            value_field = BaseConditionValueField()

        class MyChoice(BaseConditionChoice):
            operators = ConditionOperators([
             MyOperator])
            default_value_field = BaseConditionValueField()

        choice = MyChoice()
        op = choice.get_operator(b'my-op')
        self.assertNotEqual(op.value_field, choice.default_value_field)
        self.assertTrue(op.has_custom_value_field)

    def test_with_overrides(self):
        """Testing BaseConditionOperator.with_overrides"""

        class MyOperator(BaseConditionOperator):
            operator_id = b'my-op'
            name = b'My Op'
            value_field = BaseConditionValueField()

        CustomOperator = MyOperator.with_overrides(name=b'Custom Op', value_field=ConditionValueIntegerField())
        self.assertEqual(CustomOperator.__name__, b'CustomMyOperator')
        self.assertEqual(CustomOperator.name, b'Custom Op')
        self.assertIs(CustomOperator.value_field.__class__, ConditionValueIntegerField)


class ConditionOperatorsTests(TestCase):
    """Unit tests for djblets.conditions.operators.ConditionOperators."""

    def test_init_with_class_operators(self):
        """Testing ConditionOperators initialization with class-defined operators
        """

        class MyOperator1(BaseConditionOperator):
            operator_id = b'my-operator-1'

        class MyOperators(ConditionOperators):
            operator_classes = [
             MyOperator1]

        operators = MyOperators()
        self.assertEqual(list(operators), [MyOperator1])

    def test_init_with_caller_operators(self):
        """Testing ConditionOperators initialization with caller-defined operators
        """

        class MyOperator1(BaseConditionOperator):
            operator_id = b'my-operator-1'

        class MyOperator2(BaseConditionOperator):
            operator_id = b'my-operator-2'

        class MyOperators(ConditionOperators):
            operator_classes = [
             MyOperator1]

        operators = MyOperators([MyOperator2])
        self.assertEqual(list(operators), [MyOperator2])

    def test_get_operator(self):
        """Testing ConditionOperators.get_operator"""

        class MyOperator1(BaseConditionOperator):
            operator_id = b'my-operator-1'

        class MyChoice(BaseConditionChoice):
            operators = ConditionOperators([MyOperator1])

        choice = MyChoice()
        self.assertEqual(choice.operators.get_operator(b'my-operator-1', choice).__class__, MyOperator1)

    def test_get_operator_with_invalid_id(self):
        """Testing ConditionOperators.get_operator with invalid ID"""
        operators = ConditionOperators()
        with self.assertRaises(ConditionOperatorNotFoundError):
            operators.get_operator(b'invalid', None)
        return


class StandardOperatorTests(TestCase):
    """Unit tests for standard condition operators."""

    def test_is_one_of_op_with_match(self):
        """Testing IsOneOfOperator with match"""
        self.assertTrue(self._check_match(IsOneOfOperator, b'a', [
         b'a', b'b', b'c']))
        self.assertTrue(self._check_match(IsOneOfOperator, 1, [0, 1, 2]))

    def test_is_one_of_op_without_match(self):
        """Testing IsOneOfOperator without match"""
        self.assertFalse(self._check_match(IsOneOfOperator, b'd', [
         b'a', b'b', b'c']))
        self.assertFalse(self._check_match(IsOneOfOperator, 4, [0, 1, 2]))

    def test_is_not_one_of_op_with_match(self):
        """Testing IsNotOneOfOperator with match"""
        self.assertTrue(self._check_match(IsNotOneOfOperator, b'z', [
         b'a', b'b', b'c']))
        self.assertTrue(self._check_match(IsNotOneOfOperator, 9, [0, 1, 2]))

    def test_is_not_one_of_op_without_match(self):
        """Testing IsNotOneOfOperator without match"""
        self.assertFalse(self._check_match(IsNotOneOfOperator, b'a', [
         b'a', b'b', b'c']))
        self.assertFalse(self._check_match(IsNotOneOfOperator, 0, [0, 1, 2]))

    def test_any_op_with_match(self):
        """Testing AnyOperator with match"""
        self.assertTrue(self._check_match(AnyOperator, b'foo'))
        self.assertTrue(self._check_match(AnyOperator, 0))
        self.assertTrue(self._check_match(AnyOperator, False))

    def test_any_op_without_match(self):
        """Testing AnyOperator without match"""
        self.assertFalse(self._check_match(AnyOperator, b''))
        self.assertFalse(self._check_match(AnyOperator, None))
        self.assertFalse(self._check_match(AnyOperator, {}))
        self.assertFalse(self._check_match(AnyOperator, []))
        return

    def test_unset_op_with_match(self):
        """Testing UnsetOperator with match"""
        self.assertTrue(self._check_match(UnsetOperator, b''))
        self.assertTrue(self._check_match(UnsetOperator, None))
        self.assertTrue(self._check_match(UnsetOperator, {}))
        self.assertTrue(self._check_match(UnsetOperator, []))
        return

    def test_unset_op_without_match(self):
        """Testing UnsetOperator without match"""
        self.assertFalse(self._check_match(UnsetOperator, b'foo'))
        self.assertFalse(self._check_match(UnsetOperator, 0))
        self.assertFalse(self._check_match(UnsetOperator, False))

    def test_is_op_with_match(self):
        """Testing IsOperator with match"""
        self.assertTrue(self._check_match(IsOperator, 1, 1))
        self.assertTrue(self._check_match(IsOperator, b'test', b'test'))
        self.assertTrue(self._check_match(IsOperator, True, True))
        self.assertTrue(self._check_match(IsOperator, [b'a', b'b'], [b'a', b'b']))

    def test_is_op_without_match(self):
        """Testing IsOperator without match"""
        self.assertFalse(self._check_match(IsOperator, 0, 1))
        self.assertFalse(self._check_match(IsOperator, b'hi', b'test'))
        self.assertFalse(self._check_match(IsOperator, True, False))
        self.assertFalse(self._check_match(IsOperator, [1, 2], [b'a', b'b']))

    def test_is_not_op_with_match(self):
        """Testing IsNotOperator with match"""
        self.assertTrue(self._check_match(IsNotOperator, 0, 1))
        self.assertTrue(self._check_match(IsNotOperator, b'hi', b'test'))
        self.assertTrue(self._check_match(IsNotOperator, True, False))
        self.assertTrue(self._check_match(IsNotOperator, [1, 2], [b'a', b'b']))

    def test_is_not_op_without_match(self):
        """Testing IsNotOperator without match"""
        self.assertFalse(self._check_match(IsNotOperator, 1, 1))
        self.assertFalse(self._check_match(IsNotOperator, b'test', b'test'))
        self.assertFalse(self._check_match(IsNotOperator, True, True))
        self.assertFalse(self._check_match(IsNotOperator, [
         b'a', b'b'], [b'a', b'b']))

    def test_contains_op_with_match(self):
        """Testing ContainsOperator with match"""
        self.assertTrue(self._check_match(ContainsOperator, b'hello world', b'world'))
        self.assertTrue(self._check_match(ContainsOperator, [1, 2, 3], 1))

    def test_contains_op_without_match(self):
        """Testing ContainsOperator without match"""
        self.assertFalse(self._check_match(ContainsOperator, b'hello world', b'hey'))
        self.assertFalse(self._check_match(ContainsOperator, [1, 2, 3], 4))

    def test_does_not_contain_op_with_match(self):
        """Testing DoesNotContainOperator with match"""
        self.assertTrue(self._check_match(DoesNotContainOperator, b'hello world', b'hey'))
        self.assertTrue(self._check_match(DoesNotContainOperator, [
         1, 2, 3], 4))

    def test_does_not_contain_op_without_match(self):
        """Testing DoesNotContainOperator without match"""
        self.assertFalse(self._check_match(DoesNotContainOperator, b'hello world', b'hello'))
        self.assertFalse(self._check_match(DoesNotContainOperator, [
         1, 2, 3], 1))

    def test_contains_any_op_with_match(self):
        """Testing ContainsAnyOperator with match"""
        self.assertTrue(self._check_match(ContainsAnyOperator, [
         b'abc', b'def', b'xyz'], [
         b'def']))
        self.assertTrue(self._check_match(ContainsAnyOperator, [
         b'abc', b'def', b'xyz'], [
         b'def', b'XXX']))

    def test_contains_any_op_without_match(self):
        """Testing ContainsAnyOperator without match"""
        self.assertFalse(self._check_match(ContainsAnyOperator, [
         b'abc', b'def', b'xyz'], [
         b'XXX']))

    def test_does_not_contain_any_op_with_match(self):
        """Testing DoesNotContainAnyOperator with match"""
        self.assertTrue(self._check_match(DoesNotContainAnyOperator, [
         b'abc', b'def', b'xyz'], [
         b'XXX']))

    def test_does_not_contain_any_op_without_match(self):
        """Testing DoesNotContainAnyOperator without match"""
        self.assertFalse(self._check_match(DoesNotContainAnyOperator, [
         b'abc', b'def', b'xyz'], [
         b'def']))
        self.assertFalse(self._check_match(DoesNotContainAnyOperator, [
         b'abc', b'def', b'xyz'], [
         b'def', b'XXX']))

    def test_starts_with_op_with_match(self):
        """Testing StartsWithOperator with match"""
        self.assertTrue(self._check_match(StartsWithOperator, b'hello world', b'he'))

    def test_starts_without_op_without_match(self):
        """Testing StartsWithOperator without match"""
        self.assertFalse(self._check_match(StartsWithOperator, b'hello world', b'wo'))

    def test_ends_with_op_with_match(self):
        """Testing EndsWithOperator with match"""
        self.assertTrue(self._check_match(EndsWithOperator, b'hello world', b'ld'))

    def test_ends_without_op_without_match(self):
        """Testing EndsWithOperator without match"""
        self.assertFalse(self._check_match(EndsWithOperator, b'hello world', b'lo'))

    def test_greater_than_op_with_match(self):
        """Testing GreaterThanOperator with match"""
        self.assertTrue(self._check_match(GreaterThanOperator, 100, 20))

    def test_greater_than_op_without_match(self):
        """Testing GreaterThanOperator without match"""
        self.assertFalse(self._check_match(GreaterThanOperator, 20, 100))

    def test_less_than_op_with_match(self):
        """Testing LessThanOperator with match"""
        self.assertTrue(self._check_match(LessThanOperator, 20, 100))

    def test_less_than_op_without_match(self):
        """Testing LessThanOperator without match"""
        self.assertFalse(self._check_match(LessThanOperator, 100, 20))

    def test_matches_regex_op_with_match(self):
        """Testing MatchesRegexOperator with match"""
        self.assertTrue(self._check_match(MatchesRegexOperator, b'abccd', re.compile(b'abc+de?')))

    def test_matches_regex_op_without_match(self):
        """Testing MatchesRegexOperator without match"""
        self.assertFalse(self._check_match(MatchesRegexOperator, b'xyz', re.compile(b'abc+de?')))

    def test_does_not_match_regex_op_with_match(self):
        """Testing DoesNotMatchRegexOperator with match"""
        self.assertTrue(self._check_match(DoesNotMatchRegexOperator, b'xyz', re.compile(b'abc+de?')))

    def test_does_not_match_regex_op_without_match(self):
        """Testing DoesNotMatchRegexOperator without match"""
        self.assertFalse(self._check_match(DoesNotMatchRegexOperator, b'abccd', re.compile(b'abc+de?')))

    def _check_match(self, op_cls, match_value, condition_value=None):
        op = op_cls(None)
        return op.matches(match_value=match_value, condition_value=condition_value)