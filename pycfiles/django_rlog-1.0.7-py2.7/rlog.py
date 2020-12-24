# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/django_rlog/management/commands/rlog.py
# Compiled at: 2016-08-23 01:20:06
from __future__ import print_function
from django_rlog.connect import get_connection
from django_rlog.defaults import DEFAULT_CHANNEL
from django_rlog.logger import get_logger
from django_rlog.management.commands._arguments import _add_arguments
from django_six import CompatibilityBaseCommand

class Command(CompatibilityBaseCommand):
    help = "Save rlog's RedisHandler Log to Disk."

    def add_arguments(self, parser):
        parser.add_argument('--channel', dest='channel', default=DEFAULT_CHANNEL, help='Pubsub channel RedisHandler use.')
        _add_arguments(parser)

    def handle(self, *args, **options):
        debug = options.get('debug', False)
        channel = options.get('channel', DEFAULT_CHANNEL)
        r = get_connection()
        logger = get_logger(**options)
        p = r.pubsub()
        p.subscribe(channel)
        for item in p.listen():
            if item['type'] == 'message':
                if debug:
                    print(item)
                p.unsubscribe() if item['data'] == 'KILL' else logger.debug(item.get('data', ''))