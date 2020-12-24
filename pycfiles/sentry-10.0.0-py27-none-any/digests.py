# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/tasks/digests.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import logging, time
from sentry.digests import get_option_key
from sentry.digests.backends.base import InvalidState
from sentry.digests.notifications import build_digest, split_key
from sentry.models import Project, ProjectOption
from sentry.tasks.base import instrumented_task
from sentry.utils import snuba
logger = logging.getLogger(__name__)

@instrumented_task(name='sentry.tasks.digests.schedule_digests', queue='digests.scheduling')
def schedule_digests():
    from sentry import digests
    deadline = time.time()
    timeout = 300
    digests.maintenance(deadline - timeout)
    for entry in digests.schedule(deadline):
        deliver_digest.delay(entry.key, entry.timestamp)


@instrumented_task(name='sentry.tasks.digests.deliver_digest', queue='digests.delivery')
def deliver_digest(key, schedule_timestamp=None):
    from sentry import digests
    try:
        plugin, project = split_key(key)
    except Project.DoesNotExist as error:
        logger.info('Cannot deliver digest %r due to error: %s', key, error)
        digests.delete(key)
        return

    minimum_delay = ProjectOption.objects.get_value(project, get_option_key(plugin.get_conf_key(), 'minimum_delay'))
    with snuba.options_override({'consistent': True}):
        try:
            with digests.digest(key, minimum_delay=minimum_delay) as (records):
                digest = build_digest(project, records)
        except InvalidState as error:
            logger.info('Skipped digest delivery: %s', error, exc_info=True)
            return

        if digest:
            plugin.notify_digest(project, digest)