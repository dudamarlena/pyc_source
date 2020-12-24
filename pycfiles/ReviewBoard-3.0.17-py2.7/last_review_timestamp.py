# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/evolutions/last_review_timestamp.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.db import models
from django_evolution.mutations import AddField, SQLMutation
MUTATIONS = [
 AddField(b'ReviewRequest', b'last_review_timestamp', models.DateTimeField, null=True),
 SQLMutation(b'populate_last_review_timestamp', [
  b'\n        UPDATE reviews_reviewrequest\n           SET last_review_timestamp = (\n               SELECT reviews_review.timestamp\n                 FROM reviews_review\n                WHERE reviews_review.review_request_id =\n                      reviews_reviewrequest.id\n                  AND reviews_review.public\n                ORDER BY reviews_review.timestamp DESC\n                LIMIT 1)\n'])]