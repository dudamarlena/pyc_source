# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/submit/task.py
# Compiled at: 2014-10-15 11:34:01
# Size of source mod 2**32: 1392 bytes
import celery, datetime, pytz
from mediagoblin.db.models import MediaEntry

@celery.task()
def collect_garbage():
    """
        Garbage collection to clean up media

        This will look for all critera on models to clean
        up. This is primerally written to clean up media that's
        entered a erroneous state.
    """
    cuttoff = datetime.datetime.now(pytz.UTC) - datetime.timedelta(days=1)
    garbage = MediaEntry.query.filter(MediaEntry.created < cuttoff)
    garbage = garbage.filter(MediaEntry.state == 'unprocessed')
    for entry in garbage.all():
        entry.delete()