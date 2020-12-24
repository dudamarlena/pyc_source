# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/evolutions/raw_diff_file_data.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django_evolution.mutations import AddField, RenameField, RenameModel
from django.db import models
MUTATIONS = [
 RenameModel(b'FileDiffData', b'LegacyFileDiffData', db_table=b'diffviewer_filediffdata'),
 RenameField(b'FileDiff', b'diff_hash', b'legacy_diff_hash', db_column=b'diff_hash_id'),
 RenameField(b'FileDiff', b'parent_diff_hash', b'legacy_parent_diff_hash', db_column=b'parent_diff_hash_id'),
 AddField(b'FileDiff', b'diff_hash', models.ForeignKey, null=True, db_column=b'raw_diff_hash_id', related_model=b'diffviewer.RawFileDiffData'),
 AddField(b'FileDiff', b'parent_diff_hash', models.ForeignKey, null=True, db_column=b'raw_parent_diff_hash_id', related_model=b'diffviewer.RawFileDiffData')]