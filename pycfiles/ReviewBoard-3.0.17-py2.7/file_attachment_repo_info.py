# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/attachments/evolutions/file_attachment_repo_info.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django_evolution.mutations import AddField
from django.db import models
MUTATIONS = [
 AddField(b'FileAttachment', b'repository', models.ForeignKey, null=True, related_model=b'scmtools.Repository'),
 AddField(b'FileAttachment', b'repo_revision', models.CharField, max_length=512, null=True, db_index=True),
 AddField(b'FileAttachment', b'repo_path', models.CharField, max_length=1024, null=True),
 AddField(b'FileAttachment', b'added_in_filediff', models.ForeignKey, null=True, related_model=b'diffviewer.FileDiff')]