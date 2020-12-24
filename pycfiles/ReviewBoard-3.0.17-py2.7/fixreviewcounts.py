# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/management/commands/fixreviewcounts.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.core.management.base import NoArgsCommand
from reviewboard.accounts.admin import fix_review_counts

class Command(NoArgsCommand):
    help = b'Fixes all incorrect review request-related counters.'

    def handle_noargs(self, **options):
        fix_review_counts()