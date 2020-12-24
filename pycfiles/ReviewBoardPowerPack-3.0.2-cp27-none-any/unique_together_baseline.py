# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/evolutions/unique_together_baseline.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
from django_evolution.mutations import ChangeMeta
MUTATIONS = [
 ChangeMeta(b'StoredUserKey', b'unique_together', [
  ('namespace', 'name')])]