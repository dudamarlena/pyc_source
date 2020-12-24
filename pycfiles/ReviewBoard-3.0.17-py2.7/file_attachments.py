# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/evolutions/file_attachments.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django_evolution.mutations import AddField
from django.db import models
MUTATIONS = [
 AddField(b'ReviewRequest', b'file_attachments', models.ManyToManyField, related_model=b'attachments.FileAttachment'),
 AddField(b'ReviewRequest', b'inactive_file_attachments', models.ManyToManyField, related_model=b'attachments.FileAttachment'),
 AddField(b'Review', b'file_attachment_comments', models.ManyToManyField, related_model=b'reviews.FileAttachmentComment'),
 AddField(b'ReviewRequestDraft', b'file_attachments', models.ManyToManyField, related_model=b'attachments.FileAttachment'),
 AddField(b'ReviewRequestDraft', b'inactive_file_attachments', models.ManyToManyField, related_model=b'attachments.FileAttachment')]