# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/evolutions/repository_hooks_uuid.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django_evolution.mutations import AddField, ChangeMeta
from django.db import models
MUTATIONS = [
 AddField(b'Repository', b'hooks_uuid', models.CharField, max_length=32, null=True),
 ChangeMeta(b'Repository', b'unique_together', (
  ('name', 'local_site'),
  ('archived_timestamp', 'path', 'local_site'),
  ('hooks_uuid', 'local_site')))]