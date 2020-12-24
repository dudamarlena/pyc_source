# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/db/tests/test_query.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils import six
from djblets.db.query import chainable_select_related_queryset, prefix_q
from djblets.testing.testcases import TestCase

class ChainableSelectRelatedQuerySetTests(TestCase):
    """Tests for djblets.db.query.chainable_select_related_queryset."""

    def test_select_related_with_new_fields(self):
        """Testing chainable_select_related_queryset with
        select_related(field, ...)
        """
        queryset = User.objects.select_related(b'foo')
        queryset = chainable_select_related_queryset(queryset)
        queryset = queryset.select_related(b'foo__bar', b'baz')
        queryset = queryset.select_related(b'foobar', b'baz')
        self.assertEqual(queryset.query.select_related, {b'foo': {b'bar': {}}, b'baz': {}, b'foobar': {}})

    def test_select_related_with_new_no_args(self):
        """Testing chainable_select_related_queryset with select_related()"""
        queryset = User.objects.select_related(b'foo')
        queryset = chainable_select_related_queryset(queryset)
        queryset = queryset.select_related()
        self.assertTrue(queryset.query.select_related)

    def test_select_related_with_none(self):
        """Testing chainable_select_related_queryset with select_related(None)
        """
        queryset = User.objects.select_related(b'foo')
        queryset = chainable_select_related_queryset(queryset)
        queryset = queryset.select_related(None)
        self.assertFalse(queryset.query.select_related)
        return


class PrefixTests(TestCase):
    """Tests for djblets.db.query.prefix_q."""

    def test_simple(self):
        """Testing prefix_q prefixes simple expressions"""
        self.assertEqual(six.text_type(prefix_q(b'fk', Q(hello=b'goodbye'))), six.text_type(Q(fk__hello=b'goodbye')))

    def test_nested(self):
        """Testing prefix_q prefixes nested expressions"""
        self.assertEqual(six.text_type(prefix_q(b'fk', Q(foo=b'foo') | Q(bar=b'bar') & Q(baz=b'baz'))), six.text_type(Q(fk__foo=b'foo') | Q(fk__bar=b'bar') & Q(fk__baz=b'baz')))

    def test_bytestring_result(self):
        """Testing that prefix_q generates byte strings for key names"""
        q = prefix_q(b'fk', Q(foo=b'bar'))
        self.assertEqual(len(q.children), 1)
        self.assertIs(type(q.children[0]), tuple)
        self.assertIsInstance(q.children[0][0], six.binary_type)