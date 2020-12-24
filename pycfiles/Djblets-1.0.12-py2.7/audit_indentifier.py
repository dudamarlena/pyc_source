# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/privacy/evolutions/audit_indentifier.py
# Compiled at: 2019-06-12 01:17:17
"""Evolution to remove unique constraint from StoredConsentData."""
from __future__ import unicode_literals
from django_evolution.mutations import ChangeField
MUTATIONS = [
 ChangeField(b'StoredConsentData', b'audit_identifier', initial=None, unique=False)]