# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/evolutions/review_request_summary_index_manual.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.conf import settings
from django_evolution.mutations import ChangeField, SQLMutation
if settings.DATABASES[b'default'][b'ENGINE'].endswith(b'mysql'):
    field_index_suffix = b'(255)'
else:
    field_index_suffix = b''
index_sql = b'CREATE INDEX reviews_reviewrequest_summary ON reviews_reviewrequest (summary%s);' % field_index_suffix
MUTATIONS = [
 ChangeField(b'ReviewRequest', b'summary', initial=None, db_index=False),
 SQLMutation(b'reviewrequest_summary', [index_sql])]