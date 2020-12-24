# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/management/commands/reset-issue-counts.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError
from reviewboard.reviews.models import ReviewRequest

class Command(BaseCommand):
    help = b'Resets all calculated issue counts for review requests.'
    option_list = BaseCommand.option_list + (
     make_option(b'-a', b'--all', action=b'store_true', default=False, dest=b'all', help=b'Reset issue counts for all review requests.'),
     make_option(b'--recalculate', action=b'store_true', default=False, dest=b'recalculate', help=b'Recalculates issue counts for the review requests. This is not compatible with --all'))

    def handle(self, *args, **options):
        update_all = options.get(b'all')
        recalculate = options.get(b'recalculate')
        if update_all:
            if recalculate:
                raise CommandError(b'--recalculate cannot be used with --all')
            q = ReviewRequest.objects.all()
        else:
            pks = []
            for arg in args:
                try:
                    pks.append(int(arg))
                except ValueError:
                    raise CommandError(b'%s is not a valid review request ID' % arg)

            if not pks:
                raise CommandError(b'One or more review request IDs must be provided.')
            q = ReviewRequest.objects.filter(pk__in=pks)
        q.update(issue_open_count=None, issue_resolved_count=None, issue_dropped_count=None, issue_verifying_count=None)
        if not update_all and recalculate:
            if int(options[b'verbosity']) > 1:
                root_logger = logging.getLogger(b'')
                root_logger.setLevel(logging.DEBUG)
            list(q)
        if update_all:
            self.stdout.write(b'All issue counts reset.')
        else:
            self.stdout.write(b'Issue counts for review request(s) %s reset.' % (b', ').join(args))
        return