# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/evolutions/split_rich_text.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django_evolution.mutations import AddField, SQLMutation
from django.db import models
MUTATIONS = [
 AddField(b'ReviewRequest', b'description_rich_text', models.BooleanField, initial=False),
 AddField(b'ReviewRequest', b'testing_done_rich_text', models.BooleanField, initial=False),
 AddField(b'ReviewRequestDraft', b'description_rich_text', models.BooleanField, initial=False),
 AddField(b'ReviewRequestDraft', b'testing_done_rich_text', models.BooleanField, initial=False),
 AddField(b'Review', b'body_top_rich_text', models.BooleanField, initial=False),
 AddField(b'Review', b'body_bottom_rich_text', models.BooleanField, initial=False),
 SQLMutation(b'review_request_rich_text_defaults', [
  b'\n        UPDATE reviews_reviewrequest\n           SET description_rich_text = rich_text,\n               testing_done_rich_text = rich_text;\n    ']),
 SQLMutation(b'review_request_draft_rich_text_defaults', [
  b'\n        UPDATE reviews_reviewrequestdraft\n           SET description_rich_text = rich_text,\n               testing_done_rich_text = rich_text;\n    ']),
 SQLMutation(b'review_rich_text_defaults', [
  b'\n        UPDATE reviews_review\n           SET body_top_rich_text = rich_text,\n               body_bottom_rich_text = rich_text;\n    '])]