# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/bgtasks/clean_dsymcache.py
# Compiled at: 2019-08-16 12:27:40
from __future__ import absolute_import
from sentry.bgtasks.api import bgtask
from sentry.models import ProjectDebugFile

@bgtask()
def clean_dsymcache():
    ProjectDebugFile.difcache.clear_old_entries()