# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ggg/www/dev/mogos/mogo79/mogo/watchtower/management/commands/collect.py
# Compiled at: 2017-10-24 12:32:33
# Size of source mod 2**32: 781 bytes
from __future__ import print_function
import time, redis
from django.core.management.base import BaseCommand
from watchtower.db import dispatch
from watchtower.db.redis import getHits, getEvents
from watchtower.conf import FREQUENCY, VERBOSITY

class Command(BaseCommand):
    help = 'Start Watchtower collector'

    def handle(self, *args, **options):
        verbosity = options['verbosity']
        if verbosity is None:
            verbosity = VERBOSITY
        if verbosity > 0:
            print('Collecting data ...')
        r = redis.Redis(host='localhost', port=6379, db=0)
        while True:
            hits = getHits(r)
            events = getEvents(r)
            dispatch(hits, events, verbosity)
            time.sleep(FREQUENCY)