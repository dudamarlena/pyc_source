# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muhammadelias/grove_core/django-sql-explorer/explorer/tests/test_forms.py
# Compiled at: 2019-07-02 16:47:10
from django.test import TestCase
from django.forms.models import model_to_dict
from explorer.tests.factories import SimpleQueryFactory
from explorer.forms import QueryForm

class TestFormValidation(TestCase):

    def test_form_is_valid_with_valid_sql(self):
        q = SimpleQueryFactory(sql='select 1;', created_by_user_id=None)
        form = QueryForm(model_to_dict(q))
        self.assertTrue(form.is_valid())
        return

    def test_form_fails_blacklist(self):
        q = SimpleQueryFactory(sql='delete $$a$$;', created_by_user_id=None)
        q.params = {}
        form = QueryForm(model_to_dict(q))
        self.assertFalse(form.is_valid())
        return