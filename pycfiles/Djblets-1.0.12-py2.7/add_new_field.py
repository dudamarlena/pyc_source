# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/extensions/test/evolve_tests/evolutions/add_new_field.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals
from django_evolution.mutations import AddField
from django.db import models
MUTATIONS = [
 AddField(b'TestEvolveExtensionModel', b'new_field', models.IntegerField, initial=42)]