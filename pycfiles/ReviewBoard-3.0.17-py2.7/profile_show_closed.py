# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/accounts/evolutions/profile_show_closed.py
# Compiled at: 2020-02-11 04:03:56
from django_evolution.mutations import RenameField
MUTATIONS = [
 RenameField('Profile', 'show_submitted', 'show_closed')]