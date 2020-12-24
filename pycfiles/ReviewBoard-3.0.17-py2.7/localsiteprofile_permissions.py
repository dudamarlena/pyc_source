# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/evolutions/localsiteprofile_permissions.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django_evolution.mutations import AddField
from djblets.db.fields import JSONField
MUTATIONS = [
 AddField(b'LocalSiteProfile', b'permissions', JSONField, null=True)]