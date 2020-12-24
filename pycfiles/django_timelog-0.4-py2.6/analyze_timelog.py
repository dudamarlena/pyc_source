# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/timelog/management/commands/analyze_timelog.py
# Compiled at: 2011-06-22 14:48:29
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from timelog.lib import generate_table_from, analyze_log_file, PATTERN

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
     make_option('--file', dest='file', default=settings.TIMELOG_LOG, help='Specify file to use'),
     make_option('--noreverse', dest='reverse', action='store_false', default=True, help='Show paths instead of views'))

    def handle(self, *args, **options):
        LOGFILE = options.get('file')
        try:
            data = analyze_log_file(LOGFILE, PATTERN, reverse_paths=options.get('reverse'))
        except IOError:
            print 'File not found'
            exit(2)

        print generate_table_from(data)