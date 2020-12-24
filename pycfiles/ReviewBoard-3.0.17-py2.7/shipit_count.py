# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/evolutions/shipit_count.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.db import models
from django_evolution.mutations import AddField, SQLMutation
MUTATIONS = [
 AddField(b'ReviewRequest', b'shipit_count', models.IntegerField, initial=0, null=True),
 SQLMutation(b'populate_shipit_count', [
  b'\n        UPDATE reviews_reviewrequest\n           SET shipit_count = (\n               SELECT COUNT(*)\n                 FROM reviews_review\n                WHERE reviews_review.review_request_id =\n                      reviews_reviewrequest.id\n                  AND reviews_review.public\n                  AND reviews_review.ship_it\n                  AND reviews_review.base_reply_to_id is NULL)\n'])]