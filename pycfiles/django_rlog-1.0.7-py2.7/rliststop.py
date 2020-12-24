# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/django_rlog/management/commands/rliststop.py
# Compiled at: 2016-08-23 01:20:06
from django_rlog.connect import get_connection
from django_rlog.defaults import DEFAULT_KEY
from django_six import CompatibilityBaseCommand

class Command(CompatibilityBaseCommand):
    help = 'Stop rlistlog.'

    def add_arguments(self, parser):
        parser.add_argument('--key', dest='key', default=DEFAULT_KEY, help='Key RedisListHandler use.')

    def handle(self, *args, **options):
        r = get_connection()
        r.rpush(options.get('key', DEFAULT_KEY), 'KILL')