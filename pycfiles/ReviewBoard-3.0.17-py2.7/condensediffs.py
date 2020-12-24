# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/management/commands/condensediffs.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals, division
import sys
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.management.base import NoArgsCommand
from django.utils.translation import ugettext as _, ungettext_lazy as N_
from reviewboard.diffviewer.models import FileDiff

class Command(NoArgsCommand):
    help = b'Condenses the diffs stored in the database, reducing space requirements'
    DELAY_SHOW_REMAINING_SECS = 30
    TIME_REMAINING_CHUNKS = (
     (
      31536000, N_(b'%d year', b'%d years')),
     (
      2592000, N_(b'%d month', b'%d months')),
     (
      604800, N_(b'%d week', b'%d weeks')),
     (
      86400, N_(b'%d day', b'%d days')),
     (
      3600, N_(b'%d hour', b'%d hours')),
     (
      60, N_(b'%d minute', b'%d minutes')))
    TIME_REMAINING_STR = _(b'%s remaining                                  ')
    CALC_TIME_REMAINING_STR = _(b'Calculating time remaining')

    def handle_noargs(self, **options):
        counts = FileDiff.objects.get_migration_counts()
        total_count = counts[b'total_count']
        if total_count == 0:
            self.stdout.write(_(b'All diffs have already been migrated.\n'))
            return
        self.stdout.write(_(b'Processing %(count)d diffs for duplicates...\n\nThis may take a while. It is safe to continue using Review Board while this is\nprocessing, but it may temporarily run slower.\n\n') % {b'count': total_count})
        settings.DEBUG = False
        self.start_time = datetime.now()
        self.prev_prefix_len = 0
        self.prev_time_remaining_s = b''
        self.show_remaining = False
        info = FileDiff.objects.migrate_all(self._on_batch_done, counts)
        old_diff_size = info[b'old_diff_size']
        new_diff_size = info[b'new_diff_size']
        self.stdout.write(_(b'\n\nCondensed stored diffs from %(old_size)s bytes to %(new_size)s bytes (%(savings_pct)0.2f%% savings)\n') % {b'old_size': intcomma(old_diff_size), 
           b'new_size': intcomma(new_diff_size), 
           b'savings_pct': float(old_diff_size - new_diff_size) / float(old_diff_size) * 100})

    def _on_batch_done(self, processed_count, total_count):
        """Handler for when a batch of diffs are processed.

        This will report the progress of the operation, showing the estimated
        amount of time remaining.
        """
        pct = processed_count * 100 / total_count
        delta = datetime.now() - self.start_time
        delta_secs = (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) * 1000000) / 1000000
        if not self.show_remaining and delta_secs >= self.DELAY_SHOW_REMAINING_SECS:
            self.show_remaining = True
        if self.show_remaining:
            secs_left = delta_secs // processed_count * (total_count - processed_count)
            time_remaining_s = self.TIME_REMAINING_STR % self._time_remaining(secs_left)
        else:
            time_remaining_s = self.CALC_TIME_REMAINING_STR
        prefix_s = b'  [%d%%] %s/%s - ' % (pct, processed_count, total_count)
        sys.stdout.write(prefix_s)
        if self.prev_prefix_len != len(prefix_s) or self.prev_time_remaining_s != time_remaining_s:
            sys.stdout.write(time_remaining_s)
            self.prev_prefix_len = len(prefix_s)
            self.prev_time_remaining_s = time_remaining_s
        sys.stdout.write(b'\r')
        sys.stdout.flush()

    def _time_remaining(self, secs_left):
        """Returns a string representing the time remaining for the operation.

        This is a simplified version of Django's timeuntil() function that
        does fewer calculations in order to reduce the amount of time we
        have to spend every loop. For instance, it doesn't bother with
        constructing datetimes and recomputing deltas, since we already
        have those, and it doesn't rebuild the TIME_REMAINING_CHUNKS
        every time it's called. It also handles seconds.
        """
        delta = timedelta(seconds=secs_left)
        since = delta.days * 24 * 60 * 60 + delta.seconds
        if since < 60:
            return N_(b'%d second', b'%d seconds') % since
        for i, (seconds, name) in enumerate(self.TIME_REMAINING_CHUNKS):
            count = since // seconds
            if count != 0:
                break

        result = name % count
        if i + 1 < len(self.TIME_REMAINING_CHUNKS):
            seconds2, name2 = self.TIME_REMAINING_CHUNKS[(i + 1)]
            count2 = (since - seconds * count) // seconds2
            if count2 != 0:
                result += b', ' + name2 % count2
        return result