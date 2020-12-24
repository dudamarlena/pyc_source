# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/evolutions/add_diff_hash.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django_evolution.mutations import AddField, RenameField
from django.db import models
MUTATIONS = [
 RenameField(b'FileDiff', b'diff', b'diff64', db_column=b'diff_base64'),
 RenameField(b'FileDiff', b'parent_diff', b'parent_diff64', db_column=b'parent_diff_base64'),
 AddField(b'FileDiff', b'diff_hash', models.ForeignKey, null=True, related_model=b'diffviewer.FileDiffData'),
 AddField(b'FileDiff', b'parent_diff_hash', models.ForeignKey, null=True, related_model=b'diffviewer.FileDiffData')]