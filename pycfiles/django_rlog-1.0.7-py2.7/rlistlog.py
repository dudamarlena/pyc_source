# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/django_rlog/management/commands/rlistlog.py
# Compiled at: 2016-08-23 01:20:06
from __future__ import print_function
from django_rlog.connect import get_connection
from django_rlog.defaults import DEFAULT_KEY, DEFAULT_TIMEOUT
from django_rlog.logger import get_logger
from django_rlog.management.commands._arguments import _add_arguments
from django_six import CompatibilityBaseCommand

class Command(CompatibilityBaseCommand):
    help = "Save rlog's RedisListHandler Log to Disk."

    def add_arguments(self, parser):
        parser.add_argument('--key', dest='key', default=DEFAULT_KEY, help='Key RedisListHandler use.')
        parser.add_argument('--timeout', dest='timeout', default=DEFAULT_TIMEOUT, type=int, help='Timeout of BLPOP/BRPOP.')
        _add_arguments(parser)

    def handle(self, *args, **options):
        debug = options.get('debug', False)
        key = options.get('key', DEFAULT_KEY)
        timeout = options.get('timeout', DEFAULT_TIMEOUT)
        r = get_connection()
        logger = get_logger(**options)
        goon = True
        while goon:
            data = r.blpop(key, timeout)
            if not data:
                continue
            if data[(-1)] != 'KILL':
                if debug:
                    print(data)
                logger.debug(data[(-1)])
            else:
                goon = False